steps to run this script:

1.) obtain the credentials to use sheets api from google cloud platform by creating a new project and enabling and configuring the credentials in json file

2.) rename it to 'service_account_json' and put in the same folder of the script

3.) make two source and target spreadsheets and copy the id (The sheet ID is the string in the URL between /d/ and /edit (e.g., https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit)) and paste these values in SOURCE_SHEET_ID AND TARGET_SHEET_ID in the main.py script

4.) run the script  - python main.py