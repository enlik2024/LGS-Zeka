import os
import toml
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuration
FOLDER_ID = "1xWDoQGIeC3In3zJZ2CcEcFPe5h_dI_Yp"
FILE_PATH = "assets/notebooklm_video.mp4"

def upload_video(file_path):
    print(f"Uploading {file_path} to Drive Folder {FOLDER_ID}...")
    
    # 1. Authenticate
    secrets = toml.load('.streamlit/secrets.toml')
    creds_dict = secrets['gcp_service_account']
    scoops = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scoops)
    service = build('drive', 'v3', credentials=creds)
    
    # 2. Upload
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink, webContentLink').execute()
    
    print(f"✅ Upload Complete!")
    print(f"File ID: {file.get('id')}")
    print(f"View Link: {file.get('webViewLink')}")
    print(f"Download Link: {file.get('webContentLink')}")
    
    # Update Supabase if needed (can be done here or separately)
    return file.get('webViewLink')

if __name__ == "__main__":
    # Check if file exists, if not, try to find it
    if not os.path.exists(FILE_PATH):
        # Fallback: Check current directory or user provided path
        print(f"❌ File not found at {FILE_PATH}")
        # Try to find mostly recent mp4
        # (This logic handled by manual check for now)
    else:
        upload_video(FILE_PATH)
