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

    # Check progress
    url = f"https://{DATACENTER_ID}.qualtrics.com/API/v3/surveys/{SURVEY_ID}/export-responses/{progress_id}"
    headers = {"X-API-TOKEN": API_KEY}

    # Request data
    response = requests.get(url, headers=headers)

    # Return result dictionary giving fileId and progressId
    return response.json()['result']