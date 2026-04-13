import time
import glob
import os
from dotenv import load_dotenv
from api_handler import qualtrics_export, check_export_status, download_qualtrics_file
from data_processing import load_and_clean_data, get_workshop_metrics
from visualizer import create_bar_chart
from report_generator import generate_pdf_report

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

        # Defensive check: Skip null values (NaN) to prevent processing incomplete survey responses
        # and avoid errors during PDF generation.
        if os.environ.get("PANDAS_IS_NA", False) or str(workshop) == 'nan': continue

        print(f"Generating report for: {workshop}")
        # Calculate metrics and get text
        averages, enjoy, change = get_workshop_metrics(df, workshop)
        # Create visual
        chart_file = create_bar_chart(averages, workshop)
        # Create PDF
        report_file = generate_pdf_report(workshop, chart_file, enjoy, change)

        print(f"Saved: {report_file}")

if __name__ == "__main__":
    main()