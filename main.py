import time
from dotenv import load_dotenv
from api_handler import qualtrics_export, check_export_status

load_dotenv()


def main():

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


if __name__ == "__main__":
    main()