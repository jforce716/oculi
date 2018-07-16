import logging
import threading
import time

INTERVAL = 'interval'
DEFAULT_INTERVAL = 5

logger = logging.getLogger(__name__)

def get_trigger(condition, config=None):
    if condition is None:
        logger.warning('No condition is provided, None will be returned')
        return None
    
    interval = DEFAULT_INTERVAL
    if config is not None and INTERVAL in config:
        interval = config[INTERVAL]

    return threading.Thread(target=trigger_function,
                            name='Oculi fixed interval trigger',
                            args=(interval, condition),
                            daemon=True)

def trigger_function(interval, condition):
    while True:
        condition.acquire()
        condition.notify()
        condition.release()
        time.sleep(interval)
        
                            
