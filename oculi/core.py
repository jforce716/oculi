import io
import logging
import time
import importlib

from picamera import PiCamera
from picamera.array import PiRGBArray

from PIL import Image
from PIL import ImageFilter
from PIL import ImageChops

from oculi.motion import MotionDetector

PP_MODULE_KEY = 'postProcessorName'
RESOLUTION_KEY = 'resolution'
VFLIP_KEY = "vflip"
FPS_KEY = 'fps'
SHOW_VIDEO_KEY = 'showVideo'
MIN_DIFF_KEY = 'minDiffPercentage'
DELTA_THRESH_KEY = 'deltaThresh'

DEFAULT_ACTION_MODULE = 'oculi.fileaction'
DEFAULT_RESOLUTION = [640, 480]
DEFAULT_FPS = 8
DEFAULT_VFLIP = True
DEFAULT_SHOW_VIDEO = True
DEFAULT_DELTA_THRESH = 5
DEFAULT_MIN_DIFF = 0.05
WARMUP_TIME = 3

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

        try:
            self.config(config)
        except:
            logger.exception('Error occurred during configuration')
            
    def config(self, config):
        self.camera = PiCamera()
        self.camera.resolution = tuple(config.get(RESOLUTION_KEY,
                                                  DEFAULT_RESOLUTION))
        self.camera.vflip = config.get(VFLIP_KEY, DEFAULT_VFLIP)
        self.camera.framerate = config.get(FPS_KEY, DEFAULT_FPS)
        self.useVideo = config.get(SHOW_VIDEO_KEY, DEFAULT_SHOW_VIDEO)

        deltaThresh = config.get(DELTA_THRESH_KEY, DEFAULT_DELTA_THRESH)
        minDiffRatio = config.get(MIN_DIFF_KEY, DEFAULT_MIN_DIFF)
        self.mdetector = MotionDetector(delta_thresh=deltaThresh,
                                        min_diff_ratio=minDiffRatio)
        
        self.setup_postprocessor(config)

    def start(self):
        '''Start motion detection. Once motion is detected,
           call postprocessor'''
        time.sleep(WARMUP_TIME)

        avg = None
        blurFilter = ImageFilter.GaussianBlur(radius=21)
        rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)

        for f in self.camera.capture_continuous(rawCapture,
                                                format='rgb',
                                                use_video_port=self.useVideo):
            try:
                frame = Image.fromarray(f.array)
                if self.mdetector.detect_motion(frame.split()[1]):
                    logger.info('Motion detected')
                    if self.postprocessor is not None:
                        self.postprocessor.process(frame)
            finally:
                rawCapture.truncate(0)
    
    def setup_postprocessor(self, config):
        mname = config.get(PP_MODULE_KEY, DEFAULT_ACTION_MODULE)
        mod = importlib.import_module(mname)
        self.postprocessor = mod.get_processor(config)
        
