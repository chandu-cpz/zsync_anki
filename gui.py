# gui.py
from aqt import mw
from aqt.qt import QDialog, QVBoxLayout, QComboBox, QPushButton, QAction
from aqt.utils import showInfo
from aqt import qt
from .sync import synchronize
from .utils import get_decks, export_deck_to_apkg


class DeckSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a Deck")
        self.selected_deck_id = None

        layout = QVBoxLayout()

        # Create the dropdown
        self.deck_dropdown = QComboBox()
        self.deck_dict = get_decks()
        for deck_id, deck_name in self.deck_dict.items():
            self.deck_dropdown.addItem(deck_name, deck_id)
        layout.addWidget(self.deck_dropdown)

        # Create the "Sync" button
        self.sync_button = QPushButton("Sync")
        self.sync_button.clicked.connect(self.on_sync_clicked)
        layout.addWidget(self.sync_button)

        self.setLayout(layout)

        self.deck_dropdown.currentIndexChanged.connect(self.on_deck_selected)

    def on_deck_selected(self, index):
        print("The value of index is: ", index)
        if index >= 0:
            self.selected_deck_id = self.deck_dropdown.currentData()
            print(
                "The name of the selected deck is: ",
                self.deck_dict[self.selected_deck_id],
            )
        else:
            self.selected_deck_id = None

    def on_sync_clicked(self):
        if self.selected_deck_id is not None:
            # synchronization logic here
            print(f"Trying to sync deck with ID: {self.selected_deck_id}")
            synchronize(self.selected_deck_id)
            self.close()
        else:
            showInfo("Please select a deck to sync.")


def show_deck_selection_window():
    """Display a window for the user to select a deck to synchronize."""
    dialog = DeckSelectionDialog(parent=mw)
    dialog.exec()
