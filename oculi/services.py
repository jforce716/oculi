import json
from oculi import app

@app.route('/about')
def about():
    return json.dumps('Oculi version 0.0.1')

    
