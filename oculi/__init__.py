from flask import Flask
from picamera import PiCamera

app = Flask(__name__)
camera = PiCamera()
