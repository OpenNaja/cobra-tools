import sys
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QScrollArea, QAbstractScrollArea,
    QPushButton, QLabel, QGroupBox, QMainWindow
)
from PyQt5.QtCore import (
    QObject, QEvent, QPoint, QTimer, Qt, QRectF
)
from PyQt5.QtGui import QColor, QPainter, QBrush, QPainterPath, QKeyEvent

# Colors for Managed Layouts
MANAGED_L0_COLOR = QColor(15, 160, 255)   # Blue  🟦
MANAGED_L1_COLOR = QColor(255, 90, 110)   # Red   🟥
MANAGED_L2_COLOR = QColor(80, 200, 120)   # Green 🟩
MANAGED_COLORS = [MANAGED_L0_COLOR, MANAGED_L1_COLOR, MANAGED_L2_COLOR]
# Colors for Unmanaged Layouts
UNMANAGED_L0_COLOR = QColor(255, 0, 255)  # Magenta 🟪
UNMANAGED_L1_COLOR = QColor(255, 255, 0)  # Yellow  🟨
UNMANAGED_L2_COLOR = QColor(255, 165, 0)  # Orange  🟧
UNMANAGED_COLORS = [UNMANAGED_L0_COLOR, UNMANAGED_L1_COLOR, UNMANAGED_L2_COLOR]

# Brush Pattern for terminal widgets (buttons, labels, etc.)
TERMINAL_WIDGET_PATTERN = Qt.BrushStyle.Dense7Pattern

RESET_INTERVAL_MS = 200
# Opacity settings for layout visualization
BASE_ALPHA = 0        # The starting opacity for layer 0 (0-255)
ALPHA_PER_LAYER = 20  # How much opacity is added for each nested layer

class LayoutVisualizerState:
    """A simple class to hold the global state for the visualizer."""
    def __init__(self):
        self.active_layer_filter = 0  # 0 means show all layers
        self.show_unmanaged = True
        self.opaque_mode = True
        self.enabled = True 
        # A dictionary mapping a widget to its visualizer instance
        self.visualizer_map = {}

visualizer_state = LayoutVisualizerState()


