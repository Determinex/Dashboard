# logger.py
import os
import datetime

class Logger:
    def __init__(self):
        self.log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error_log.txt')

    def log_error(self, message):
        with open(self.log_file_path, 'a') as log_file:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{timestamp} - ERROR - {message}\n")

    def log_info(self, message):
        with open(self.log_file_path, 'a') as log_file:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{timestamp} - INFO - {message}\n")