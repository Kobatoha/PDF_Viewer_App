import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox, QScrollArea,\
    QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
import fitz


class PDFViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 800, 900)

        self.label = QLabel(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.label)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.prev_button = QPushButton('Previous', self)
        self.prev_button.setGeometry(10, 830, 100, 30)
        self.prev_button.clicked.connect(self.show_previous_page)

        self.next_button = QPushButton('Next', self)
        self.next_button.setGeometry(120, 830, 100, 30)
        self.next_button.clicked.connect(self.show_next_page)

        self.open_button = QPushButton('Open PDF', self)
        self.open_button.setGeometry(230, 830, 100, 30)
        self.open_button.clicked.connect(self.open_pdf)

        self.draw_button = QPushButton('Draw Rectangle', self)
        self.draw_button.setGeometry(340, 830, 130, 30)
        self.draw_button.clicked.connect(self.draw_rectangle)

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
        print("Rectangle drawing functionality")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFViewerApp()
    window.show()
    sys.exit(app.exec_())
