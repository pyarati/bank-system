import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s')

file = logging.FileHandler('record.log')
file.setFormatter(log_format)

console = logging.StreamHandler()
console.setFormatter(log_format)

logger.addHandler(file)
logger.addHandler(console)
