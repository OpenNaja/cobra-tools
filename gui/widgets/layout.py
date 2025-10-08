from collections import deque

from typing import Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QSize, QEvent, QTimer,
						  QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation,
						  QChildEvent, QMargins)
from PyQt5.QtGui import (QShowEvent, QResizeEvent)
from PyQt5.QtWidgets import (QWidget, QStyle, QLayoutItem,
							 QAction, QToolButton, QSpacerItem,
							 QFrame, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy,
							 QSplitter, QToolBar, QWidgetAction, QProxyStyle, QStyleOption)


def pack_in_box(*widgets, margins=(0, 0, 0, 0), layout=QtWidgets.QVBoxLayout):
	frame = QtWidgets.QWidget()
	box = layout()
	for w in widgets:
		box.addWidget(w)
	box.setContentsMargins(*margins)
	box.setSizeConstraint(layout.SizeConstraint.SetNoConstraint)
	frame.setLayout(box)
	return frame


class CollapsibleBox(QWidget):
	"""A widget that can be collapsed or expanded by clicking its title bar.

	This container consists of a title button and a content area. Clicking the
	button toggles the visibility of the content area with a smooth animation.
	To add content to the box, use the standard `setLayout()` method, which
	will place your layout and its widgets within the collapsible section.
	"""

	def __init__(self, title="", parent=None):
		super().__init__(parent)

		self.toggle_button = QToolButton(
			text=title, checkable=True, checked=False
		)
		self.toggle_button.setStyleSheet("QToolButton { border: none; }")
		self.toggle_button.setToolButtonStyle(
			Qt.ToolButtonStyle.ToolButtonTextBesideIcon
		)
		self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
		self.toggle_button.pressed.connect(self.on_pressed)

		self.toggle_animation = QParallelAnimationGroup(self)

		self.content_area = QScrollArea(
			maximumHeight=0, minimumHeight=0
		)
		self.content_area.setSizePolicy(
			QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
		)
		self.content_area.setFrameShape(QFrame.Shape.NoFrame)

		pack_in_box(
			self.toggle_button,
			self.content_area
		)

		self.toggle_animation.addAnimation(
			QPropertyAnimation(self, b"minimumHeight")
		)
		self.toggle_animation.addAnimation(
			QPropertyAnimation(self, b"maximumHeight")
		)
		self.toggle_animation.addAnimation(
			QPropertyAnimation(self.content_area, b"maximumHeight")
		)

	@pyqtSlot()
	def on_pressed(self):
		checked = self.toggle_button.isChecked()
		self.toggle_button.setArrowType(
			Qt.ArrowType.DownArrow if not checked else Qt.ArrowType.RightArrow
		)
		self.toggle_animation.setDirection(
			QAbstractAnimation.Direction.Forward
			if not checked
			else QAbstractAnimation.Direction.Backward
		)
		self.toggle_animation.start()

	def setLayout(self, layout):
		lay = self.content_area.layout()
		del lay
		self.content_area.setLayout(layout)
		collapsed_height = (
				self.sizeHint().height() - self.content_area.maximumHeight()
		)
		content_height = layout.sizeHint().height()
		for i in range(self.toggle_animation.animationCount()):
			animation = self.toggle_animation.animationAt(i)
			animation.setDuration(100)
			animation.setStartValue(collapsed_height)
			animation.setEndValue(collapsed_height + content_height)

		content_animation = self.toggle_animation.animationAt(
			self.toggle_animation.animationCount() - 1
		)
		content_animation.setDuration(100)
		content_animation.setStartValue(0)
		content_animation.setEndValue(content_height)