class LayoutVisualizer(QObject):
    """
    An event filter to visualize Qt layouts by drawing colored overlays.
    """
    def __init__(self, parent=None, use_unmanaged_palette=False, base_layer=0):
        super().__init__(parent)
        self.current_pos = QPoint(-1, -1)
        self.use_unmanaged_palette = use_unmanaged_palette
        self.base_layer = base_layer # The starting depth for this visualizer instance
        self.reset_timer = QTimer(self)
        self.reset_timer.setInterval(RESET_INTERVAL_MS)
        self.reset_timer.timeout.connect(self._reset_highlight)

    def eventFilter(self, obj, event):
        if obj is not self.parent():
             return super().eventFilter(obj, event)

        event_type = event.type()
        
        if event_type in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseMove):
            self.current_pos = event.pos()
            obj.update() 
            self.reset_timer.start()

        elif event_type == QEvent.Type.Paint:
            if not visualizer_state.enabled:
                return False
            if obj.layout():
                painter = QPainter(obj)
                # Start drawing from the correct base layer for this instance
                self._draw_layout_recursive(painter, obj.layout(), self.base_layer)
                painter.end()
        return False

    def _reset_highlight(self):
        self.reset_timer.stop()
        if self.parent():
            self.current_pos = QPoint(-1, -1)
            self.parent().update()

    def _draw_layout_recursive(self, painter, layout, layer):
        if visualizer_state.active_layer_filter > 0 and layer < visualizer_state.active_layer_filter:
            return

        is_unmanaged_and_hidden = self.use_unmanaged_palette and not visualizer_state.show_unmanaged
        # Layer depth
        min_layer = max(0, visualizer_state.active_layer_filter)
        style_layer = layer - min_layer
        # Opaque Mode toggle
        current_alpha = 255 if visualizer_state.opaque_mode else BASE_ALPHA
        # Determine which color palette to use
        palette = UNMANAGED_COLORS if self.use_unmanaged_palette else MANAGED_COLORS
        # Cycle through the chosen palette
        current_color = palette[style_layer % len(palette)]

        if not is_unmanaged_and_hidden:
            layout_rect = layout.contentsRect().marginsAdded(layout.contentsMargins())
            background_path = QPainterPath()
            background_path.setFillRule(Qt.OddEvenFill)
            background_path.addRect(QRectF(layout_rect))
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() and not item.widget().layout():
                    background_path.addRect(QRectF(item.geometry()))

            if visualizer_state.opaque_mode:
                widget_being_painted = painter.device()
                bg_color = widget_being_painted.palette().color(widget_being_painted.backgroundRole())
                painter.fillPath(background_path, bg_color)

            is_under_mouse = layout_rect.contains(painter.transform().inverted()[0].map(self.current_pos))
            if not visualizer_state.opaque_mode:
                fill_alpha = min(255, current_alpha + (style_layer * ALPHA_PER_LAYER))
                fill_color = QColor(current_color)
                fill_color.setAlpha(fill_alpha)
                painter.fillPath(background_path, fill_color)
            
            if layer % 2 == 0:
                pattern = Qt.BrushStyle.BDiagPattern if self.use_unmanaged_palette else Qt.BrushStyle.FDiagPattern
            else:
                pattern = Qt.BrushStyle.FDiagPattern if self.use_unmanaged_palette else Qt.BrushStyle.BDiagPattern
            
            if is_under_mouse:
                pattern = Qt.BrushStyle.Dense1Pattern
            
            stripe_color = QColor(current_color)
            stripe_color.setAlpha(255)
            painter.fillPath(background_path, QBrush(stripe_color, pattern))
            painter.setPen(stripe_color)
            painter.drawRect(layout_rect)

        next_layer = layer + 1
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if not item: continue
            
            widget = item.widget() if hasattr(item, 'widget') else None
            child_layout = item.layout()
            if not child_layout and widget:
                child_layout = widget.layout()
            
            if child_layout:
                painter.save()
                painter.translate(item.geometry().topLeft())
                self._draw_layout_recursive(painter, child_layout, next_layer)
                painter.restore()
            elif widget and not is_unmanaged_and_hidden:
                widget_rect = item.geometry()

                if visualizer_state.opaque_mode:
                    widget_being_painted = painter.device()
                    bg_color = widget_being_painted.palette().color(widget_being_painted.backgroundRole())
                    painter.fillRect(widget_rect, bg_color)

                if not visualizer_state.opaque_mode:
                    fill_alpha = min(255, current_alpha + (style_layer * ALPHA_PER_LAYER))
                    fill_color = QColor(current_color)
                    fill_color.setAlpha(fill_alpha)
                    painter.fillRect(widget_rect, fill_color)
                
                stripe_color = QColor(current_color)
                stripe_color.setAlpha(255)
                painter.fillRect(widget_rect, QBrush(stripe_color, TERMINAL_WIDGET_PATTERN))
                painter.setPen(stripe_color)
                painter.drawRect(widget_rect)


def _recursive_install(widget: QWidget, is_managed: bool, depth: int):
    """
    Recursively installs a visualizer on any widget with a layout and correctly identifies unmanaged branches.
    """
    if not widget or widget in visualizer_state.visualizer_map:
        return

    # A widget with a layout is a new root for visualization. Install a visualizer on it.
    if widget.layout():
        visualizer = LayoutVisualizer(widget, use_unmanaged_palette=(not is_managed), base_layer=depth)
        widget.installEventFilter(visualizer)
        visualizer_state.visualizer_map[widget] = visualizer
        
        # This widget now defines a managed context for its direct layout children.
        # Its own children that are NOT in the layout are unmanaged.
        managed_children = {
            widget.layout().itemAt(i).widget()
            for i in range(widget.layout().count())
            if hasattr(widget.layout().itemAt(i), 'widget') and widget.layout().itemAt(i).widget()
        }

        for child in widget.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly):
            # If the child is in the layout, it's managed and its depth increases.
            if child in managed_children:
                _recursive_install(child, is_managed=True, depth=depth + 1)
            # If it's a child but not in the layout, it's an unmanaged tree.
            else:
                _recursive_install(child, is_managed=False, depth=0)  # Reset depth for new tree
    else:
        # This widget has no layout. Its children are part of the same tree type (managed/unmanaged)
        # as this widget, at the same depth.
        for child in widget.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly):
            _recursive_install(child, is_managed, depth)

    # Special handling for scroll areas, which are new paint roots.
    if isinstance(widget, QAbstractScrollArea) and hasattr(widget, 'widget') and widget.widget():
        # The content of a scroll area starts a new layout tree.
        # It inherits the managed status of the scroll area itself, but its depth resets to 0.
        _recursive_install(widget.widget(), is_managed, depth=0)


