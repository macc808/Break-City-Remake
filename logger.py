import logging

class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR

class NonErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.ERROR

# Set up logger
logger_instance = logging.getLogger('game')
logger_instance.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.addFilter(NonErrorFilter())
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger_instance.addHandler(console_handler)

# File handler for errors
file_handler = logging.FileHandler('assets/game_log.txt')
file_handler.setLevel(logging.ERROR)
file_handler.addFilter(ErrorFilter())
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger_instance.addHandler(file_handler)

class Logger:
    def __init__(self):
        self.logger = logger_instance

    def log_message(self, func, res):
        self.logger.info(f"{func.__name__} returned: {res}")

    def clear_log(self):
        with open('assets/game_log.txt', 'w') as f:
            f.write("")

logger = Logger()