class FlowWidget(QWidget):
	"""A widget that implements a responsive, flowing horizontal layout.

	As the widget's width decreases, child widgets are progressively hidden
	from left to right. As the width increases, they reappear in the reverse
	order. This is useful for creating toolbars or button rows that adapt to
	narrow spaces.

	This widget must be used with a `FlowHLayout`. Widgets are added via the
	layout's `addWidget` method, which includes a `hide_index` parameter to
	control the order of disappearance. A `hide_index` of -1 makes a widget
	permanently visible.
	"""
	def __init__(self, parent: Optional[QWidget] = None) -> None:
		super().__init__(parent)
		self.widgets: deque[QWidget] = deque()           # Visible widgets
		self.widgets_overflow: deque[QWidget] = deque()  # Hidden widgets
		self.perm_widgets: deque[QWidget] = deque()      # Permanently visible widgets
		self.flow_spacers: deque[QLayoutItem] = deque()  # Spacer widgets
		# Dummy widget to pad non-consecutive hide indices
		self.dummy = QWidget()
		self.dummy.setMaximumWidth(0)
		self.dummy.setHidden(True)
		self.dummy.setObjectName("dummy")

	def add_flow_widget(self, obj: QWidget, hide_index: int) -> None:
		"""Sort children for flow"""
		if hide_index > -1 and hide_index < len(self.widgets):
			self.widgets.insert(hide_index, obj)
		elif hide_index > -1:
			# Handle non-consecutive hide indices
			for _ in range(0, hide_index - len(self.widgets)):
				self.widgets.append(self.dummy)
			self.widgets.append(obj)
		else:
			# Hide Index -1 is permanently visible
			self.perm_widgets.append(obj)

	def add_flow_item(self, obj: QLayoutItem) -> None:
		self.flow_spacers.append(obj)

	def remove_flow_widget(self, obj: QWidget) -> None:
		if obj in self.widgets:
			self.widgets.remove(obj)

	def remove_flow_item(self, obj: QLayoutItem) -> None:
		if obj in self.flow_spacers:
			self.flow_spacers.remove(obj)

	def do_flow_all(self, event: QResizeEvent, widgets: deque[QWidget]) -> None:
		for widget in widgets.copy():
			self.do_flow(event, widget)

	def do_flow(self, event: QResizeEvent, widget: QWidget) -> None:
		width = event.size().width()
		old_width = event.oldSize().width()
		growing = width >= old_width if old_width > -1 else False
		visible_count = 1 if widget.isVisible() else 0
		sibling_min_hint_width = 0
		spacer_width = 0
		total_width = 0
		spacing = self.layout().spacing()
		left_margin, _, right_margin, _ = self.layout().getContentsMargins()
		margins = left_margin + right_margin
		# Get spacer widths
		for spacer in self.flow_spacers:
			if isinstance(spacer, QSpacerItem) and spacer.sizeHint().width() > 0:
				spacer_width += spacer.sizeHint().width()
				visible_count += 1
		# Get sibling widget minimum widths
		for child in self.children():
			if isinstance(child, QWidget) and child != widget and child.isVisible():
				sibling_min_hint_width += child.minimumSizeHint().width()
				visible_count += 1
		# All visible widgets + spacing and margins
		total_width = widget.width() + sibling_min_hint_width + spacing * (visible_count - 1) + margins + spacer_width
		# Hide or show, and move the widget in or out of overflow
		if not growing and widget.isVisible() and width <= total_width:
			widget.hide()
			self.widgets_overflow.appendleft(self.widgets.popleft())
		elif growing and widget.isHidden() and total_width < width:
			widget.show()
			self.widgets.appendleft(self.widgets_overflow.popleft())

	def resizeEvent(self, event: QResizeEvent) -> None:
		"""Do flow on one or all widgets depending on oldSize() and growing/shrinking"""
		width = event.size().width()
		old_width = event.oldSize().width()
		if width < 0:
			return super().resizeEvent(event)
		growing = width >= old_width if old_width > -1 else False
		first_visible = self.widgets[0] if self.widgets else None
		first_hidden = self.widgets_overflow[0] if self.widgets_overflow else None
		current_item = first_visible if not growing else first_hidden
		if current_item:
			return self.do_flow(event, current_item) if old_width > -1 else self.do_flow_all(event, self.widgets)
		return super().resizeEvent(event)

	def compact_widgets(self) -> None:
		"""Remove any empty spots from non-consecutive hide indices"""
		for widget in self.widgets.copy():
			if widget.objectName() == "dummy":
				self.widgets.remove(self.dummy)

	def show(self) -> None:
		self.compact_widgets()  # Ensures always runs
		return super().show()

	def showEvent(self, event: QShowEvent) -> None:
		"""Send an initial QResizeEvent so that visibility is calculated on first show"""
		super().showEvent(event)
		self.resizeEvent(QResizeEvent(self.size(), QSize(-1, -1)))

	def sizeHint(self) -> QSize:
		"""Return the minimumSizeHint so that splitter/window resizing is not blocked"""
		return self.minimumSizeHint()

	def minimumSizeHint(self) -> QSize:
		"""Return the accumulated minimum widths of permanently visible widgets"""
		min_perm_width = 0
		for child in self.children():
			if isinstance(child, QWidget) and child in self.perm_widgets:
				min_perm_width += child.minimumSizeHint().width()
		min_size = super().minimumSizeHint()
		return QSize(min_perm_width, min_size.height())


