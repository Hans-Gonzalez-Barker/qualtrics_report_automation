import io
import zipfile

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load necessary credentials from .env
API_KEY = os.getenv("QUALTRICS_API_TOKEN")
DATACENTER_ID = os.getenv("QUALTRICS_DATA_CENTER")
SURVEY_ID = os.getenv("QUALTRICS_SURVEY_ID")


# Get data from Qualtrics
def qualtrics_export():

    # Use an f-string to build the web address
    url = f"https://{DATACENTER_ID}.qualtrics.com/API/v3/surveys/{SURVEY_ID}/export-responses/"
    headers = {
        "X-API-TOKEN": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"format": "csv", "useLabels": True}

    # Execute post request
    response = requests.post(url, json=payload, headers=headers)

    # Return progressId from data
    return response.json()['result']['progressId']


# Poll if download is ready
def check_export_status(progress_id):

    # Get progress web address
    url = f"https://{DATACENTER_ID}.qualtrics.com/API/v3/surveys/{SURVEY_ID}/export-responses/{progress_id}"
    headers = {"X-API-TOKEN": API_KEY}

    # Request data
    response = requests.get(url, headers=headers)

    # Return result dictionary giving fileId and progressId
    return response.json()['result']

def download_qualtrics_file(file_id, export_dir="data"):

    # Get web address
    url = f"https://{DATACENTER_ID}.qualtrics.com/API/v3/surveys/{SURVEY_ID}/export-responses/{file_id}/file"
    headers = {"X-API-TOKEN": API_KEY}

    # Download the zipped data
    response = requests.get(url, headers=headers, stream=True)

    # Ensure data folder is created if not already
    os.makedirs(export_dir, exist_ok=True)

    # Open the ZIP in memory and extract it to the /data folder
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(export_dir)

    print(f"File extracted to the '{export_dir}' folder.")