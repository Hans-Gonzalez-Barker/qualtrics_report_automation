import pandas as pd


def load_and_clean_data(file_path):
    """
        Loads raw Qualtrics CSV data and performs initial cleaning and transformation.

        This includes skipping metadata headers, consolidating 7-week and 14-week
        workshop columns, mapping text-based Likert scales to integers (1-5),
        and filtering for finished responses.

        Args:
            file_path (str): Path to the raw CSV file.

        Returns:
            pandas.DataFrame: A cleaned DataFrame ready for analysis.
    """

    # Load CSV, skipping the two label rows Qualtrics adds (rows 1 and 2)
    df = pd.read_csv(file_path, skiprows=[1, 2])

    # Create a unified Workshop column from Q5 (7-week) and Q6 (14-week)
    df['Workshop'] = df['Q5'].fillna(df['Q6'])

    # Define the Likert Scale mapping to quantify opinions
    likert_map = {
        "Strongly agree": 5,
        "Somewhat agree": 4,
        "Neither agree nor disagree": 3,
        "Somewhat disagree": 2,
        "Strongly disagree": 1
    }

    # Convert the agreement statements (Q7_1 to Q7_7) to numbers 1-5
    q7_cols = [f'Q7_{i}' for i in range(1, 8)]
    for col in q7_cols:
        df[col] = df[col].map(likert_map)

    # Filter - Keep only finished responses and remove previews
    df = df[df['Finished'] == True]
    if 'DistributionChannel' in df.columns:
        df = df[df['DistributionChannel'] != 'preview']

    return df


def get_workshop_metrics(df, workshop_name):
    """
    Extracts quantitative averages and qualitative comments for a specific workshop.

    Args:
        df (pandas.DataFrame): The cleaned survey dataset.
        workshop_name (str): The name of the workshop to filter by.

    Returns:
        tuple: (averages, enjoy_comments, change_comments) where averages is a Series
               of mean scores, and comments are lists of strings.
    """
    workshop_df = df[df['Workshop'] == workshop_name]

    # Calculate means for the 7 agreement questions
    q7_cols = [f'Q7_{i}' for i in range(1, 8)]
    averages = workshop_df[q7_cols].mean()

    # Get qualitative text responses (dropping empty ones)
    comments_enjoy = workshop_df['Q8'].dropna().tolist()
    comments_change = workshop_df['Q9'].dropna().tolist()

    return averages, comments_enjoy, comments_change