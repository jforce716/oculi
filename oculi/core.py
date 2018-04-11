import io
import logging
import PIL
import time
import importlib

from picamera import PiCamera

CAMERA_SETTINGS = 'cameraSettings'
TRIGGER_SETTINGS = 'triggerSettings'
MODULE_KEY = 'moduleName'
DEFAULT_TRIGGER_MODULE = 'oculi.scheduled'

logger = logging.getLogger(__name__)

class OculiCore:
    def __init__(self, config={}):
        self.camera = PiCamera()
        if config is not None:
            self.config(config)
        else:
            logger.exception('None configuration')
            
    def config(self, config):
        if CAMERA_SETTINGS in config:
            for attr in config[CAMERA_SETTINGS]:
                self.set_camera_attr(attr, config[CAMERA_SETTINGS][attr])

        if TRIGGER_SETTINGS in config:
            self.setup_trigger(config=config[TRIGGER_SETTINGS])
        else:
            self.setup_trigger()

    def start(self):
        '''Start oculi. It will listen to trigger for events . When it happens,
           the OculiCore will take action.'''
        if self.trigger is not None:
            self.trigger.start()

    def take_action(self):
        '''Take a picture, post-processing it and decide
           whether send it to server or ignore.'''
        print('Event triggered. Take action...')

    def take_picture(self):
        try:
            stream = io.BytesIO()
            self.camera.start_preview()
            time.sleep(2)
            self.camera.capture(stream, format='jpeg')
            self.camera.stop_preview()
            stream.seek(0)
            return PIL.Image.open(stream)
        except:
            logger.exception('Error occurred while taking photo')

        return None
            
    
    def set_camera_attr(self, attr_name, value):
        try:
            setattr(self.camera, attr_name, value)
        except:
            logger.exception('Cannot set camera attribute: {} to {}',
                             attr_name, value)

    def setup_trigger(self, config={}):
        mname = DEFAULT_TRIGGER_MODULE
        if config is not None and MODULE_KEY in config:
            mname = config[TRIGGER_MODULE]
        mod = importlib.import_module(mname)
        self.trigger = mod.get_trigger(self.take_action, config)
        
