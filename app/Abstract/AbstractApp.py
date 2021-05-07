#!/bin/python3
import logging
from time import sleep

class AbstractApp:

    def __init__(self):
        pass

    def get_logger(self, name) -> logging.Logger:
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def idle(self, duration=None):
        interval = duration if duration else self.idle_interval
        self.log.debug(f"Idling for {interval} seconds.")
        sleep(interval)