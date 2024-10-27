import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextBrowser, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from fuzzywuzzy import fuzz
import spacy
import random
import re
import json

nlp = spacy.load('en_core_web_sm')

class ChatBotGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.load_intents()

    def init_ui(self):
        self.setWindowTitle('ChatBot')
        self.setGeometry(100, 100, 800, 600)

        self.conversation_text = QTextBrowser(self)
        self.conversation_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText('Posez une question...')
        self.message_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.message_input.returnPressed.connect(self.send_message)

        self.send_button = QPushButton('Envoyer', self)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.addWidget(self.conversation_text)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

    def load_intents(self):
        with open('D://projetchatbot//Nouveau dossier//intents2.0.json') as f:
            self.intents = json.load(f)

    @pyqtSlot()
    def send_message(self):
        user_input = self.message_input.text()
        self.conversation_text.append(f'<img src="D://projetchatbot//Nouveau dossier//tr.jpg" width="80" height="80"> {user_input}')

        response = self.generate_response(user_input)

        self.conversation_text.append(f'<img src="D://projetchatbot//Nouveau dossier//OIP.jpg" width="80" height="80">{response}')
        self.message_input.clear()

    @pyqtSlot()
    def generate_response(self, user_input):
        processed_message = self.preprocess_message(user_input)
        highest_score = 0
        best_response = "Je suis désolé, je ne suis pas sûr de comprendre."

        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                if re.search(pattern, processed_message, re.IGNORECASE):
                    return random.choice(intent['responses'])
                else:
                    score = fuzz.ratio(pattern.lower(), user_input.lower())
                    if score > highest_score:
                        highest_score = score
                        best_response = random.choice(intent['responses'])

        return best_response

    def preprocess_message(self, message):
        message = message.lower()
        message = ' '.join(message.split())
        message = re.sub(r'[^\w\s]', '', message)
        doc = nlp(message)
        lemmatized_tokens = [token.lemma_ for token in doc]
        processed_message = ' '.join(lemmatized_tokens)
        return processed_message


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatbot_gui = ChatBotGUI()
    chatbot_gui.show()
    sys.exit(app.exec_())
