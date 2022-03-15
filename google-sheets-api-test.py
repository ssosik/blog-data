# From https://developers.google.com/sheets/api/quickstart/python

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'XXXXXXXXX'
SAMPLE_RANGE_NAME = 'Sheet1!A1'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    values = [
        ( "10/10/2021 11:04:17PM",	"60.7",	"89.4",	"996.4" ),
        # Additional rows ...
    ]
    body = { 'values': values }
    result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range="Sheet4!A1:D",
        valueInputOption="USER_ENTERED", body=body).execute()
    print('{0} cells updated.'.format(result['updates']['updatedRows']))

    ## Call the Sheets API
    #sheet = service.spreadsheets()
    #result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
    #                            range=SAMPLE_RANGE_NAME).execute()
    #values = result.get('values', [])

    #if not values:
    #    print('No data found.')
    #else:
    #    print('Name, Major:')
    #    for row in values:
    #        # Print columns A and E, which correspond to indices 0 and 4.
    #        print('%s, %s' % (row[0], row[1]))

if __name__ == '__main__':
    main()
