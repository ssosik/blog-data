from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import argparse
import csv
import os
import pdb
import sys

parser = argparse.ArgumentParser(description="Retry uploading failed CSV entries")
parser.add_argument("--file", "-f", help="Specify the file to source CSV rows from", required=True)
args = parser.parse_args()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'XXXXXX'
SHEET_RANGE = 'Environment Readings Upload!A1'

creds = None

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('sheets', 'v4', credentials=creds)

with open(args.file, "r") as f:
    lines = f.readlines()

with open(args.file, "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    for line in lines:
        row = line.strip().split(',')

        print(f"Publish row {row}")
        sys.stdout.flush()

        body = { 'values': [row] }

        try:
            result = service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=SHEET_RANGE,
                valueInputOption="USER_ENTERED",
                body=body,
            ).execute()

            updates = result.get('updates')
            if updates is not None and updates.get('updatedRows') == 1:
                # The good case, we updated a row, continue
                print("updated 1 Row")
                sys.stdout.flush()

            else:
                raise Exception(f"update not expected {result}")

        except Exception as e:
            # If we fall through here, the google update didn't succeed so write the CSV
            # Emit row to CSV
            print(f"Publish error {e}, keeping row on disk")
            sys.stdout.flush()
            writer.writerow(row)

