import toml
from google.oauth2 import service_account
from googleapiclient.discovery import build

FOLDER_ID = "1xWDoQGIeC3In3zJZ2CcEcFPe5h_dI_Yp"

def list_files():
    print(f"Listing files in Drive Folder {FOLDER_ID}...")
    
    secrets = toml.load('.streamlit/secrets.toml')
    creds_dict = secrets['gcp_service_account']
    scoops = ['https://www.googleapis.com/auth/drive.readonly']
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scoops)
    service = build('drive', 'v3', credentials=creds)
    
    results = service.files().list(
        q=f"'{FOLDER_ID}' in parents and trashed = false",
        fields="nextPageToken, files(id, name, webViewLink, webContentLink)"
    ).execute()
    
    files = results.get('files', [])
    
    if not files:
        print("No files found.")
    else:
        print("Files:")
        for file in files:
            print(f"Name: {file['name']}")
            print(f"ID: {file['id']}")
            print(f"View: {file['webViewLink']}")
            print(f"Download: {file['webContentLink']}")
            print("-" * 20)

if __name__ == "__main__":
    list_files()
