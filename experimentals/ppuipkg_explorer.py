#!/usr/bin/env python3
"""
PPUIPKG Explorer (PyQt5)

A single-file GUI tool to view, extract, import, drag-and-drop, and edit
`.ppuipkg` packages used by Jurassic World Evolution 3 UI mods.

Features
- Open/Save .ppuipkg files (custom XML-like format shown by the user)
- View a virtual folder tree of file_name entries
- Drag files OUT to the OS (materializes temp files with full in-archive path)
- Drag files IN from the OS (drop onto a folder or root to add/replace)
- Extract All to folder (recreates full paths)
- Import All from folder (recursive; paths relative to chosen folder)
- Edit `game` and `basic_path` fields; changes are saved
- Context menu: Export Selected, Remove, Rename (in-archive path), Replace From File

Notes & assumptions
- The package format has a root element PPUIPKGRoot with attributes
  file_count, icondata_count, game; a <basic_path> element; a <files> list of
  <ppuipkgfile> with <file_name> and <file_content> (space-separated decimals).
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
import os
import sys
import tempfile
import shutil
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
    parts = s.split()
    try:
        return bytes(int(p) & 0xFF for p in parts)
    except ValueError as e:
        raise ValueError(f"Invalid decimal byte in content: {e}")


@dataclass
class PPUIPKGFile:
    file_name: str
    content: bytes


@dataclass
class PPUIPKG:
    game: str = ""
    basic_path: str = ""
    files: Dict[str, PPUIPKGFile] = field(default_factory=dict)

    @staticmethod
    def load(path: str) -> "PPUIPKG":
        tree = ET.parse(path)
        root = tree.getroot()
        if root.tag != "PPUIPKGRoot":
            raise ValueError("Not a PPUIPKGRoot document")
        game = root.attrib.get("game", "")
        basic_path_el = root.find("basic_path")
        basic_path = basic_path_el.text if basic_path_el is not None else ""
        files_el = root.find("files")
        files: Dict[str, PPUIPKGFile] = {}
        if files_el is not None:
            for f in files_el.findall("ppuipkgfile"):
                name_el = f.find("file_name")
                cont_el = f.find("file_content")
                if name_el is None or cont_el is None:
                    continue
                name = name_el.text or ""
                content = decimal_string_to_bytes(cont_el.text or "")
                files[name] = PPUIPKGFile(name, content)
        pkg = PPUIPKG(game=game, basic_path=basic_path, files=files)
        return pkg

    def save(self, path: str) -> None:
        root = ET.Element("PPUIPKGRoot", attrib={
            "file_count": str(len(self.files)),
            "icondata_count": "0",
            "game": self.game,
        })
        basic = ET.SubElement(root, "basic_path")
        basic.text = self.basic_path
        files_el = ET.SubElement(root, "files")
        # Deterministic order
        for name in sorted(self.files.keys()):
            pfile = self.files[name]
            pnode = ET.SubElement(files_el, "ppuipkgfile", attrib={
                "file_size": str(len(pfile.content)),
            })
            n = ET.SubElement(pnode, "file_name")
            n.text = pfile.file_name
            c = ET.SubElement(pnode, "file_content")
            c.text = bytes_to_decimal_string(pfile.content)
        ET.SubElement(root, "types")  # present but empty
        tree = ET.ElementTree(root)
        # Pretty-print by manual newline/indent (ElementTree has limited pretty)
        indent_xml(root)
        tree.write(path, encoding="utf-8", xml_declaration=False)

    def add_or_replace(self, archive_path: str, content: bytes):
        archive_path = normalize_archive_path(archive_path)
        self.files[archive_path] = PPUIPKGFile(archive_path, content)

    def remove(self, archive_path: str):
        archive_path = normalize_archive_path(archive_path)
        self.files.pop(archive_path, None)

    def rename(self, old_path: str, new_path: str):
        old_path = normalize_archive_path(old_path)
        new_path = normalize_archive_path(new_path)
        if old_path not in self.files:
            return
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
            if not apath or apath.endswith("/"):
                # skip folders on drag out
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
        form.addRow("game:", self.game_edit)
        form.addRow("basic_path:", self.basic_path_edit)

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
            self.pkg.save(self.current_path)
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
        added = 0
        for root, _, files in os.walk(folder):
            for fn in files:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, folder).replace("\\", "/")
                with open(full, "rb") as f:
                    data = f.read()
                self.pkg.add_or_replace(rel, data)
                added += 1
        self.rebuild_tree()
        QtWidgets.QMessageBox.information(self, "Import All", f"Imported/updated {added} file(s) from:\n{folder}")

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
            if isinstance(apath, str) and content is not None and not apath.endswith("/"):
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
        with open(path, "rb") as f:
            new_bytes = f.read()
        for it in items:
            apath = it.data(0, QtCore.Qt.UserRole)
            self.pkg.add_or_replace(apath, new_bytes)
        self.rebuild_tree(select_paths=[it.data(0, QtCore.Qt.UserRole) for it in items])

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
        self.pkg.rename(apath, new)
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
        added = 0
        for p in files:
            with open(p, "rb") as f:
                data = f.read()
            rel = os.path.basename(p)
            self.pkg.add_or_replace(prefix + rel, data)
            added += 1
        self.rebuild_tree()
        self.statusBar().showMessage(f"Added {added} file(s)")

    # ----------------- Drop handling
    def on_files_dropped(self, pairs: List[Tuple[str, str]], prefix: str):
        prefix = normalize_archive_path(prefix)  # may be ""
        if prefix:
            if not prefix.endswith("/"):
                prefix += "/"
        for src, rel in pairs:
            with open(src, "rb") as f:
                data = f.read()
            apath = prefix + normalize_archive_path(rel)
            self.pkg.add_or_replace(apath, data)
        self.rebuild_tree()

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
