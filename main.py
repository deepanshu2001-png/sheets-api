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

def incremental_update_google_sheet(source_sheet_id, target_sheet_id):
    """
    Incrementally updates data from a source Google Sheet to a target Google Sheet.
    Updates existing rows based on unique IDs, appends new rows, and ignores deletions.

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

        # Fetch all data from both sheets
        source_data = source_sheet.get_all_values()
        target_data = target_sheet.get_all_values()

        # Ensure source data contains an ID column (starting from 1 if not present)
        if source_data:
            for index, row in enumerate(source_data, start=1):
                if len(row) == 0 or row[0] == "":
                    row.insert(0, str(index))  # Add an ID column if missing

        # Ensure target data contains an ID column
        if target_data:
            for index, row in enumerate(target_data, start=1):
                if len(row) == 0 or row[0] == "":
                    row.insert(0, str(index))  # Add an ID column if missing

        # Create dictionaries for fast lookup in both sheets (by ID)
        target_data_dict = {row[0]: (index, row) for index, row in enumerate(target_data, start=1)}
        source_data_dict = {row[0]: row for row in source_data}

        # Track rows to update or append
        processed_ids = set()

        # Iterate through source data to update or add rows
        for source_id, source_row in source_data_dict.items():
            if source_id in target_data_dict:
                # Update existing row if it has changed
                target_index, target_row = target_data_dict[source_id]
                if source_row != target_row:  # Check if row content differs
                    target_sheet.update(f"A{target_index}:Z{target_index}", [source_row])  # Update row in target sheet
                processed_ids.add(source_id)
            else:
                # Append new rows if the ID doesn't exist in the target sheet
                target_sheet.append_row(source_row)
                processed_ids.add(source_id)

        # Ignore deletions: Rows not in the source will remain in the target sheet
        print("Incremental update completed successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

        
if __name__ == "__main__":
    # Replace these with the actual sheet IDs
    SOURCE_SHEET_ID = "1zrDoTfEZkdm8_grWQ25MkzV2Ui1st9paCQZzvMigWhQ"
    TARGET_SHEET_ID = "1nK3ENa3ulcnu_VBC5zDzD29e6vlzB2JyMRLT3VKjVxc"

    incremental_update_google_sheet(SOURCE_SHEET_ID, TARGET_SHEET_ID)