class FlowHLayout(QHBoxLayout):
	"""Layout for FlowWidget. Must be passed a `parent` FlowWidget."""
	def __init__(self, parent: FlowWidget) -> None:
		super().__init__(parent)
		self.parent_flow = parent

	def addWidget(self, widget: QWidget, stretch: int = 0,
				  alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignVCenter,
				  hide_index: int = -1) -> None:
		self.parent_flow.add_flow_widget(widget, hide_index)
		return super().addWidget(widget, stretch, alignment)

	def addItem(self, item: QLayoutItem) -> None:
		self.parent_flow.add_flow_item(item)
		return super().addItem(item)

	def removeWidget(self, widget: QWidget) -> None:
		self.parent_flow.remove_flow_widget(widget)
		return super().removeWidget(widget)

	def removeItem(self, item: QLayoutItem) -> None:
		self.parent_flow.remove_flow_item(item)
		return super().removeItem(item)


ToolbarItem = Union[QAction, QWidget]


class ToolbarSpacingProxyStyle(QProxyStyle):
	"""
	A QProxyStyle that overrides the styling of toolbar widgets
	"""

	def __init__(self, base_style: QStyle | str | None=None):
		super().__init__(base_style)
		self._spacing = 10  # Default spacing

	def set_toolbar_spacing(self, spacing: int) -> None:
		"""Allows you to dynamically set the desired spacing."""
		self._spacing = spacing

	def pixelMetric(self, metric: QStyle.PixelMetric, option: QStyleOption | None=None,
					widget: QWidget | None=None) -> int:
		"""
		Custom pixel metric overrides
		"""
		if metric == QStyle.PixelMetric.PM_ToolBarItemSpacing:
			return self._spacing

		return super().pixelMetric(metric, option, widget)


class OrientationToolBar(QToolBar):
	"""
	A QToolBar that manages the visibility of its actions and widgets
	based on the toolbar's orientation.
	"""

	def __init__(self, title: str, parent: QWidget = None):
		super().__init__(title, parent)
		# This dictionary maps a QAction or QWidget to its visibility rule
		# The rule is a Qt.Orientations flag (e.g. Qt.Orientation.Horizontal)
		self._item_visibility: dict[ToolbarItem, Qt.Orientations] = {}
		# Store margins for each orientation, initializing with the current state.
		self._horizontal_margins = self.contentsMargins()
		self._vertical_margins = self.contentsMargins()

	def addOrientationAction(self, action: QAction, visibility: Qt.Orientations) -> None:
		"""
		Adds a QAction that will only be visible in the specified orientations.
		  Example: (Qt.Orientation.Horizontal | Qt.Orientation.Vertical)
		"""
		super().addAction(action)
		self._item_visibility[action] = visibility
		self._updateItemVisibility(action)

	def addOrientationWidget(self, widget: QWidget, visibility: Qt.Orientations) -> None:
		"""
		Adds a QWidget that will only be visible in the specified orientations.
		"""
		widget_action = super().addWidget(widget)
		#widget_action.setPriority(QAction.Priority.LowPriority)
		self._item_visibility[widget_action] = visibility
		self._updateItemVisibility(widget_action)

	def addOrientationSeparator(self, visibility: Qt.Orientations) -> QAction:
		"""
		Adds a separator that will only be visible in the specified orientations.
		"""
		separator_action = super().addSeparator()
		self._item_visibility[separator_action] = visibility
		self._updateItemVisibility(separator_action)
		return separator_action

	def setOrientation(self, orientation: Qt.Orientation) -> None:
		"""
		Overrides the parent method to apply custom visibility rules and to
		propagate the orientation change to any child that supports it.
		"""
		# Let the parent class handle its own orientation change first
		super().setOrientation(orientation)
		# Iterate through all managed items to find child widgets
		for item_action in self._item_visibility.keys():
			if isinstance(item_action, QWidgetAction):
				# Retrieve the actual widget from the widget action
				child_widget = item_action.defaultWidget()
				# Check if the widget has a 'setOrientation' method
				if child_widget and hasattr(child_widget, 'setOrientation'):
					child_widget.setOrientation(orientation)
		# Apply this toolbar's own visibility logic to its immediate items
		self._updateAllItemVisibility()
		# Apply the correct margins for the new orientation
		self._applyOrientationMargins()

	def setOrientationMargins(self,
							  horizontal: QMargins | None = None,
							  vertical: QMargins | None = None) -> None:
		"""
		Sets the content margins to be used for each orientation.
		"""
		if horizontal:
			self._horizontal_margins = horizontal
		if vertical:
			self._vertical_margins = vertical
		# Apply the correct margins immediately based on the current orientation
		self._applyOrientationMargins()

	def _applyOrientationMargins(self) -> None:
		"""
		Applies the stored margins based on the current orientation.
		"""
		if self.orientation() == Qt.Orientation.Horizontal:
			super().setContentsMargins(self._horizontal_margins)
		else:  # Qt.Orientation.Vertical
			super().setContentsMargins(self._vertical_margins)

	def setContentsMargins(self, *args, **kwargs) -> None:
		"""
		The margins should only be set via setOrientationMargins().
		"""
		pass


	def _updateAllItemVisibility(self) -> None:
		"""
		Iterates through all tracked items and sets their visibility based on the toolbar's
		current orientation.
		"""
		for item, visibility_rule in self._item_visibility.items():
			self._updateItemVisibility(item, visibility_rule)

	def _updateItemVisibility(self, item: ToolbarItem, visibility_rule: Qt.Orientations = None) -> None:
		"""
		Updates the visibility of a single item.
		"""
		if visibility_rule is None:
			visibility_rule = self._item_visibility.get(item)

		if not visibility_rule:
			return

		# Check if the item's visibility rule includes the current orientation
		is_visible = bool(self.orientation() & visibility_rule)
		item.setVisible(is_visible)

	def removeAction(self, action: QAction) -> None:
		"""
		Overrides removeAction to clean up the item from the tracking dictionary.
		"""
		if action in self._item_visibility:
			del self._item_visibility[action]
		super().removeAction(action)

	def childEvent(self, event: QChildEvent) -> None:
		"""
		Overrides childEvent to catch when a widget is removed from the toolbar,
		ensuring it's also removed from the tracking dictionary.
		"""
		if event.type() == QEvent.Type.ChildRemoved:
			child = event.child()
			if child in self._item_visibility:
				del self._item_visibility[child]
		super().childEvent(event)


