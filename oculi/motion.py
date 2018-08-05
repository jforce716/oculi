from PIL import Image
from PIL import ImageFilter
from PIL import ImageChops

import sys

class MotionDetector:
    def __init__(self, blur_radius=21, delta_thresh=5,
                 min_diff_ratio=0.1):
        self.blurFilter = ImageFilter.GaussianBlur(radius=blur_radius)
        self.delta_thresh = delta_thresh
        self.min_diff_ratio = min_diff_ratio
        self.avg_background = None

    def detect_motion(self, image, debug=False):
        blured_image = image.filter(self.blurFilter)
        if self.avg_background is None:
            self.avg_background = blured_image
            return False
        
        self.avg_background = ImageChops.add(self.avg_background,
                                             blured_image, 2)
        imagedelta = ImageChops.difference(self.avg_background, blured_image)
        thresh = imagedelta.point(lambda x: 0 if x < self.delta_thresh else 255)

        total = 0
        changedtotal = 0
        for p in thresh.getdata():
            total += 1
            if p >= 255:
                changedtotal += 1
        motion = (changedtotal / total > self.min_diff_ratio)

        if debug:
            self.avg_background.show()
            blured_image.show()
            imagedelta.show()
            thresh.show()
            print('Difference ratio: {}'.format(changedtotal / total))
            
        return motion
        
