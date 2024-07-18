import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsPipeline:
    def __init__(self):
        # Use credentials to create a client to interact with the Google Drive API
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/credentials.json", scope)  # Adjust the path
        self.client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = self.client.open("Grant Scraping").sheet1

    def process_item(self, item, spider):
        # Extract the data from the item
        title = item.get('title', 'N/A')
        amount = item.get('amount', 'N/A')
        deadline = item.get('deadline', 'N/A')
        url = item.get('url', 'N/A')

        # Write the data to the next available row in the Google Sheet
        self.sheet.append_row([title, amount, deadline, url])

        return item
