import os
from firebase_admin import credentials, initialize_app, storage
from .db import initializeDB, destroyDB
from datetime import datetime
import firebase_admin
import json


def get_project_id():
    with open(os.path.join(os.path.dirname(__file__), "credentials.json"), "r") as f:
        creds = json.loads(f.read())
    return creds["project_id"]


def initialize_firebase() -> None:
    """Initialize the Firebase app with the provided credentials."""
    print("Initializing the firebase")
    try:
        # Check if the default app is already initialized
        firebase_admin.get_app()
    except ValueError:
        credentials_path = os.path.join(os.path.dirname(__file__), "credentials.json")
        cred = credentials.Certificate(credentials_path)
        initialize_app(cred, {"storageBucket": f"{get_project_id()}.appspot.com"})
    print("Done initializing firebase")


def upload_file(path: str):
    """Upload a local file to the Firebase Storage and return the public URL."""
    # Initialze the firebase
    try:
        print(f"Trying to uplaod file with path: {path}")
        initialize_firebase()
        bucket = storage.bucket()
        for blob in bucket.list_blobs():
            print(blob.name)
        blob = bucket.blob(path)
        path = os.path.join(os.path.dirname(__file__), path)
        blob.upload_from_filename(path)
        blob.make_public()
        print("Done uploading file ")
        return blob.public_url
    except Exception as e:
        print("Failed to upload file ")
        print(e)


def update_files_info():
    print("Trying to fetch details from firebase")
    initialize_firebase()
    con, cur = initializeDB()
    bucket = storage.bucket()
    files = []
    for blob in bucket.list_blobs():
        with open("logs.txt", "a") as f:
            f.write(str(blob))
        deck_id = blob.name.split("/")[-1].split("---")[-1].split(".apkg")[0]
        print(deck_id)
        cur.execute(
            f"INSERT OR REPLACE INTO checkupdate VALUES(?,?,?)",
            (int(deck_id), datetime.timestamp(blob.updated), blob.name),
        )
        files.append((blob.name, blob.updated))
    print(files)
    destroyDB(con)
    print("Done updating details from firebase")


def save_blob(blob_name):
    if blob_name == None:
        with open("logs.txt", "a") as f:
            f.write("The blob name is null")
    else:
        with open("logs.txt", "a") as f:
            f.write(f"The blob name that is asked to save is: {blob_name}")
    initialize_firebase()
    bucket = storage.bucket()
    blob = bucket.get_blob(blob_name)
    deck_id = blob_name.split("/")[-1].split("---")[-1].split(".apkg")[0]
    deck_name = blob_name.split("/")[-1].split("---")[0]
    with open("logs.txt", "a") as f:
        f.write(f"The saving deck is {deck_id},{deck_name}")
    con, cur = initializeDB()
    cur.execute(f"INSERT INTO decks VALUES({deck_id},'{deck_name}')")
    destroyDB(con)
    blob.download_to_filename(os.path.join(os.path.dirname(__file__), blob_name))
