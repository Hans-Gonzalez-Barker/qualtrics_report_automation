from fpdf import FPDF
import os


def generate_pdf_report(workshop_name, chart_path, enjoy_comments, change_comments, output_folder="reports"):
    """
    Assembles the feedback data into a styled PDF.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize PDF (A4 size, units in millimeters)
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header / Title
    pdf.set_font("Arial", 'B', 16)
    title = f"AU25 Instructor Feedback - {workshop_name}"
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
        # multi_cell allows text to wrap to the next line automatically
        pdf.multi_cell(0, 6, f"- {comment}")
        pdf.ln(2)

    pdf.ln(5)

    # Qualitative Section: Change
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "What would you change about this class to make it better?", ln=True)

    pdf.set_font("Arial", '', 10)
    for comment in change_comments:
        pdf.multi_cell(0, 6, f"- {comment}")
        pdf.ln(2)

    # Export the final file
    safe_name = workshop_name.replace(" ", "_").replace("/", "-")
    output_path = os.path.join(output_folder, f"Report_{safe_name}.pdf")
    pdf.output(output_path)

    return output_path