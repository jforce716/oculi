import sys
import json
from oculi.core import OculiCore

prompt = 'Oculi>'
unknown_cmd = 'Unknown command, type help for a list of valid commands'

cmd_mapping = {
    'exit': lambda: True
}

def print_usage():
    print('Usage: python -m oculi [path_to_config_file]')

def load_json(path_to_json):
    with open(path_to_json, 'r') as f:
        config = json.load(f)
    return config

oculi_core = OculiCore()

if len(sys.argv) > 2:
    print_usage()
elif len(sys.argv) == 2:
    oculi_core.config(load_json(sys.argv[1]))

oculi_core.start()

while True:
    key = input(prompt)
    if not (key in cmd_mapping):
        print(unknown_cmd)
    else:
        if cmd_mapping[key]():
            break

    
    
    
    
