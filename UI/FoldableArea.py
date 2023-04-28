from PySide6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QAbstractAnimation, Slot
from PySide6.QtWidgets import QWidget, QFrame

from UI.ui_FoldableArea import Ui_FoldableArea


class FoldableArea(QWidget):

    def __init__(self, master: QWidget, title: str, animation_duration: int):
        """
        References:
            # Adapted from c++ version
            http://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
        """
        super().__init__(master)
        self.ui = Ui_FoldableArea()
        self.ui.setupUi(self)

        self.animation_duration = animation_duration
        self.reveal_animation = QParallelAnimationGroup()
        self.collapse_animation = QParallelAnimationGroup()
        self.setup_toggle_button(title)
        self.setup_header_line()
        self.setup_animation()

        # start out collapsed
        self.ui.content_area.setMaximumHeight(0)
        self.ui.content_area.setMinimumHeight(0)

        self.ui.toggle_button.clicked.connect(self.toggle)
        self.set_animation(0)

    def setup_toggle_button(self, title: str):
        self.ui.toggle_button.setText(title)
        self.ui.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.ui.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.ui.toggle_button.setArrowType(Qt.RightArrow)
        self.ui.toggle_button.setCheckable(True)
        self.ui.toggle_button.setChecked(False)

    def setup_header_line(self):
        self.ui.header_line.setFrameShape(QFrame.Shape.HLine)
        self.ui.header_line.setFrameShadow(QFrame.Shadow.Sunken)

    def setup_animation(self):
        self.reveal_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.reveal_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.reveal_animation.addAnimation(QPropertyAnimation(self.ui.content_area, b"maximumHeight"))

        self.collapse_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.collapse_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.collapse_animation.addAnimation(QPropertyAnimation(self.ui.content_area, b"maximumHeight"))

    @Slot()
    def toggle(self):
        checked = self.ui.toggle_button.isChecked()
        arrow_type = Qt.DownArrow if checked else Qt.RightArrow
        self.ui.toggle_button.setArrowType(arrow_type)
        if checked:
            self.reveal_animation.start()
        else:
            self.collapse_animation.start()

    def set_content_layout(self, layout):
        # Not sure if this is equivalent to self.contentArea.destroy()
        self.ui.content_area.setLayout(layout)
        self.set_animation(layout.sizeHint().height())

    def set_animation(self, content_height):
        collapsed_height = self.sizeHint().height() - self.ui.content_area.maximumHeight()

        for i in range(self.reveal_animation.animationCount() - 1):
            spoiler_animation = self.reveal_animation.animationAt(i)
            spoiler_animation.setDuration(self.animation_duration)
            spoiler_animation.setStartValue(collapsed_height)
            spoiler_animation.setEndValue(collapsed_height + content_height)
        content_animation = self.reveal_animation.animationAt(self.reveal_animation.animationCount() - 1)
        content_animation.setDuration(self.animation_duration)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

        for i in range(self.collapse_animation.animationCount() - 1):
            spoiler_animation = self.collapse_animation.animationAt(i)
            spoiler_animation.setDuration(self.animation_duration)
            spoiler_animation.setStartValue(collapsed_height + content_height)
            spoiler_animation.setEndValue(collapsed_height)
        content_animation = self.collapse_animation.animationAt(self.collapse_animation.animationCount() - 1)
        content_animation.setDuration(self.animation_duration)
        content_animation.setStartValue(content_height)
        content_animation.setEndValue(0)