class SnapCollapseWidget(QWidget):
	"""
	A widget that contains a toolbar and content, designed to be used within a SnapCollapseSplitter.

	When the widget's size shrinks below a certain threshold in its primary
	orientation, the content widget is hidden. For horizontal orientation,
	the toolbar also switches from being above the content to being vertical.
	"""
	snapped = pyqtSignal(bool)
	current_size = pyqtSignal(QSize)
	SNAP_THRESHOLD = 120

	def __init__(self, toolbar: QWidget=None, content: QWidget=None, orientation: Qt.Orientation=Qt.Orientation.Vertical,
				 threshold: int=SNAP_THRESHOLD, parent=None):
		super().__init__(parent)
		self._orientation = orientation
		self._toolbar = None
		self._content = None
		self._is_collapsed = False
		self._snap_threshold = threshold

		self._layout = QVBoxLayout(self)
		self._layout.setContentsMargins(0, 0, 0, 0)
		self._layout.setSpacing(0)
		self.setLayout(self._layout)

		if toolbar:
			self.set_toolbar(toolbar)
		if content:
			self.set_content(content)

	def set_toolbar(self, toolbar: QWidget):
		"""Sets or replaces the toolbar widget."""
		# Remove and delete the existing toolbar, if any
		if self._toolbar:
			self._layout.removeWidget(self._toolbar)
			self._toolbar.deleteLater()

		self._toolbar = toolbar
		if self._toolbar:
			# Insert at top
			self._layout.insertWidget(0, self._toolbar)

	def set_content(self, content: QWidget):
		"""Sets or replaces the content widget."""
		# Remove and delete the existing content, if any
		if self._content:
			self._layout.removeWidget(self._content)
			self._content.deleteLater()

		self._content = content
		if self._content:
			self._layout.addWidget(self._content)
			
			# Apply the size policy for collapsing
			if self._orientation == Qt.Orientation.Horizontal:
				self._content.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
			else:  # Vertical
				self._content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)

			# If the widget is already collapsed, hide the new content immediately
			if self.is_collapsed():
				self._content.hide()

	def is_collapsed(self) -> bool:
		return self._is_collapsed

	def resizeEvent(self, event):
		"""The core logic for snapping is handled on resize"""
		super().resizeEvent(event)
		current_size = (
			self.width() if self._orientation == Qt.Orientation.Horizontal else self.height()
		)
		# Emit the signal every time the resize happens and we are under the threshold.
		# This allows the parent splitter to continuously enforce the snap.
		if current_size < self._snap_threshold:
			if not self._is_collapsed:
				self.collapse()
			else:
				# If already collapsed, still emit the signal so the splitter can enforce the size.
				self.snapped.emit(True)
		elif self._is_collapsed:
			self.expand()
		self.current_size.emit(self.size())

	def collapse(self):
		"""Hides the content and updates the layout for the collapsed state."""
		self._is_collapsed = True
		self._content.hide()
		if self._orientation == Qt.Orientation.Horizontal and hasattr(self._toolbar, "setOrientation"):
			self._toolbar.setOrientation(Qt.Orientation.Vertical)

		self.snapped.emit(True)
		self.updateGeometry()

	def expand(self):
		"""Shows the content and restores the layout for the expanded state."""
		self._is_collapsed = False
		self._content.show()
		if self._orientation == Qt.Orientation.Horizontal and hasattr(self._toolbar, "setOrientation"):
			self._toolbar.setOrientation(Qt.Orientation.Horizontal)

		self.snapped.emit(False)
		self.updateGeometry()

	def minimumSizeHint(self) -> QSize:
		"""
		Calculates the minimum size hint for the parent QSplitter.
		"""
		if self._is_collapsed:
			return self._toolbar.minimumSizeHint()
		# When expanded, the layout is always QVBoxLayout.
		# Therefore, the minimum size is the max of the children's widths and the sum of their heights.
		toolbar_hint = self._toolbar.minimumSizeHint()
		content_hint = self._content.minimumSizeHint()
		
		w = max(toolbar_hint.width(), content_hint.width())
		h = toolbar_hint.height() + content_hint.height()
		return QSize(w, h)


