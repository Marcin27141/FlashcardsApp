from PySide6.QtWidgets import QWidget, QStackedLayout, QWidget
from PySide6.QtCore import Qt, Signal
from Controllers.SerializeController import SerializeController
from Controllers.FlashcardsSetController import FlashcardsSetController
from View.BasicTester.BasicFlashcardTesterSwitch import BasicFlashcardTesterSwitch
from View.StatsTester.StatsResultWidget import StatsResultWidget
from View.StatsTester.StatsIncorrectWidget import StatsIncorrectWidget
from View.StatsTester.StatsTestWidget import StatsTestWidget
from View.StatsTester.SerializerTest import SerializerTest


class StatsFlashcardTester(BasicFlashcardTesterSwitch):
    CONTINUE_THE_TEST = Signal()

    def __init__(self) -> None:
        #test_widget = StatsTestWidget()
        flashcards_controller = FlashcardsSetController()
        serialize_controller = SerializeController()
        test_widget = SerializerTest(flashcards_controller, serialize_controller)
        mistake_widget = StatsIncorrectWidget()
        result_widget = StatsResultWidget()
        result_widget.CONTINUE_THE_TEST.connect(lambda incorrect: self.continue_the_test(incorrect))
        super().__init__(test_widget, mistake_widget, result_widget)

    def show_test_summary(self, test_results):
        self.result_widget.present_results(test_results)
        #self.incorrect = incorrect if len(incorrect) > 0 else self.test_widget.set_flashcards(self.original_flashcards)
        self.stacked_layout.setCurrentWidget(self.result_widget)
        self.test_widget.setEnabled(False)

    def continue_the_test(self, incorrect):
        self.test_widget.set_flashcards(incorrect)
        self.test_widget.reset()
        self.stacked_layout.setCurrentWidget(self.test_widget)
        self.test_widget.setEnabled(True)

    def load_test_state(self, serialized):
        self.test_widget.load_test(serialized)
        