import sys
import os
from .config import ADDON_NAME

print(f"Trying to initialize the addon {ADDON_NAME}")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib/"))
print("Done inserting the libs into the sys path")


from aqt import mw
from .main import start_addon
from aqt.qt import *
from .sync import check_for_updates

# Create the menu dropdown on main window then Start checking for updates

# create a new menu item, based on addon name
action = QAction(ADDON_NAME, mw)
# set it to call start addon when it's clicked
qconnect(action.triggered, start_addon)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

check_for_updates()
