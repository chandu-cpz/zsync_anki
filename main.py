from aqt import mw
from aqt.utils import showInfo
import datetime
from .gui import show_deck_selection_window
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))


def start_addon() -> None:
    print("=============The Addon is Triggered=============")
    show_deck_selection_window()

    # Backup just for testing code:
    # cardCount = mw.col.cardCount()
    # showInfo("Card count: %d" % cardCount)
