import matplotlib.pyplot as plt
import os

# Mapping Qualtrics IDs to the actual labels from your survey
QUESTION_MAP = {
    'Q7_1': 'The instructor was knowledgeable about the subject',
    'Q7_2': 'The instructor was well prepared for class',
    'Q7_3': 'The instructor was engaging/enthusiastic/interactive',
    'Q7_4': 'The instructor answered questions in helpful ways.',
    'Q7_5': 'The class increased my knowledge and understanding about the subject',
    'Q7_6': 'The class materials were well-prepared',
    'Q7_7': 'The assignments were purposeful'
}


def create_bar_chart(averages, workshop_name, output_folder="output"):
    """
        Generates a horizontal bar chart visualizing instructor agreement scores.

        Saves the chart as a high-resolution PNG for inclusion in the PDF report.

        Args:
            averages (pandas.Series): Mean scores for the 7 Likert-scale questions.
            workshop_name (str): The name of the workshop for the chart title.
            output_folder (str): Directory to save the generated image.

        Returns:
            str: The file path to the saved chart image.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Prepare labels and values in reverse order for top-down display
    labels = [QUESTION_MAP[col] for col in averages.index][::-1]
    values = averages.values[::-1]

    # Initialize the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the horizontal bars
    bars = ax.barh(labels, values, color='#1f77b4', height=0.7)

    # Configure the X-Axis to match the 1-5 Likert Scale
    ax.set_xlim(1, 5)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels([
        'Strongly\ndisagree',
        'Somewhat\ndisagree',
        'Neither agree\nnor disagree',
        'Somewhat\nagree',
        'Strongly\nagree'
    ], fontsize=9)

    # Add styling and remove unnecessary borders (spines)
    ax.set_title(f"Agreement Scores: {workshop_name}", fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add numerical labels to the end of each bar for precision
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.05, bar.get_y() + bar.get_height() / 2,
                f'{width:.2f}', va='center', fontsize=10)

    # Adjust layout to prevent labels from being cut off
    plt.tight_layout()

    # Save the file with a unique name based on the workshop
    safe_name = workshop_name.replace("/", "-")
    filepath = os.path.join(output_folder, f"{safe_name} Chart.png")

    # High resolution for PDF
    plt.savefig(filepath, dpi=300)
    # Closes the plot to free up memory for the next loop
    plt.close()

    return filepath