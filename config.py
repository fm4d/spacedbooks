import logging

SPACED_REPETITION_INTERVALS = [30, 60, 120, 180, 360, 360, 360, 360, 360, 360, 360, 360]

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.FileHandler('main.log'))