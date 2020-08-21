import os
import pickle
import json

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = '1DQCxQlio2jkxKRCkgA3ftbSkfp-kZ07BcKDdVD-t9yI'
RANGE_NAME = 'Joueurs!A3:F82'


def connect():

    # The file token.pickle stores the user's access and refresh tokens,
    # and is created automatically chen the authorization flow completes for the first time

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "spreadsheet-credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def fetch_players(spreadsheet_id=SPREADSHEET_ID, spreadsheet_range=RANGE_NAME):
    creds = connect()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=spreadsheet_range
    ).execute()
    return result.get("values", [])


if __name__ == "__main__":

    connect()
    players = fetch_players()

    with open("players.json", "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4, ensure_ascii=False)