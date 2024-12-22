import logging

# Create a logger object
logger = logging.getLogger('logger')
log_level = logging.DEBUG

# Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(log_level)

# Create a file handler and set its level
file_handler = logging.FileHandler('exploding_kittens.log')
file_handler.setLevel(log_level)

# Create a console handler and set its level
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)


# Create a custom formatter class to align messages on different log levels
class FixedWidthFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{record.levelname:<5}"  # 5 is enough as I don't use WARNING or CRITICAL in this project
        return super().format(record)


# Create a formatter and set its format
formatter = FixedWidthFormatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
