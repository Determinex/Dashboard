# generate_dashboard_pdf.py

import os
from fpdf import FPDF
from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, JavascriptLexer, CssLexer
from pygments.formatters import HtmlFormatter
from bs4 import BeautifulSoup
import PyPDF2

class PDF(FPDF):
    def header(self):
        # Centered title for each file
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Page number
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def highlight_code(content, file_extension):
    if file_extension == '.py':
        lexer = PythonLexer()
    elif file_extension == '.html':
        lexer = HtmlLexer()
    elif file_extension == '.js':
        lexer = JavascriptLexer()
    elif file_extension == '.css':
        lexer = CssLexer()
    else:
        return content  # No highlighting for unsupported file types

    highlighted_content = []
    for line in content:
        highlighted_line = highlight(line, lexer, HtmlFormatter())
        soup = BeautifulSoup(highlighted_line, 'html.parser')
        highlighted_content.append(soup.get_text())
    return highlighted_content

def create_pdf(files, output_pdf_path, directory_structure, text_only=False):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Dashboard: A Flask Application for Data Management Solutions", 0, 1, 'C')
    pdf.ln(20)  # Add some space after the title

    # Table of Contents
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Table of Contents", 0, 1, 'C')
    pdf.set_font("Arial", size=12)

    # Print the directory structure
    for line in directory_structure:
        pdf.cell(0, 10, line, 0, 1)

    pdf.add_page()  # Add a new page for the content

    # Process each file
    for file_path in files:
        pdf.title = os.path.relpath(file_path, os.getcwd())  # Set the title for the header
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, pdf.title, 0, 1, 'C')
        pdf.ln(5)

        # Read the file content
        file_extension = os.path.splitext(file_path)[1]
        content = read_file(file_path)

        if text_only:
            # Add text-only content
            pdf.set_font("Courier", size=10)
            for line in content:
                pdf.multi_cell(0, 10, line.strip())
        else:
            # Add highlighted content
            highlighted_content = highlight_code(content, file_extension)
            pdf.set_font("Courier", size=10)
            for line in highlighted_content:
                pdf.multi_cell(0, 10, line)

    pdf.output(output_pdf_path)

def compress_pdf(input_pdf_path, output_pdf_path):
    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PyPDF2.PdfReader(input_pdf_file)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        with open(output_pdf_path, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

def find_files_and_directories(directory):
    supported_extensions = ['.py', '.html', '.js', '.css']
    files = []
    directory_structure = []

    for root, dirs, filenames in os.walk(directory):
        # Create a relative path for the current directory
        relative_path = os.path.relpath(root, directory)
        if relative_path == '.':
            relative_path = 'Dashboard'  # Rename the root directory for clarity
        else:
            relative_path = os.path.join('Dashboard', relative_path)  # Prefix with 'Dashboard' for clarity

        # Add the directory to the structure with indentation
        depth = relative_path.count(os.sep)  # Count the depth of the directory
        indented_path = ' ' * depth + relative_path
        directory_structure.append(indented_path)

        for filename in filenames:
            if any(filename.endswith(ext) for ext in supported_extensions):
                files.append(os.path.join(root, filename))

    return files, directory_structure

if __name__ == "__main__":
    directory = os.getcwd()  # Use the current working directory as the base path
    files, directory_structure = find_files_and_directories(directory)

    # Create text-only PDF
    text_only_pdf_path = 'text_only_output.pdf'
    create_pdf(files, text_only_pdf_path, directory_structure, text_only=True)
    compress_pdf(text_only_pdf_path, 'compressed_text_only_output.pdf')

    # Create formatted PDF
    formatted_pdf_path = 'formatted_output.pdf'
    create_pdf(files, formatted_pdf_path, directory_structure, text_only=False)
    compress_pdf(formatted_pdf_path, 'compressed_formatted_output.pdf')