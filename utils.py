from aqt import mw
from anki.exporting import AnkiPackageExporter
import aqt
from anki.importing.apkg import AnkiPackageImporter
from anki.collection import Collection
from anki.collection import ImportAnkiPackageOptions, ImportAnkiPackageRequest
import os
from aqt.utils import showInfo


def get_decks() -> dict:
    """Function to return a dictionary of decks with key as id and value as name of deck"""
    decks = {}
    all_decks = mw.col.decks.all_names_and_ids()
    for deckNameId in all_decks:
        decks[deckNameId.id] = deckNameId.name
    return decks


def export_deck_to_apkg(deck_id):
    # Get the deck object
    print("Starting to export")
    deck = mw.col.decks.get(deck_id)
    print("The deck is: ", deck)

    # Create the exporter
    exporter = AnkiPackageExporter(mw.col)
    exporter.did = deck_id
    relative_export_path = f"user_files/{deck['name']}---{deck['id']}.apkg"
    print("The relative_export_path:", relative_export_path)
    # Set the export file path
    export_path = os.path.join(os.path.dirname(__file__), relative_export_path)

    try:
        # Export the deck to the .apkg file
        exporter.exportInto(export_path)
        showInfo(f"Deck has been exported to '{export_path}'")
        return relative_export_path
    except Exception as e:
        showInfo(f"Error exporting deck: {e}")


def import_apkg_file(apkg_file_path):
    """
    Import an Anki deck (.apkg file) programmatically.
    """
    print(
        "=================================START: TRYING TO IMPORT ",
        apkg_file_path,
        "==================================",
    )
    if aqt.mw.col == None:
        print("col is empty")
        collection_path = os.path.join(mw.pm.base, "User 1", "collection.anki2")
        print(f"Using the collection at path:{collection_path}")

        # Create a new Collection object
        col = Collection(collection_path)
    else:
        col = aqt.mw.col
    apkg_file_path = os.path.join(os.path.dirname(__file__), apkg_file_path)
    col.import_anki_package(
        ImportAnkiPackageRequest(
            package_path=apkg_file_path,
            options=ImportAnkiPackageOptions(
                with_scheduling=False, with_deck_configs=False
            ),
        )
    )
    col.save()
    # Reset the main window to reflect the changes
    aqt.mw.reset()
    # importer = AnkiPackageImporter(mw.col, apkg_file_path)
    # importer.run()
    print("Done importing package")
    print("====================================")
