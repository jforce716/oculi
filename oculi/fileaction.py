import os
from datetime import datetime

PATH_KEY = 'directory'
FILENAME_FORMAT_KEY = 'fileNameFormat'
MOTION_GAP_KEY = 'montionGap'

DEFAULT_PATH = '.'
DEFAULT_NAME_FORMAT = 'oculi_%y_%m_%d_%H_%M_%S_%f.jpg'
DEFAULT_MOTION_GAP = 2

def get_processor(config):
    return FileBasedProcessor(config)

class FileBasedProcessor:
    def __init__(self, config):
        if config is None:
            config = {}

        self.target_path = config.get(PATH_KEY, DEFAULT_PATH)
        self.name_format = config.get(FILENAME_FORMAT_KEY,
                                      DEFAULT_NAME_FORMAT)
        self.motionGap = config.get(MOTION_GAP_KEY, DEFAULT_MOTION_GAP)
        self.lastMotion = None

    def process(self, image):
        now = datetime.now()
        delta = None if self.lastMotion is None else now - self.lastMotion
        if delta is None or delta.total_seconds() > self.motionGap:
            name = now.strftime(self.name_format)
            image.save(os.path.join(self.target_path, name))
        self.lastMotion = now
        
    
