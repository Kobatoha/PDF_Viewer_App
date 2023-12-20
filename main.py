import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox, QScrollArea,\
    QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import fitz


class PDFViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 800, 900)

        self.label = QLabel()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.label)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)

        button_layout = QHBoxLayout()

        self.prev_button = QPushButton('Previous', self)
        button_layout.addWidget(self.prev_button)
        self.prev_button.setGeometry(10, 10, 130, 30)
        self.prev_button.clicked.connect(self.show_previous_page)

        self.next_button = QPushButton('Next', self)
        button_layout.addWidget(self.next_button)
        self.next_button.setGeometry(110, 10, 130, 30)
        self.next_button.clicked.connect(self.show_next_page)

        self.open_button = QPushButton('Open PDF', self)
        button_layout.addWidget(self.open_button)
        self.open_button.setGeometry(230, 10, 130, 30)
        self.open_button.clicked.connect(self.open_pdf)

        self.draw_button = QPushButton('Draw Rectangle', self)
        button_layout.addWidget(self.draw_button)
        self.draw_button.setGeometry(340, 10, 130, 30)
        self.draw_button.clicked.connect(self.draw_rectangle)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.page_number = 0
        self.doc = None
        self.pages_count = 0

    def open_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        try:
            if file_path:
                print(file_path)
                self.doc = fitz.open(file_path)
                self.pages_count = self.doc.page_count
                self.page_number = 0
                self.show_page()
        except:
            QMessageBox.warning(self, "Error", "Failed to open PDF file.", QMessageBox.Ok)

    def show_previous_page(self):
        if self.page_number > 0:
            self.page_number -= 1
            self.show_page()

    def show_next_page(self):
        if self.page_number < self.pages_count - 1:
            self.page_number += 1
            self.show_page()

    def show_page(self):
        page = self.doc.load_page(self.page_number)
        pixmap = page.get_pixmap()
        image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    def draw_rectangle(self):
        if self.doc is not None:
            page = self.doc.load_page(self.page_number)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(image))
            self.label.mousePressEvent = self.mouse_press_event
            self.label.mouseReleaseEvent = self.mouse_release_event

    def mouse_press_event(self, event):
        self.start_x = event.x()
        self.start_y = event.y()

    def mouse_release_event(self, event):
        end_x = event.x()
        end_y = event.y()
        painter = QPainter(self.label.pixmap())
        painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
        painter.drawRect(self.start_x, self.start_y, end_x - self.start_x, end_y - self.start_y)
        painter.end()
        self.label.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFViewerApp()
    window.show()
    sys.exit(app.exec_())
