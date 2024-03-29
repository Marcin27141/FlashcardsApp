from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt, Signal
from View.ViewUtilities import set_widget_font_size

class FlashcardsSetListTable(QTableWidget):     
    SHOW_SET_DETAILS_VIEW = Signal(object)
    COLUMNS_COUNT = 1

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.setColumnCount(self.COLUMNS_COUNT)
        self.setHorizontalHeaderLabels(["Created sets"])
        available_sets = controller.get_available_sets()
        self.populate_table(available_sets)
        self.itemClicked.connect(self.show_set_details)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionsMovable(False)
        self.horizontalHeader().setSectionsClickable(False)


        set_widget_font_size(self, 15)
        
    def populate_table(self, flashcards_sets):
        for row, _set in enumerate(flashcards_sets):
            self.insertRow(row)
            table_widget_item = QTableWidgetItem(_set.name)
            self.setItem(row, 0, table_widget_item)
            table_widget_item.setData(self.controller.SET_ROLE, _set)

    def show_set_details(self, item):
        flashcards_set = item.data(self.controller.SET_ROLE)
        self.SHOW_SET_DETAILS_VIEW.emit(flashcards_set)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected_rows = sorted(set(index.row() for index in self.selectedIndexes()), reverse=True)
            if selected_rows:
                result = QMessageBox.question(self, "Delete Sets", "Are you sure you want to delete selected sets?",
                                              QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    for row in selected_rows:
                        set_name = self.item(row, 0).text()
                        self.controller.remove_set_by_name(set_name)
                        self.removeRow(row)

    def showEvent(self, event):
        super().showEvent(event)
        self.clearContents()
        self.setRowCount(0)
        available_sets = self.controller.get_available_sets()
        self.populate_table(available_sets)

    