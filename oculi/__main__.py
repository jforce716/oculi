import sys
import json
from oculi.core import OculiCore

def print_usage():
    print('Usage: python -m oculi [path_to_config_file]')
    sys.exit(1)

def load_json(path_to_json):
    with open(path_to_json, 'r') as f:
        config = json.load(f)
    return config

if len(sys.argv) > 2:
    print_usage()

config = None
if len(sys.argv) == 2:
    config = load_json(sys.argv[1])
oculi_core = OculiCore(config)
print('Starting Oculi. Press Contrl-C to exit')
oculi_core.start()

    
    
    
    
