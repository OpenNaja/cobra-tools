#!/usr/bin/env python3
"""
PPUIPKG Explorer (PyQt5)

A single-file GUI tool to view, extract, import, drag-and-drop, and edit
`.ppuipkg` packages used by Jurassic World Evolution 3 UI mods.

Features
- Open/Save .ppuipkg files (custom XML-like format shown by the user)
- Read Base64 and legacy decimal content; save as Base64 or legacy decimals
- View a virtual folder tree of file_name entries
- Drag files OUT to the OS (materializes temp files with full in-archive path)
- Drag files IN from the OS (drop onto a folder or root to add/replace)
- Extract All to folder (recreates full paths)
- Import All from folder (recursive; paths relative to chosen folder)
- Import texture assets as icon metadata using their .tex sidecar's ovs value
- Preserve icon metadata on Open/Save; skip texture assets during extraction/drag-out
- Edit `game` and `basic_path` fields; changes are saved
- Context menu: Export Selected, Remove, Rename (in-archive path), Replace From File

Notes & assumptions
- The package format has a root element PPUIPKGRoot with attributes
  files_count, icondata_count, game; a <basic_path> element; a <files> list of
  <ppuipkgfile> with <file_name> and <file_content>. Base64 content has
  encoding="base64"; unmarked content and encoding="decimal" use space-separated
  decimal bytes. file_size is always the decoded byte count.
- Saves default to Base64, matching cobra-tools' Base64ArrayPointer. Choose
  Decimal (legacy) in Package Metadata when saving for older readers.
- Texture assets are virtual entries: their bytes are never stored or exported.
  On save they become <icondata>/<userinterfaceicondata> entries with <ovs>.
  Legacy <types>, <asset_package>, and <assetPackage> remain readable. Only a duplicated
  .png.png suffix loses its final .png; other image names retain their suffix.
  An existing .tex sidecar identifies non-PNG texture assets. Appended .tex and
  replacement-extension .tex sidecars are read only for metadata and never added.
- Drag-out creates temporary real files under a temp session directory and
  provides file:// URLs so your OS can receive them. Extract All is the
  recommended way to put files in a permanent location.
- Drag-in: dropping files on a folder node will add them with that folder as
  prefix. Dropping on the root puts them at the archive root (their relative
  paths from the dragged folder are preserved if you drag a folder).

Tested with: Python 3.9+, PyQt5

Run: python ppuipkg_explorer.py
"""
from __future__ import annotations
import base64
import binascii
import os
import sys
import tempfile
import shutil
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET

from PyQt5 import QtCore, QtGui, QtWidgets

# ------------------------------
# Data model
# ------------------------------

def bytes_to_decimal_string(b: bytes) -> str:
    return " ".join(str(x) for x in b)


def decimal_string_to_bytes(s: str) -> bytes:
    s = s.strip()
    if not s:
        return b""
    try:
        values = [int(p, 10) for p in s.split()]
    except ValueError as e:
        raise ValueError(f"Invalid decimal byte in content: {e}") from e
    if any(value < -128 or value > 255 for value in values):
        raise ValueError("Decimal byte values must be between -128 and 255")
    return bytes(value & 0xFF for value in values)


def file_content_to_bytes(elem: ET.Element) -> bytes:
    """Decode the explicit XML encoding; unmarked content is legacy decimal."""
    if len(elem):
        raise ValueError("file_content must contain text, not child elements")
    encoding = elem.get("encoding")
    text = elem.text or ""
    if encoding in (None, "decimal"):
        return decimal_string_to_bytes(text)
    if encoding == "base64":
        try:
            return base64.b64decode("".join(text.split()), validate=True)
        except (binascii.Error, ValueError) as e:
            raise ValueError(f"Invalid Base64 file_content: {e}") from e
    raise ValueError(f"Unsupported file_content encoding: {encoding!r}")


@dataclass
class PPUIPKGFile:
    file_name: str
    content: bytes
    # Private import metadata; texture/TEX contents are not retained in the package.
    _asset_package: Optional[str] = field(default=None, repr=False)

    @property
    def is_icondata(self) -> bool:
        return self._asset_package is not None

    @property
    def image_name(self) -> str:
        """Remove only the extra PNG export suffix, preserving other formats."""
        return self.file_name[:-4] if is_png_asset(self.file_name) else self.file_name

    @property
    def is_extractable(self) -> bool:
        return not (self.is_icondata or is_png_asset(self.file_name)
                    or is_texture_sidecar(self.file_name))


