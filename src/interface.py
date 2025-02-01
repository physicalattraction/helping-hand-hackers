import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea, QFrame, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Red Cross Chatbot")
        self.setGeometry(100, 100, 1100, 600)
        pixmap = QPixmap("cross.jpg")  # Replace with your image

        # Main layout
        main_layout = QVBoxLayout()

        # Profile Picture (Optional)
        self.image_label = QLabel(self)
        pixmap = QPixmap("cross.jpg")  # Replace with your image
        pixmap = pixmap.scaled(50, 50)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)

        # Scrollable Chat Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_widget.setLayout(self.chat_layout)

        self.scroll_area.setWidget(self.chat_widget)
        main_layout.addWidget(self.scroll_area)

        # Input field and send button
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type a message...")
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)

        # Set main layout
        self.setLayout(main_layout)

    def send_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.add_message(user_message, "user")
            self.input_field.clear()

            # Simulate AI response (replace this with real AI logic)
            ai_response = self.generate_ai_response(user_message)
            self.add_message(ai_response, "ai")

            # Auto-scroll
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def add_message(self, text, sender):
        """Adds a chat message to the interface, adjusting size based on content."""
        message_frame = QFrame()
        message_layout = QHBoxLayout()

        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        message_label.setStyleSheet("padding: 10px; border-radius: 8px;")

        if sender == "user":
            message_label.setStyleSheet("background-color:rgb(157, 159, 155); padding: 10px; border-radius: 8px;")
            message_layout.addStretch()
            message_layout.addWidget(message_label)
        else:
            message_label.setStyleSheet("background-color:rgb(181, 181, 193); padding: 10px; border-radius: 8px;")
            message_layout.addWidget(message_label)
            message_layout.addStretch()
            

        message_frame.setLayout(message_layout)
        self.chat_layout.addWidget(message_frame)

    def generate_ai_response(self, user_input):
        """Simulates an AI response."""
        responses = {
            "hello": "Hi there! How can I assist you?",
            "how are you": "I'm just a chatbot, but I'm here to help!",
            "bye": "Goodbye! Have a great day!",
        }
        return responses.get(user_input.lower(), "I'm not sure how to answer that. 🤖")

# Run the app
app = QApplication(sys.argv)
window = ChatApp()
window.show()
sys.exit(app.exec())
