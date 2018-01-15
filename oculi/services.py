import json
import io
import PIL
import flask
import time
import traceback

from functools import wraps
from oculi import app, camera

currentImage = None

def produces(content_type):
    def content_type_decorator(f):
        @wraps
        def wrapper(*args, **kwargs):
            r = f(*args, **kwargs)
            return flask.Response(r, content_type=content_type)

    return content_type_decorator

@app.route('/about')
#@produces('text/json')
def about():
    return flask.Response(json.dumps('Oculi version 0.0.1'),
                          'text/json')

@app.route('/take_photo')
#@produces('image/jpeg')
def take_photo():
    try:
        stream = io.BytesIO()
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, format='jpeg')
        camera.stop_preview()
        stream.seek(0)
        return flask.send_file(stream, mimetype='image/jpeg')
    except:
        app.logger.error(traceback.format_exc())
        flask.abort(500)