def install_layout_visualizer(main_window: QMainWindow):
    """
    Installs the LayoutVisualizer by recursively finding all layout roots.
    """
    visualizer_state.visualizer_map.clear()

    # The central widget is the root of the primary "managed" tree.
    central_widget = main_window.centralWidget()
    if central_widget:
        _recursive_install(central_widget, is_managed=True, depth=0)

    # Any other top-level children of the main window are roots of "unmanaged" trees.
    for child in main_window.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly):
        if child is not central_widget:
             _recursive_install(child, is_managed=False, depth=0)

    install_visualizer_shortcuts(main_window)


def install_visualizer_shortcuts(main_window: QMainWindow):
    """
    Installs key press shortcuts onto a QMainWindow to control the visualizer.
    """
    original_keyPressEvent = main_window.keyPressEvent

    logging.info("LAYOUT VIS SHORTCUTS:")
    logging.info("+/- to increase/decrease the minimum visible layer")
    logging.info("0 to toggle visibility")
    logging.info("U to toggle unmanaged layout visibility")
    logging.info("O to toggle opaque overlays")

    def new_keyPressEvent(event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_Plus or key == Qt.Key.Key_Equal:
            visualizer_state.active_layer_filter += 1
        elif key == Qt.Key.Key_Minus or key == Qt.Key.Key_Underscore:
            visualizer_state.active_layer_filter = max(0, visualizer_state.active_layer_filter - 1)
        elif key == Qt.Key.Key_U:
            visualizer_state.show_unmanaged = not visualizer_state.show_unmanaged
        elif key == Qt.Key.Key_O:
            visualizer_state.opaque_mode = not visualizer_state.opaque_mode
        elif key == Qt.Key_0:
            visualizer_state.enabled = not visualizer_state.enabled
        else:
            original_keyPressEvent(event)
            return

        layer_text = "All" if visualizer_state.active_layer_filter == 0 else str(visualizer_state.active_layer_filter)
        print(f"Layer Filter: {layer_text}, Show Unmanaged: {visualizer_state.show_unmanaged}")

        # Update all widgets that have a visualizer installed
        for widget in list(visualizer_state.visualizer_map.keys()):
            try:
                if widget and widget.parent():
                    widget.update()
            except RuntimeError: # Widget has been deleted
                del visualizer_state.visualizer_map[widget]

    main_window.keyPressEvent = new_keyPressEvent


class VisualizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Layout Visualizer")
        self.setGeometry(100, 100, 550, 600)
        self.create_widgets()

    def create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Layer 0 (Managed)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Layer 1 (Managed)
        original_ui_group = QGroupBox("Layer 1 Group")
        original_ui_layout = QGridLayout(original_ui_group)
        main_layout.addWidget(original_ui_group)

        # Layer 2 (Managed)
        nested_group = QGroupBox("Layer 2 Group")
        nested_layout = QVBoxLayout(nested_group)
        nested_layout.addWidget(QPushButton("Button A (L2)"))
        original_ui_layout.addWidget(nested_group, 0, 0)
        
        # A button that is a child of original_ui_group but NOT in its layout
        # This will be detected as an unmanaged branch.
        unmanaged_button = QPushButton("Unmanaged Child Button", original_ui_group)
        unmanaged_button.setGeometry(150, 50, 180, 30)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area) 

        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)
        
        # Layer 0 (of scroll area)
        scroll_layout = QVBoxLayout(scroll_content_widget)
        scroll_layout.addWidget(QLabel("Scroll Area Content (L0 Root)"))

        # Layer 1 (of scroll area)
        scroll_group_box = QGroupBox("Scroll Area Group (L1)")
        scroll_grid_layout = QGridLayout(scroll_group_box)
        scroll_grid_layout.addWidget(QPushButton("Button C (L1)"), 0, 0)
        scroll_layout.addWidget(scroll_group_box)
        
        for i in range(10):
            scroll_layout.addWidget(QLabel(f"Scroll Label {i+1}"))

        # Create an unmanaged "orphan" widget
        orphan_widget = QWidget(self)
        orphan_widget.setGeometry(350, 30, 180, 150)
        orphan_widget.setStyleSheet("background-color: #444; border: 1px solid yellow;")
        # Layer 0 (Unmanaged)
        orphan_layout = QVBoxLayout(orphan_widget)
        orphan_layout.addWidget(QLabel("Orphan Widget (Unmanaged L0)"))
        
        # Layer 1 (Unmanaged)
        nested_orphan_group = QGroupBox("Layer 1 Group (Unmanaged)")
        nested_orphan_layout = QVBoxLayout(nested_orphan_group)
        nested_orphan_layout.addWidget(QPushButton("Orphan Button (L1)"))
        orphan_layout.addWidget(nested_orphan_group)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example_window = VisualizerWindow()
    install_layout_visualizer(example_window)
    example_window.show()
    sys.exit(app.exec_())