@dataclass
class PPUIPKG:
    game: str = ""
    basic_path: str = ""
    files: Dict[str, PPUIPKGFile] = field(default_factory=dict)
    _other_types: List[ET.Element] = field(default_factory=list, repr=False)

    @staticmethod
    def load(path: str) -> "PPUIPKG":
        tree = ET.parse(path)
        root = tree.getroot()
        if root.tag != "PPUIPKGRoot":
            raise ValueError("Not a PPUIPKGRoot document")
        game = root.attrib.get("game", "")
        basic_path_el = root.find("basic_path")
        basic_path = (basic_path_el.text or "") if basic_path_el is not None else ""
        files_el = root.find("files")
        files: Dict[str, PPUIPKGFile] = {}
        if files_el is not None:
            for f in files_el.findall("ppuipkgfile"):
                name_el = f.find("file_name")
                cont_el = f.find("file_content")
                if name_el is None or cont_el is None:
                    continue
                name = normalize_archive_path(name_el.text or "")
                if is_texture_sidecar(name):
                    continue
                try:
                    content = file_content_to_bytes(cont_el)
                    declared_size = f.get("file_size")
                    if declared_size is not None and int(declared_size) != len(content):
                        raise ValueError(f"file_size is {declared_size}, but decoded file_content has {len(content)} bytes")
                except ValueError as e:
                    raise ValueError(f"{name}: {e}") from e
                files[name] = PPUIPKGFile(name, content)
        pkg = PPUIPKG(game=game, basic_path=basic_path, files=files)
        types_el = root.find("icondata")
        if types_el is None:
            types_el = root.find("types")
        if types_el is not None:
            for node in types_el:
                if node.tag != "userinterfaceicondata":
                    pkg._other_types.append(deepcopy(node))
                    continue
                image_name = normalize_archive_path(node.findtext("image_name") or "")
                asset_package_el = node.find("ovs")
                if asset_package_el is None:
                    asset_package_el = node.find("asset_package")
                if asset_package_el is None:
                    asset_package_el = node.find("assetPackage")
                asset_package = asset_package_el.text if asset_package_el is not None else None
                if not image_name or not asset_package or not asset_package.strip():
                    raise ValueError("Invalid userinterfaceicondata: image_name and ovs are required")
                # Restore PNG export names without adding PNG suffixes to other
                # image formats or to already doubled legacy names.
                name = image_name
                if name.lower().endswith(".png") and not is_png_asset(name):
                    name += ".png"
                pkg.files[name] = PPUIPKGFile(name, b"", asset_package)
        return pkg

    def save(self, path: str, *, content_encoding: str = "base64") -> None:
        if content_encoding not in ("base64", "decimal"):
            raise ValueError(f"Unsupported output content encoding: {content_encoding!r}")
        regular_files = []
        icon_files = []
        for name in sorted(self.files):
            pfile = self.files[name]
            if is_texture_sidecar(pfile.file_name):
                continue
            if pfile.is_icondata:
                icon_files.append(pfile)
            elif is_png_asset(pfile.file_name):
                raise ValueError(f"PNG asset has no asset_package metadata: {pfile.file_name}")
            else:
                regular_files.append(pfile)
        root = ET.Element("PPUIPKGRoot", attrib={
            "files_count": str(len(regular_files)),
            "icondata_count": str(len(icon_files)),
            "game": self.game,
        })
        basic = ET.SubElement(root, "basic_path")
        basic.text = self.basic_path
        files_el = ET.SubElement(root, "files")
        # Deterministic order
        for pfile in regular_files:
            pnode = ET.SubElement(files_el, "ppuipkgfile", attrib={
                "file_size": str(len(pfile.content)),
            })
            n = ET.SubElement(pnode, "file_name")
            n.text = pfile.file_name
            c = ET.SubElement(pnode, "file_content")
            if content_encoding == "base64":
                c.set("encoding", "base64")
                c.text = base64.b64encode(pfile.content).decode("ascii")
            else:
                c.text = bytes_to_decimal_string(pfile.content)
        types_el = ET.SubElement(root, "icondata")
        for pfile in icon_files:
            icon = ET.SubElement(types_el, "userinterfaceicondata")
            ET.SubElement(icon, "image_name").text = pfile.image_name
            ET.SubElement(icon, "ovs").text = pfile._asset_package
        for node in self._other_types:
            types_el.append(deepcopy(node))
        tree = ET.ElementTree(root)
        # Pretty-print by manual newline/indent (ElementTree has limited pretty)
        indent_xml(root)
        tree.write(path, encoding="utf-8", xml_declaration=False)

    def add_or_replace(self, archive_path: str, content: bytes = b"",
                       *, asset_package: Optional[str] = None) -> bool:
        archive_path = normalize_archive_path(archive_path)
        if is_texture_sidecar(archive_path):
            return False
        existing = self.files.get(archive_path)
        if (is_png_asset(archive_path) or asset_package is not None
                or (existing is not None and existing.is_icondata)):
            if asset_package is None:
                asset_package = existing._asset_package if existing else None
            if not asset_package or not asset_package.strip():
                raise ValueError(f"Texture asset requires a .tex sidecar with an ovs value: {archive_path}")
            self.files[archive_path] = PPUIPKGFile(archive_path, b"", asset_package)
        else:
            self.files[archive_path] = PPUIPKGFile(archive_path, content)
        return True

    def import_file(self, source_path: str, archive_path: Optional[str] = None) -> bool:
        """Import bytes for normal files, or only ovs metadata for textures."""
        archive_path = normalize_archive_path(archive_path or os.path.basename(source_path))
        if is_texture_sidecar(source_path) or is_texture_sidecar(archive_path):
            return False
        if is_png_asset(source_path) and not is_png_asset(archive_path):
            raise ValueError("PNG assets must use a .png.png archive path")
        existing = self.files.get(archive_path)
        if (is_png_asset(archive_path)
                or (existing is not None and existing.is_icondata)
                or any(os.path.isfile(p) for p in texture_sidecar_paths(source_path))):
            if not os.path.isfile(source_path):
                raise FileNotFoundError(source_path)
            asset_package = read_image_asset_package(source_path)
            return self.add_or_replace(archive_path, asset_package=asset_package)
        with open(source_path, "rb") as f:
            return self.add_or_replace(archive_path, f.read())

    def remove(self, archive_path: str):
        archive_path = normalize_archive_path(archive_path)
        self.files.pop(archive_path, None)

    def rename(self, old_path: str, new_path: str):
        old_path = normalize_archive_path(old_path)
        new_path = normalize_archive_path(new_path)
        if old_path not in self.files:
            return
        pf = self.files[old_path]
        if is_texture_sidecar(new_path):
            raise ValueError(".tex sidecars cannot be added to a package")
        if pf.is_icondata:
            if is_png_asset(old_path):
                if not is_png_asset(new_path):
                    raise ValueError("PNG assets must keep the .png.png suffix")
            elif (is_png_asset(new_path)
                  or os.path.splitext(old_path)[1].lower() != os.path.splitext(new_path)[1].lower()):
                raise ValueError("Texture assets must keep their image extension")
        elif is_png_asset(new_path):
            raise ValueError("Import a PNG with its .tex sidecar to create an icon")
        pf = self.files.pop(old_path)
        pf.file_name = new_path
        self.files[new_path] = pf


