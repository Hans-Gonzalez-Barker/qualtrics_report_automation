from fpdf import FPDF
import os
from dotenv import load_dotenv

load_dotenv()

SEMESTER = os.getenv("SEMESTER")


def clean_text(text):
    """
        Sanitizes Unicode 'smart' characters for FPDF compatibility.

        Replaces curly quotes, apostrophes, and dashes with standard ASCII
        equivalents to prevent PDF encoding errors.

        Args:
            text (str): The input string to be cleaned.

        Returns:
            str: A Latin-1 encoded string safe for PDF generation.
    """
    if not isinstance(text, str):
        return str(text)

    # Replace common curly quotes and apostrophes
    replacements = {
        "\u2018": "'",  # Left single quote
        "\u2019": "'",  # Right single quote
        "\u201c": '"',  # Left double quote
        "\u201d": '"',  # Right double quote
        "\u2013": "-",  # En dash
        "\u2014": "-",  # Em dash
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)

    # Encode to latin-1 and ignore anything that won't fit
    return text.encode('latin-1', 'ignore').decode('latin-1')


def generate_pdf_report(workshop_name, chart_path, enjoy_comments, change_comments, output_folder="reports"):
    """
        Compiles workshop data and charts into a multi-page PDF feedback report.

        Args:
            workshop_name (str): Name of the workshop for the header and filename.
            chart_path (str): Path to the pre-generated Matplotlib chart.
            enjoy_comments (list): List of qualitative 'positive' responses.
            change_comments (list): List of qualitative 'improvement' responses.
            output_folder (str): Directory to save the final PDF.

        Returns:
            str: The file path to the generated PDF report.
    """
    # Create a reports/ folder if not already there
    os.makedirs("reports", exist_ok=True)

    # Initialize PDF (A4 size, units in millimeters)
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header / Title
    pdf.set_font("Arial", 'B', 16)
    title = f"{SEMESTER} Instructor Feedback - {workshop_name}"
    pdf.cell(0, 10, title, ln=True, align='C')
    # Line break
    pdf.ln(5)

    # Add the Chart
    # Center image by calculating the offset (A4 width is 210mm)
    chart_width = 170
    x_offset = (210 - chart_width) / 2
    pdf.image(chart_path, x=x_offset, y=None, w=chart_width)
    pdf.ln(10)

    # Qualitative Section: Enjoy Most
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "What did you enjoy most about the class?", ln=True)

    pdf.set_font("Arial", '', 10)
    for comment in enjoy_comments:
        # We clean every comment before putting it in the PDF
        cleaned_comment = clean_text(comment)
        pdf.multi_cell(0, 6, f"- {cleaned_comment}")
        pdf.ln(2)

    pdf.ln(5)

    # Qualitative Section: Change
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "What would you change about this class to make it better?", ln=True)

    pdf.set_font("Arial", '', 10)
    for comment in change_comments:
        cleaned_comment = clean_text(comment)
        pdf.multi_cell(0, 6, f"- {cleaned_comment}")
        pdf.ln(2)

    # Export the final file
    safe_name = workshop_name.replace("/", "-")
    output_path = os.path.join(output_folder, f"{safe_name}.pdf")
    pdf.output(output_path)

    return output_path