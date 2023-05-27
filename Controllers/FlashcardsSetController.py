from View.BasicTester.BasicFlashcardTester import BasicFlashcardTester
from View.BasicTester.BasicIncorrectWidget import IncorrectAnswer
from Database.DatabaseManager import DatabaseManager

class FlashcardsSetController:
    SET_ROLE = 100

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def set_flashcards_widget(self, flashcards_widget):
        self.flashcards_widget = flashcards_widget

    def get_available_sets(self):
        return self.db_manager.get_all_sets()

    def add_new_set(self, new_set_name, flashcards):
        self.db_manager.create_new_flashcards_set(new_set_name, flashcards)
        self.flashcards_widget.stacked_layout.setCurrentWidget(self.flashcards_widget.show_sets_widget)

    def show_set_details(self, flashcards_set):
        self.flashcards_widget.edit_sets_widget.load_set_for_edit(flashcards_set)
        self.flashcards_widget.stacked_layout.setCurrentWidget(self.flashcards_widget.edit_sets_widget)

    def return_from_set_editing(self):
        self.flashcards_widget.stacked_layout.setCurrentWidget(self.flashcards_widget.show_sets_widget)