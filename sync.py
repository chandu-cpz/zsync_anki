from .upload import update_files_info, save_blob, upload_file
from .db import initializeDB, destroyDB
from .utils import import_apkg_file, export_deck_to_apkg
from datetime import datetime
from aqt import mw


def synchronize(deck_id):
    print("=========synchronizing..........========")
    deck_name = mw.col.decks.get(deck_id)["name"]
    con, cur = initializeDB()
    cur.execute(f"INSERT INTO decks VALUES({deck_id},'{deck_name}')")
    export_path = export_deck_to_apkg(deck_id)
    public_url = upload_file(export_path)
    cur.execute(
        f"INSERT INTO updatehistory VALUES({deck_id},{datetime.timestamp(datetime.now())})"
    )
    destroyDB(con)
    print(f"The deck has been uploaded to {public_url}")
    print("synchronize is finished")


def check_for_updates():
    print("=====Starting to check for new updates ========")
    # Check if there is a new deck if so download it and import it.
    update_files_info()
    con, cur = initializeDB()
    res = cur.execute(
        """select blob_name from checkupdate
where deck_id not in (select deck_id from decks)"""
    )
    res = res.fetchall()
    for row in res:
        print("Found a new deck with deck id:")
        print(row)
        save_blob(row[0])
        import_apkg_file(row[0])

    destroyDB(con)
    # See if there is a new update and download and import it.
    con, cur = initializeDB()
    res = cur.execute(
        """SELECT cu.blob_name
FROM updatehistory uh
INNER JOIN checkupdate cu ON uh.deck_id = cu.deck_id
WHERE uh.last_update < cu.last_update_on_server;
        """
    )
    for row in res.fetchall():
        print(row)
    destroyDB(con)
    print("Done Checking for updates")
    pass
