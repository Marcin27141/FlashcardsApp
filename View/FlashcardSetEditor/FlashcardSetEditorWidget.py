from PySide6.QtWidgets import QWidget, QTableWidget, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from View.FlashcardSetEditor.FlashcardSetTable import FlashcardSetTable
from View.FlashcardSetEditor.NameWidget import NameWidget
from Flashcards import Flashcard
from View.ViewUtilities import set_widget_font_size

class FlashcardSetEditorWidget(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.name_widget = NameWidget()
        set_widget_font_size(self.name_widget, 15)

        self.table = FlashcardSetTable()
        
        self.add_button = QPushButton("Add Flashcard")
        self.add_button.clicked.connect(lambda: self.add_flashcard())

        self.continue_button = QPushButton("Continue")
        self.continue_button.clicked.connect(lambda: self.process_flashcards())

        layout = QVBoxLayout()
        layout.addWidget(self.name_widget)
        layout.addWidget(self.table)
        layout.addWidget(self.add_button)
        layout.addWidget(self.continue_button)
        self.setLayout(layout)

    def add_flashcard(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

    def get_flashcards_list(self):
        flashcards = []
        for row in range(self.table.rowCount()):
            original_item = self.table.item(row, 0)
            translation_item = self.table.item(row, 1)
            if original_item and translation_item:
                original_text = original_item.text()
                translation_text = translation_item.text()
                flashcards.append(Flashcard(original_text, translation_text))
        return flashcards

    def process_flashcards(self):
        new_set_name = self.name_widget.name_line_edit.text()
        self.controller.add_new_set(new_set_name, self.get_flashcards_list())