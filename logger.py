import logging
import os

class Logger:
    def __init__(self, name="library_log", log_file="log_file.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create a StreamHandler for console output
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # Check if the log file exists, create if not
        if not os.path.exists(log_file):
            with open(log_file, 'w'):
                pass  

        # Create a FileHandler for writing logs to a file
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

# Example usage
logger = Logger()
logger.log_info("This is an info message")
logger.log_warning("This is a warning message")
logger.log_error("This is an error message")
