import gspread
from oauth2client.service_account import ServiceAccountCredentials

def copy_google_sheet_data(source_sheet_id, target_sheet_id):
    """
    Copies data from one Google Sheet to another.

    Args:
        source_sheet_id (str): The ID of the source Google Sheet.
        target_sheet_id (str): The ID of the target Google Sheet.
    """
    try:
        # Authenticate and initialize the gspread client
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account_key.json', scope)
        client = gspread.authorize(credentials)

        # Open the source and target Google Sheets
        source_sheet = client.open_by_key(source_sheet_id).sheet1
        target_sheet = client.open_by_key(target_sheet_id).sheet1

        # Fetch all data from the source sheet
        data = source_sheet.get_all_values()

        # Clear the target sheet to ensure no stale data remains
        target_sheet.clear()

        # Write the data to the target sheet
        for row_index, row in enumerate(data):
            target_sheet.insert_row(row, row_index + 1)
        
        print("Data successfully copied from the source sheet to the target sheet.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace these with the actual sheet IDs
    SOURCE_SHEET_ID = "sourcesheet id"
    TARGET_SHEET_ID = "targetsheet id"

    copy_google_sheet_data(SOURCE_SHEET_ID, TARGET_SHEET_ID)
