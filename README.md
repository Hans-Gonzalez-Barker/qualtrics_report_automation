# Qualtrics Automated Reporting

An **ETL** pipeline developed for the Ohio State MMC Digital Lab supervisor team to automate
the generation of 7 and 14-week workshops leader performance reports.

## Problem Statement
The MMC Digital Lab program manages multiple 7-week and 14-week workshops. 
Previously, generating feedback reports was a lengthy process of downloading,
editing, and ensuring accuracy of each workshop report from Qualtrics. This
had to be done each semester, for each workshop, which causes a bottleneck
in workshop completion and workshop ratings reports.

## Goals & Results
* **Speed:** Reduced processing time from **45-90 minutes to 10 seconds**.
* **Accuracy:** Eliminated 100% of manual transcription and editing potential fault-points.
* **Scalability:** Implemented batch processing to handle any number of workshops in a single execution.
* **Data Integrity:** Developed a robust sanitization layer to handle Unicode encoding errors.

## Tools
* **API/Backend:** `Requests`, `python-dotenv`
* **Visualization:** `Pandas`, `Matplotlib`
* **Reporting:** `FPDF2`
* **File Management:** `Zipfile`, `IO`, `Glob`

## Project Structure
```text
qualtrics_report_automation/
├── main.py              # Main orchestrator (Batch processing loop)
├── api_handler.py       # API connection and extraction logic
├── data_processing.py   # Pandas cleaning and metric calculation
├── visualizer.py        # Matplotlib chart generation
├── report_generator.py  # PDF assembly and text sanitization
├── .env                 # API credentials (GIT IGNORED)
├── data/                # Raw CSV storage (GIT IGNORED)
├── output/              # Temporary chart storage (GIT IGNORED)
└── reports/             # Final PDF reports (GIT IGNORED)
```

## Setup & Usage
* Clone the Repository:
```bash
   git clone https://github.com/Hans-Gonzalez-Barker/qualtrics_report_automation
```
* Install Dependencies:
```bash
   pip install -r requirements.txt
```
* Configure Environment Variables:
```bash
   Create a .env file with QUALTRICS_API_TOKEN, QUALTRICS_DATA_CENTER, 
   and QUALTRICS_SURVEY_ID.
   
   API token: Log into Qualtrics > Account Settings > API > Token
   Datacenter ID: Log into Qualtrics > Account Settings > User > Datacenter ID
   Survey ID: Look at your Qualtrics survey URL, should begin with /SV_ ...
```
* Run the Pipeline:
```bash
   python main.py
   
   A reports folder (along with data & output) should appear with all 
   PDF reports.
```