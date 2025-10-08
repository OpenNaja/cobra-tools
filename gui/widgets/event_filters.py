
from typing import Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QEvent)
from PyQt5.QtGui import (QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent)
from PyQt5.QtWidgets import (QWidget)


class MouseWheelGuard(QObject):
	"""An event filter that prevents widgets from being changed by the mouse
	wheel unless they have focus.

	This is particularly useful for `QComboBox` and `QSpinBox` widgets placed
	inside a `QScrollArea`, as it stops them from 'stealing' the scroll
	event from the parent. It works by intercepting wheel events and only
	allowing them to pass if the widget's focus policy is `WheelFocus`.
	"""

	def __init__(self, parent: Optional[QObject] = None) -> None:
		super().__init__(parent)

	def eventFilter(self, object: QObject, event: QEvent) -> bool:
		if isinstance(object, QWidget):
			if event.type() == QEvent.Type.Wheel:
				if object.focusPolicy() == Qt.FocusPolicy.WheelFocus:
					event.accept()
					return False
				else:
					event.ignore()
					return True
			if event.type() == QEvent.Type.FocusIn and object.focusPolicy() == Qt.FocusPolicy.StrongFocus:
				object.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
			if event.type() == QEvent.Type.FocusOut and object.focusPolicy() == Qt.FocusPolicy.WheelFocus:
				object.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

		return super().eventFilter(object, event)


class ClickGuard(QObject):
	"""A simple event filter that intercepts and blocks all mouse press events
	for a widget.

	This can be used to make a widget non-interactive to clicks while still
	allowing it to receive other events or display tooltips, providing an
	alternative to simply disabling it, or to allow a parent to handle the
	events instead.
	"""

	def __init__(self, parent: Optional[QObject] = None) -> None:
		super().__init__(parent)

	def eventFilter(self, object: QObject, event: QEvent) -> bool:
		if isinstance(object, QWidget):
			if event.type() == QEvent.Type.MouseButtonPress:
				event.ignore()
				return True

		return super().eventFilter(object, event)


class DragDropPassthrough(QObject):
	"""An event filter that forwards drag-and-drop events from a child widget
	to its parent.

	This is useful for creating composite widgets that should act as a single,
	unified drop target. By installing this filter on child components any
	drag or drop action performed over them will be handled by the parent
	widget's drag-and-drop event handlers.
	"""

	def __init__(self, parent: Optional[QObject] = None) -> None:
		super().__init__(parent)
		self.parent_widget = parent

	def eventFilter(self, object: QObject, event: QEvent) -> bool:
		if object.parent() == self.parent_widget and isinstance(self.parent_widget, QWidget):
			# Due to confusing inheritance between these QEvents, use type() for typing constraint
			# event.type() will not narrow the type for type checkers
			if type(event) is QDragMoveEvent:
				self.parent_widget.dragMoveEvent(event)
				return True
			elif type(event) is QDragEnterEvent:
				self.parent_widget.dragEnterEvent(event)
				return True
			elif type(event) is QDragLeaveEvent:
				self.parent_widget.dragLeaveEvent(event)
				return True
			elif type(event) is QDropEvent:
				self.parent_widget.dropEvent(event)
				return True

		return super().eventFilter(object, event)

