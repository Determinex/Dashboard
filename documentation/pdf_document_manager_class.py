# PDFDocumentManager class
class PDFDocumentManager:
    def __init__(self, output_pdf_path, logging_manager):
        self.output_pdf_path = output_pdf_path
        self.logging_manager = logging_manager

    def create_pdf_batch(self, files, directory_structure):
        self.logging_manager.info("Starting PDF batch creation.")

        # Create a simple PDF document
        doc = SimpleDocTemplate(self.output_pdf_path, pagesize=letter)
        elements = []

        # Add title page
        title = "Dashboard: A Flask Application for Data Management Solutions"
        elements.append(Paragraph(title, getSampleStyleSheet()['Title']))
        elements.append(Spacer(1, 12))
        elements.append(PageBreak())

        # Add Table of Contents
        elements.append(Paragraph("Table of Contents", getSampleStyleSheet()['Heading1']))
        elements.append(Spacer(1, 12))

        # Add the directory structure formatted as a tree
        for line in directory_structure:
            elements.append(Paragraph(line, getSampleStyleSheet()['Normal']))
            elements.append(Spacer(1, 5))  # Add some spacing between items
        elements.append(PageBreak())

        # Process each file
        for file_path in files:
            try:
                self.logging_manager.debug(f"Processing file: {file_path}")
                content_lines = list(FileManager.read_file_generator(file_path))

                if not content_lines:
                    self.logging_manager.warning(f"No valid content to process in file: {file_path}.")
                    continue

                # Add file title
                file_title = str(file_path.relative_to(Path.cwd()))
                elements.append(Paragraph(file_title, getSampleStyleSheet()['Heading2']))
                elements.append(Spacer(1, 12))

                # Highlighted code or text
                highlighted_code = self.highlight_code(content_lines, file_path.suffix)
                elements.append(Preformatted(highlighted_code, getSampleStyleSheet()['Code']))
                elements.append(PageBreak())
            except Exception as e:
                self.logging_manager.error(f"Failed to process file {file_path}: {e}")
                continue

        # Build the document
        doc.build(elements)
        self.logging_manager.info("Batch processing completed. PDF created successfully.")

    def highlight_code(self, content_lines, file_extension):
        # Highlight the lines of code based on the file type
        lexer_mapping = {
            '.py': PythonLexer(),
            '.html': HtmlLexer(),
            '.js': JavascriptLexer(),
            '.css': CssLexer()
        }
        
        lexer = lexer_mapping.get(file_extension, None)

        highlighted_code = ""
        for line in content_lines:
            if isinstance(line, str):
                if lexer:  # Ensure a valid lexer is being used
                    highlighted_line = highlight(line, lexer, HtmlFormatter())
                    soup = BeautifulSoup(highlighted_line, 'html.parser')
                    highlighted_code += soup.get_text() + "\n"
                else:
                    self.logging_manager.warning(f"No lexer found for file extension: {file_extension}")
            else:
                self.logging_manager.warning("Invalid line detected, skipping.")

        return highlighted_code

    def process_files_in_batches(self, files, batch_size=50):
        """Yield files in batches of specified size for processing."""
        for i in range(0, len(files), batch_size):
            yield files[i:i + batch_size]