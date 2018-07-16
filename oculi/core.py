import io
import logging
import time
import importlib
import threading

from PIL import Image
from picamera import PiCamera

CAMERA_SETTINGS = 'cameraSettings'
TRIGGER_SETTINGS = 'triggerSettings'
ACTION_SETTINGS = 'actionSettings'

MODULE_KEY = 'moduleName'
DEFAULT_TRIGGER_MODULE = 'oculi.scheduled'
DEFAULT_ACTION_MODULE = 'oculi.fileaction'

logger = logging.getLogger(__name__)

def value_for_key(vdict, key, default_value):
    if key in vdict:
        return vdict[key]
    else:
        return default_value
        
class OculiCore:
    def __init__(self, config):
        if config is None:
            config = {}

        self.act_condition = threading.Condition() 
        self.camera = PiCamera()
        try:
            self.config(config)
        except:
            logger.exception('Error occurred during configuration')
            
    def config(self, config):
        if CAMERA_SETTINGS in config:
            for attr in config[CAMERA_SETTINGS]:
                self.set_camera_attr(attr, config[CAMERA_SETTINGS][attr])

        self.setup_trigger(config[TRIGGER_SETTINGS])
        self.setup_action(config[ACTION_SETTINGS])

    def start(self):
        '''Start oculi. It will listen to trigger for events . When it happens,
           the OculiCore will take action.'''
        if self.trigger is not None:
            self.trigger.start()

        while True:
            self.act_condition.acquire()
            self.act_condition.wait()
            self.take_action()
            self.act_condition.release()

    def take_action(self):
        '''Take a picture, post-processing it and decide
           whether send it to server or ignore.'''
        image = self.take_picture()
        if image is None:
            return

        if self.postProcessor is not None:
            self.postProcessor.process(image)
        else:
            logger.warning('No post processor is configured')

    def take_picture(self):
        try:
            stream = io.BytesIO()
            self.camera.start_preview()
            time.sleep(2)
            self.camera.capture(stream, format='jpeg')
            self.camera.stop_preview()
            stream.seek(0)
            return Image.open(stream)
        except:
            logger.exception('Error occurred while taking photo')

        return None
            
    
    def set_camera_attr(self, attr_name, value):
        try:
            setattr(self.camera, attr_name, value)
        except:
            logger.exception('Cannot set camera attribute: {} to {}',
                             attr_name, value)

    def setup_trigger(self, config):
        if config is None:
            config = {}
            
        mname = value_for_key(config, MODULE_KEY, DEFAULT_TRIGGER_MODULE)
        print('module name is {}'.format(mname))
        mod = importlib.import_module(mname)
        self.trigger = mod.get_trigger(self.act_condition, config)
        
    def setup_action(self, config):
        if config is None:
            config = {}

        mname = value_for_key(config, MODULE_KEY, DEFAULT_ACTION_MODULE)
        mod = importlib.import_module(mname)
        self.postProcessor = mod.get_processor(config)
        
