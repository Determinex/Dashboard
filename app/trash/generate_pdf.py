# C:\Users\Andrew\AppData\Local\Programs\Python\Python313\python.exe C:\Users\Andrew\Documents\My_Programs\Dashboard\generate_pdf.py


import os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvasimport os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger

# Configure logging
logging.basicConfig(
    filename='event_log.txt',  # Output log file
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_pdf_from_file(file_path, output_pdf, max_line_length=80):
    """Convert a text or image file to a PDF."""
    try:
        c = canvas.Canvas(output_pdf, pagesize=letter)
        
        # Check the file type and process accordingly
        if file_path.endswith(('.txt', '.py', '.html', '.css', '.js')):
            c.drawString(100, 750, os.path.basename(file_path))  # Title
            c.drawString(100, 730, "---------------------------------")
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                y = 700
                for line in lines:
                    # Break long lines based on max_line_length
                    for i in range(0, len(line), max_line_length):
                        c.drawString(100, y, line[i:i + max_line_length].strip())
                        y -= 15
                        if y < 50:  # Check for page overflow
                            c.showPage()
                            y = 750
            logging.info(f"Successfully created PDF from file: {file_path}")
        elif file_path.endswith(('.jpg', '.jpeg', '.png')):
            c.drawImage(file_path, 100, 100)  # Adjust position as needed
            logging.info(f"Image added to PDF: {file_path}")
        else:
            logging.warning(f"Unsupported file type for file: {file_path}")

        c.save()
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

def traverse_directory(directory, merger, toc_canvas, toc_y):
    """Recursively traverse the directory and process files."""
    try:
        for root, dirs, files in os.walk(directory):
            logging.info(f"Traversing directory: {root}")  # Log current directory
            for file in files:
                file_path = os.path.join(root, file)
                logging.info(f"Found file: {file_path}")  # Log found files
                pdf_file_name = f"{file_path}.pdf"
                create_pdf_from_file(file_path, pdf_file_name)

                # Add to TOC
                toc_canvas.drawString(100, toc_y, f"{file_path}")
                toc_y -= 15

                # Append to merger
                merger.append(pdf_file_name)

        return toc_y  # Return the updated y position for TOC
    except Exception as e:
        logging.error(f"Error traversing directory {directory}: {e}")

def main():
    # Prompt for the directory containing files
    directory = input("Enter the directory to traverse: ")
    output_pdf = os.path.join(directory, 'final_document.pdf')  # Output PDF path

    logging.info("Script started.")
    
    try:
        # Prepare Table of Contents PDF
        toc_pdf = os.path.join(directory, 'toc.pdf')
        toc_canvas = canvas.Canvas(toc_pdf, pagesize=letter)
        toc_canvas.drawString(100, 750, "Table of Contents")
        toc_canvas.drawString(100, 730, "-------------------------------")
        toc_y = 710

        # Initialize PDF merger
        merger = PdfMerger()

        # Traverse the directory and process files
        toc_y = traverse_directory(directory, merger, toc_canvas, toc_y)

        # Save the TOC
        toc_canvas.save()
        merger.append(toc_pdf)

        # Write out the final PDF
        merger.write(output_pdf)
        merger.close()
        logging.info(f"Final PDF created: {output_pdf}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    print("Process completed. Check event_log.txt for details.")

if __name__ == "__main__":
    main()
