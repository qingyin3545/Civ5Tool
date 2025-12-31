class StdoutToLogger:
    def __init__(self, log_func, tag="builder"):
        self.log_func = log_func
        self.tag = tag

    def write(self, message):
        message = message.rstrip()
        if message:
            self.log_func(message, self.tag)

    def flush(self):
        pass