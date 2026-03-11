import logging

class AsciiFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().isascii()