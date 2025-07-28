import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import time

try:
    from flask import request
except ImportError:
    request = None  # For non-Flask use cases

# Set up a module-level logger
logger = None

class ContextFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'user_id'):
            record.user_id = 'system'
        return True

def setup_logger(name: str, log_file: str, level=logging.INFO):
    global logger
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [user_id=%(user_id)s] - %(message)s'
    )


    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console)
    logger.propagate = False

    return logger
def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if logger is None:
            raise RuntimeError("Logger not initialized. Call setup_logger() first.")

        start = time.time()
        user_id = 'system'  # Default fallback
        params = {}

        if request:
            try:
                params = request.get_json(silent=True) or request.args.to_dict()
                user_id = getattr(request, 'user', 'anonymous')  # You can modify this if you have a `current_user` or JWT
            except Exception:
                pass

        extra = {
            "user_id": user_id,
            "params": params
        }

        logger.info(f"Calling {func.__name__}", extra=extra)
        result = func(*args, **kwargs)
        duration = (time.time() - start) * 1000
        logger.info(f"Executed {func.__name__} in {duration:.2f} ms", extra=extra)
        return result
    return wrapper

