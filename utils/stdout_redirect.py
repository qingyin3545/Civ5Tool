import sys

class StdoutToLogger:
    def __init__(self, log_func):
        self.log_func = log_func

    def write(self, message):
        message = message.rstrip()
        if message:
            self.log_func(message)

    def flush(self):
        pass