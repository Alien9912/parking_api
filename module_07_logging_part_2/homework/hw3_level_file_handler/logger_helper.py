import logging
import os

class LevelFileHandler(logging.Handler):
    def __init__(self, path_template):
        super().__init__()
        self.path_template = path_template

    def emit(self, record):
        levelname = record.levelname.lower()
        filename = self.path_template.format(level=levelname)
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(self.format(record) + '\n')