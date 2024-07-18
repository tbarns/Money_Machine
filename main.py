import json
import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from scrape_dynamic import scrape_dynamic
from grant_urls import grant_urls

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

def main():
    print(f"Current Directory: {os.getcwd()}")
    urls = grant_urls
    all_grants = []

    for url in urls:
        print(f"Scraping URL: {url}")
        scraped_data = scrape_dynamic(url)
        if scraped_data:
            all_grants.extend(scraped_data)

    print(f"Total grants scraped: {len(all_grants)}")

    if all_grants:
        range_name = 'Sheet1!A2:D'  # Adjust the range as needed
        write_to_sheet(sheets_service, spreadsheet_id, range_name, all_grants)
    else:
        print("No data scraped.")

if __name__ == "__main__":
    main()
