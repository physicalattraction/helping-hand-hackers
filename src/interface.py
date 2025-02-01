import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap

class QuestionForm(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Red Cross Chatbot")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Image Label
        self.image_label = QLabel(self)
        pixmap = QPixmap("..//cross.png")  # Change to your image file
        self.image_label.setPixmap(pixmap.scaled(100, 100))  # Resize image
        layout.addWidget(self.image_label)

        # Question Label
        self.label = QLabel("What is your name?")
        
        layout.addWidget(self.label)

        # Input Field
        self.entry = QLineEdit(self)
        layout.addWidget(self.entry)

        # Submit Button
        self.button = QPushButton("Submit", self)
        self.button.clicked.connect(self.show_response)
        layout.addWidget(self.button)

        # Response Label
        self.response_label = QLabel("")
        layout.addWidget(self.response_label)

        # Set layout
        self.setLayout(layout)

    def show_response(self):
        question = self.entry.text()
        self.response_label.setText(f"You asked: {question}")

# Run the app
app = QApplication(sys.argv)
window = QuestionForm()
window.show()
sys.exit(app.exec())