class SnapCollapseSplitter(QSplitter):
	"""
	A QSplitter that properly handles SnapCollapseWidget children by actively
	enforcing their snapped (collapsed) state.
	"""
	def __init__(self, orientation: Qt.Orientation, parent: QWidget | None = None):
		super().__init__(orientation, parent)
		self._snap_widgets = {}

	def addWidget(self, widget: QWidget):
		"""
		Overrides addWidget to identify SnapCollapseWidgets and configure them.
		"""
		super().addWidget(widget)
		if isinstance(widget, SnapCollapseWidget):
			index = self.indexOf(widget)
			self._snap_widgets[index] = widget
			self.setCollapsible(index, False)
			widget.snapped.connect(self._on_child_snapped)

	def _on_child_snapped(self, is_collapsed: bool):
		"""
		When a child snaps collapsed, this slot enforces the splitter size,
		forcing the widget to its minimum and giving the extra space to another widget.
		"""
		if not is_collapsed:
			return

		sender_widget = self.sender()
		if not isinstance(sender_widget, SnapCollapseWidget):
			return

		index = self.indexOf(sender_widget)
		current_sizes = self.sizes()
		if len(current_sizes) < 2 or index == -1:
			return

		min_hint = sender_widget.minimumSizeHint()
		min_size = min_hint.width() if self.orientation() == Qt.Orientation.Horizontal else min_hint.height()
		# If the widget already has a size smaller or equal to its minimum, do nothing
		# This check is to prevent recursive loops
		if current_sizes[index] <= min_size:
			return

		# Calculate the space to reclaim from the collapsed widget
		delta = current_sizes[index] - min_size
		new_sizes = list(current_sizes)
		new_sizes[index] = min_size
		# Find the largest non-collapsed widget to give the extra space to
		largest_widget_index = -1
		max_size = -1
		for i, size in enumerate(new_sizes):
			if i == index:
				continue
			widget = self.widget(i)
			# Don't give space to other collapsed widgets
			if isinstance(widget, SnapCollapseWidget) and widget.is_collapsed():
				continue
			if size > max_size:
				max_size = size
				largest_widget_index = i
		
		if largest_widget_index != -1:
			new_sizes[largest_widget_index] += delta
		else:
			# Fallback: if all other widgets are collapsed, give it to the first neighbor
			if index > 0:
				new_sizes[index - 1] += delta
			else:
				new_sizes[index + 1] += delta

		# Use a zero-delay QTimer to apply the sizes. This breaks potential
		# recursive event loops where setSizes -> resizeEvent -> snapped -> _on_child_snapped.
		QTimer.singleShot(0, lambda: self.setSizes(new_sizes))
