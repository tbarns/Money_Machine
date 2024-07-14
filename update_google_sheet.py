import json
import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def load_credentials(file_path):
    try:
        print(f"Loading credentials from {file_path}...")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r') as file:
            data = file.read()
            if data.strip() == "":
                raise ValueError("File is empty.")
            credentials = json.loads(data)
            if credentials.get('type') != 'service_account':
                raise ValueError(f"Unexpected credentials type: {credentials.get('type')}. Expected 'service_account'.")
            return credentials
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None

# Path to your credentials file
credentials_file = r'C:\Users\tbarn\MyProject\grants\credentials.json'
credentials = load_credentials(credentials_file)

if not credentials:
    print("Failed to load credentials.")
    exit(1)

# Define the scope and load the credentials
scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_info(credentials, scopes=scopes)

# Build the service
sheets_service = build('sheets', 'v4', credentials=creds)

# Use the ID of the shared Google Sheet
spreadsheet_id = '1YMbJBZqzuFDnMuvQV6WXoG0tA2Tmy-p2pKT83KaYzJw'

def write_to_sheet(service, spreadsheet_id, range_name, values):
    try:
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='RAW', body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
    except Exception as e:
        print(f"An error occurred while writing to the sheet: {e}")

# Example operation: Write data to the sheet
range_name = 'Sheet1!A1:D1'  # Adjust the range as needed
values = [
    ["Grant Name", "Amount", "Due Date", "Link"]
]

write_to_sheet(sheets_service, spreadsheet_id, range_name, values)
