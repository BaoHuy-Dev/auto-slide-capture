from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QRect, QPoint, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QKeyEvent, QMouseEvent

class OverlayWindow(QWidget):
    region_selected = Signal(int, int, int, int) # left, top, width, height
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Geometry covering all screens
        geometry = QRect()
        for screen in QApplication.screens():
            geometry = geometry.united(screen.geometry())
            
        self.setGeometry(geometry)
        self.setCursor(Qt.CrossCursor)
        
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_drawing = False
        self.selection_rect = QRect()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Semi-transparent dark background
        bg_color = QColor(0, 0, 0, 100)
        painter.fillRect(self.rect(), bg_color)
        
        if not self.selection_rect.isNull():
            # Clear the selected region
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(self.selection_rect, Qt.transparent)
            
            # Draw red border
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.start_point = event.globalPosition().toPoint()
            self.end_point = self.start_point
            self.is_drawing = True
            self.update_selection_rect()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_drawing:
            self.end_point = event.globalPosition().toPoint()
            self.update_selection_rect()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.is_drawing:
            self.end_point = event.globalPosition().toPoint()
            self.is_drawing = False
            self.update_selection_rect()

    def update_selection_rect(self):
        self.selection_rect = QRect(self.start_point, self.end_point).normalized()
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if not self.selection_rect.isNull() and self.selection_rect.width() > 0 and self.selection_rect.height() > 0:
                ratio = self.devicePixelRatio()
                self.region_selected.emit(
                    int(self.selection_rect.left() * ratio),
                    int(self.selection_rect.top() * ratio),
                    int(self.selection_rect.width() * ratio),
                    int(self.selection_rect.height() * ratio)
                )
            self.close()
