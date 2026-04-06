import time
import glob
import pandas as pd
from dotenv import load_dotenv
from api_handler import qualtrics_export, check_export_status, download_qualtrics_file
from data_processing import load_and_clean_data, get_workshop_metrics

load_dotenv()


def main():

    # --- DATA ACQUISITION ---
    # Begin data exportation from Qualtrics
    progress_id = qualtrics_export()
    print(f"Export started: {progress_id}")

    # Initialize variables for polling completion
    is_complete = False
    file_id = None

    print("Waiting for Qualtrics to process the file...")

    while not is_complete:

        # Check for update on progress
        status_response = check_export_status(progress_id)

        # Track and report percentage completion
        percent_done = status_response['percentComplete']
        print(f"Progress: {percent_done}%")

        # If complete, grab the final fieldId, update boolean
        if status_response['status'] == 'complete':
            file_id = status_response['fileId']
            is_complete = True
        else:
            # Else, wait 5 seconds
            time.sleep(5)

    # Signal completion
    print(f"File is ready. File ID: {file_id}")

    # Download and Unzip data
    download_qualtrics_file(file_id)



    # --- DATA PROCESSING ---
    # Get the CSV
    csv_files = glob.glob("data/*.csv")
    if not csv_files:
        # For testing purposes
        print("No CSV found in data folder.")
        return

    raw_csv = csv_files[0]
    df = load_and_clean_data(raw_csv)

    # Get list of unique workshops
    workshops = df['Workshop'].unique()

    for workshop in workshops:
        if pd.isna(workshop): continue

        print(f"Processing metrics for: {workshop}")

        # Calculate scores and grab comments for this specific workshop
        averages, enjoy_text, change_text = get_workshop_metrics(df, workshop)

    print("All data processed. Visualizing...")


if __name__ == "__main__":
    main()