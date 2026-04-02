class Logger:
    def __init__(self):
        self.filename = "game_log.txt"

    def log_message(self, func, res):
        with open(self.filename, 'a') as f:
            f.write(f"{func.__name__} returned: {res}\n")

    def clear_log(self):
        with open(self.filename, 'w') as f:
            f.write("")

logger = Logger()