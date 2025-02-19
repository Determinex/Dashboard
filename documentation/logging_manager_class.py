# Class to manage logging
class LoggingManager:
    def __init__(self, event_log_path="event_log.txt", error_log_path="error_log.txt"):
        self.logger = logging.getLogger("PDFDocumentLogger")
        self.logger.setLevel(logging.DEBUG)

        # Event log handler
        event_handler = logging.FileHandler(event_log_path)
        event_handler.setLevel(logging.DEBUG)
        event_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        event_handler.setFormatter(event_formatter)
        
        # Error log handler
        error_handler = logging.FileHandler(error_log_path)
        error_handler.setLevel(logging.WARNING)
        error_handler.setFormatter(event_formatter)

        self.logger.addHandler(event_handler)
        self.logger.addHandler(error_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)