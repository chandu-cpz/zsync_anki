import sqlite3
import os


def initializeDB():
    db_path = os.path.join(os.path.dirname(__file__), "user_files", "data.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # Create the `decks` table
    cur.execute(
        """CREATE TABLE IF NOT EXISTS decks
                 (deck_id INTEGER PRIMARY KEY,
                  deck_name TEXT)"""
    )

    # Create the `updateHistory` table
    cur.execute(
        """CREATE TABLE IF NOT EXISTS updatehistory
    ( deck_id INTEGER PRIMARY KEY,
                  last_update TIMESTAMP,
                  FOREIGN KEY (deck_id) REFERENCES decks(deck_id))"""
    )

    # Create `Check Updates` table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS checkupdate
        (deck_id INTEGER PRIMARY KEY,
            last_update_on_server TIMESTAMP,
            blob_name TEXT,
            FOREIGN KEY (deck_id) REFERENCES decks(deck_id))
    """
    )
    con.commit()
    return con, cur


def destroyDB(con):
    con.commit()
    con.close()