def indent_xml(elem: ET.Element, level: int = 0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        for e in elem:
            indent_xml(e, level + 1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# ------------------------------
# Utilities
# ------------------------------

def normalize_archive_path(p: str) -> str:
    p = p.replace("\\", "/").strip("/")
    return p


def is_png_asset(path: str) -> bool:
    return path.lower().endswith(".png.png")


def is_texture_sidecar(path: str) -> bool:
    return path.lower().endswith(".tex")


def texture_sidecar_paths(source_path: str) -> List[str]:
    # Prefer the exact appended sidecar if both spellings exist.
    return [source_path + ".tex", os.path.splitext(source_path)[0] + ".tex"]


def read_image_asset_package(source_path: str) -> str:
    candidates = texture_sidecar_paths(source_path)
    for tex_path in candidates:
        if not os.path.isfile(tex_path):
            continue
        try:
            root = ET.parse(tex_path).getroot()
        except (ET.ParseError, OSError) as e:
            raise ValueError(f"Cannot read texture sidecar {tex_path}: {e}") from e
        asset_package = root.get("ovs")
        if not asset_package or not asset_package.strip():
            raise ValueError(f"Texture sidecar has no non-empty ovs attribute: {tex_path}")
        return asset_package
    raise ValueError(f"Texture sidecar not found for {source_path}; expected {candidates[0]} or {candidates[1]}")


def ensure_parent_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


# ------------------------------
# GUI
# ------------------------------

class FileTreeWidget(QtWidgets.QTreeWidget):
    """Tree that shows folders/files and supports drag-out and drop-in."""

    fileDropped = QtCore.pyqtSignal(list, str)  # [(src_path, rel_path)], drop_prefix

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.setHeaderHidden(False)
        self.setHeaderLabels(["Archive path"])
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self._temp_dir = tempfile.mkdtemp(prefix="ppuipkg_drag_")

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        try:
            shutil.rmtree(self._temp_dir, ignore_errors=True)
        except Exception:
            pass
        super().closeEvent(e)

    # -------- Drag out
    def startDrag(self, supportedActions):
        items = self.selectedItems()
        if not items:
            return
        urls = []
        for it in items:
            apath = it.data(0, QtCore.Qt.UserRole)
            if (not apath or apath.endswith("/")
                    or not it.data(0, QtCore.Qt.UserRole + 2)):
                # Only regular files may be written to the drag-out temp dir.
                continue
            # materialize temp file with full path under temp root
            temp_target = os.path.join(self._temp_dir, apath)
            ensure_parent_dir(temp_target)
            content: bytes = it.data(0, QtCore.Qt.UserRole + 1) or b""
            with open(temp_target, "wb") as f:
                f.write(content)
            urls.append(QtCore.QUrl.fromLocalFile(temp_target))
        if not urls:
            return
        mime = QtCore.QMimeData()
        mime.setUrls(urls)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime)
        drag.exec_(QtCore.Qt.CopyAction)

    # -------- Drop in
    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        pos = event.pos()
        target_item = self.itemAt(pos)
        prefix = ""
        if target_item is not None:
            data = target_item.data(0, QtCore.Qt.UserRole)
            if isinstance(data, str) and data.endswith("/"):
                prefix = data  # folder path with trailing /
            elif isinstance(data, str):
                # dropping on a file -> use its folder
                prefix = os.path.dirname(data) + "/" if "/" in data else ""
        urls = [u for u in event.mimeData().urls() if u.isLocalFile()]
        pairs = []
        for u in urls:
            src = u.toLocalFile()
            if os.path.isdir(src):
                # walk folder; rel paths from this folder
                base = src
                for root, _, files in os.walk(src):
                    for fn in files:
                        full = os.path.join(root, fn)
                        rel = os.path.relpath(full, base).replace("\\", "/")
                        pairs.append((full, rel))
            else:
                pairs.append((src, os.path.basename(src)))
        if pairs:
            self.fileDropped.emit(pairs, prefix)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PPUIPKG Explorer")
        self.resize(1000, 680)

        self.pkg = PPUIPKG()
        self.current_path: Optional[str] = None

        self.tree = FileTreeWidget()
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.on_context_menu)
        self.tree.fileDropped.connect(self.on_files_dropped)

        # Right pane: metadata editor
        meta_box = QtWidgets.QGroupBox("Package Metadata")
        form = QtWidgets.QFormLayout(meta_box)
        self.game_edit = QtWidgets.QLineEdit()
        self.basic_path_edit = QtWidgets.QLineEdit()
        self.content_encoding_combo = QtWidgets.QComboBox()
        self.content_encoding_combo.addItem("Base64", "base64")
        self.content_encoding_combo.addItem("Decimal (legacy)", "decimal")
        self.content_encoding_combo.setToolTip("Saves default to Base64. Choose Decimal for older cobra-tools readers.")
        form.addRow("game:", self.game_edit)
        form.addRow("basic_path:", self.basic_path_edit)
        form.addRow("Content encoding:", self.content_encoding_combo)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(meta_box)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

        self._build_menu()
        self.statusBar().showMessage("Ready")

    # ----------------- Menu
    def _build_menu(self):
        mb = self.menuBar()
        filem = mb.addMenu("&File")
        open_act = filem.addAction("Open…")
        open_act.triggered.connect(self.action_open)
        save_act = filem.addAction("Save")
        save_act.triggered.connect(self.action_save)
        saveas_act = filem.addAction("Save As…")
        saveas_act.triggered.connect(self.action_save_as)
        filem.addSeparator()
        extract_all = filem.addAction("Extract All…")
        extract_all.triggered.connect(self.action_extract_all)
        import_all = filem.addAction("Import All From Folder…")
        import_all.triggered.connect(self.action_import_all)
        filem.addSeparator()
        exit_act = filem.addAction("Exit")
        exit_act.triggered.connect(self.close)

        editm = mb.addMenu("&Edit")
        new_file = editm.addAction("Add File…")
        new_file.triggered.connect(self.action_add_file)

    # ----------------- Context menu
    def on_context_menu(self, pos: QtCore.QPoint):
        item = self.tree.itemAt(pos)
        menu = QtWidgets.QMenu(self)
        export_act = menu.addAction("Export Selected…")
        export_act.triggered.connect(self.action_export_selected)
        replace_act = menu.addAction("Replace From File…")
        replace_act.triggered.connect(self.action_replace_selected)
        rename_act = menu.addAction("Rename…")
        rename_act.triggered.connect(self.action_rename_selected)
        remove_act = menu.addAction("Remove")
        remove_act.triggered.connect(self.action_remove_selected)
        menu.exec_(self.tree.viewport().mapToGlobal(pos))

    # ----------------- File ops
    def action_open(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open .ppuipkg", "", "PPUIPKG (*.ppuipkg);;XML (*.xml);;All files (*.*)")
        if not path:
            return
        try:
            pkg = PPUIPKG.load(path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Open failed", str(e))
            return
        self.pkg = pkg
        self.current_path = path
        self.game_edit.setText(pkg.game)
        self.basic_path_edit.setText(pkg.basic_path)
        self.content_encoding_combo.setCurrentIndex(0)
        self.rebuild_tree()
        self.statusBar().showMessage(f"Loaded {os.path.basename(path)}")

    def persist_metadata(self):
        self.pkg.game = self.game_edit.text()
        self.pkg.basic_path = self.basic_path_edit.text()

    def action_save(self):
        if not self.current_path:
            self.action_save_as()
            return
        try:
            self.persist_metadata()
            self.pkg.save(self.current_path, content_encoding=self.content_encoding_combo.currentData())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Save failed", str(e))
            return
        self.statusBar().showMessage(f"Saved to {self.current_path}")

    def action_save_as(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save .ppuipkg", self.current_path or "package.ppuipkg", "PPUIPKG (*.ppuipkg);;All files (*.*)")
        if not path:
            return
        self.current_path = path
        self.action_save()

    def action_extract_all(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Extract All to…")
        if not folder:
            return
        count = 0
        for name, pf in self.pkg.files.items():
            if not pf.is_extractable:
                continue
            target = os.path.join(folder, name)
            ensure_parent_dir(target)
            with open(target, "wb") as f:
                f.write(pf.content)
            count += 1
        QtWidgets.QMessageBox.information(self, "Extract All", f"Extracted {count} file(s) to:\n{folder}")

    def action_import_all(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Import All from folder (recursive)")
        if not folder:
            return
        pairs = []
        for root, _, files in os.walk(folder):
            for fn in files:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, folder).replace("\\", "/")
                pairs.append((full, rel))
        added = self.import_sources(pairs)
        QtWidgets.QMessageBox.information(self, "Import All", f"Imported/updated {added} entry/entries from:\n{folder}")

    def action_export_selected(self):
        items = self.tree.selectedItems()
        if not items:
            return
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Export selected to…")
        if not folder:
            return
        count = 0
        for it in items:
            apath = it.data(0, QtCore.Qt.UserRole)
            content = it.data(0, QtCore.Qt.UserRole + 1)
            if (isinstance(apath, str) and content is not None and not apath.endswith("/")
                    and it.data(0, QtCore.Qt.UserRole + 2)):
                target = os.path.join(folder, apath)
                ensure_parent_dir(target)
                with open(target, "wb") as f:
                    f.write(content)
                count += 1
        QtWidgets.QMessageBox.information(self, "Export Selected", f"Exported {count} file(s)")

    def action_replace_selected(self):
        items = [it for it in self.tree.selectedItems() if it.data(0, QtCore.Qt.UserRole) and not str(it.data(0, QtCore.Qt.UserRole)).endswith("/")]
        if not items:
            return
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose replacement file", "", "All files (*.*)")
        if not path:
            return
        paths = [it.data(0, QtCore.Qt.UserRole) for it in items]
        self.import_sources([(path, apath) for apath in paths], select_paths=paths)

    def action_remove_selected(self):
        items = self.tree.selectedItems()
        if not items:
            return
        paths = [it.data(0, QtCore.Qt.UserRole) for it in items]
        for p in paths:
            if isinstance(p, str) and not p.endswith("/"):
                self.pkg.remove(p)
        self.rebuild_tree()

    def action_rename_selected(self):
        items = self.tree.selectedItems()
        if len(items) != 1:
            return
        it = items[0]
        apath = it.data(0, QtCore.Qt.UserRole)
        if not isinstance(apath, str) or apath.endswith("/"):
            return
        new, ok = QtWidgets.QInputDialog.getText(self, "Rename", "New archive path:", text=apath)
        if not ok or not new:
            return
        try:
            self.pkg.rename(apath, new)
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Rename failed", str(e))
            return
        self.rebuild_tree(select_paths=[normalize_archive_path(new)])

    def action_add_file(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Add file(s)")
        if not files:
            return
        # Ask for prefix (folder) once
        prefix, ok = QtWidgets.QInputDialog.getText(self, "Archive folder", "Optional archive folder prefix (e.g. UIGameface/img):", text="")
        if not ok:
            return
        if prefix:
            prefix = normalize_archive_path(prefix) + "/"
        added = self.import_sources([(p, os.path.basename(p)) for p in files], prefix)
        self.statusBar().showMessage(f"Added/updated {added} entries")

    def import_sources(self, pairs: List[Tuple[str, str]], prefix: str = "",
                       select_paths: Optional[List[str]] = None) -> int:
        """Use the same texture/sidecar rules for folder, add, replace and drop."""
        prefix = normalize_archive_path(prefix)
        if prefix:
            prefix += "/"
        added = 0
        errors = []
        for src, rel in pairs:
            apath = prefix + normalize_archive_path(rel)
            try:
                if self.pkg.import_file(src, apath):
                    added += 1
            except (OSError, ValueError) as e:
                errors.append(f"{apath}: {e}")
        self.rebuild_tree(select_paths=select_paths)
        if errors:
            QtWidgets.QMessageBox.warning(self, "Import incomplete",
                                         "Could not import the following entries:\n\n" + "\n\n".join(errors))
        return added

    # ----------------- Drop handling
    def on_files_dropped(self, pairs: List[Tuple[str, str]], prefix: str):
        added = self.import_sources(pairs, prefix)
        self.statusBar().showMessage(f"Imported/updated {added} entries")

    # ----------------- Tree building
    def rebuild_tree(self, select_paths: Optional[List[str]] = None):
        self.tree.clear()
        # Build folder hierarchy
        root_map: Dict[str, QtWidgets.QTreeWidgetItem] = {}

        def get_folder_node(path_parts: List[str]) -> QtWidgets.QTreeWidgetItem:
            key = "/".join(path_parts) + "/" if path_parts else ""  # folder key ends with /
            if key in root_map:
                return root_map[key]
            if not path_parts:
                # root invisible
                node = self.tree.invisibleRootItem()
                root_map[key] = node
                return node
            parent = get_folder_node(path_parts[:-1])
            node = QtWidgets.QTreeWidgetItem([path_parts[-1] + "/"])
            node.setData(0, QtCore.Qt.UserRole, key)
            node.setIcon(0, self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
            parent.addChild(node)
            root_map[key] = node
            return node

        for apath, pf in sorted(self.pkg.files.items()):
            parts = apath.split("/") if apath else []
            folder_parts, fname = parts[:-1], parts[-1] if parts else ([], apath)
            parent = get_folder_node(folder_parts)
            item = QtWidgets.QTreeWidgetItem([fname])
            item.setData(0, QtCore.Qt.UserRole, apath)
            item.setData(0, QtCore.Qt.UserRole + 1, pf.content)
            item.setData(0, QtCore.Qt.UserRole + 2, pf.is_extractable)
            if pf.is_icondata:
                item.setToolTip(0, f"userinterfaceicondata\nimage_name: {pf.image_name}\n"
                                   f"ovs: {pf._asset_package}\nTexture contents are not packaged or extracted.")
            item.setIcon(0, self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon))
            parent.addChild(item)

        self.tree.expandAll()
        # Restore selection
        if select_paths:
            to_select = set(select_paths)
            def walk(node):
                for i in range(node.childCount()):
                    ch = node.child(i)
                    ap = ch.data(0, QtCore.Qt.UserRole)
                    if ap in to_select:
                        ch.setSelected(True)
                    walk(ch)
            walk(self.tree.invisibleRootItem())


# ------------------------------
# App entry
# ------------------------------

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
