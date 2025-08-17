import logging

class LoggerConfig:
    @staticmethod
    def get_logger(name: str):
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            logging.basicConfig(level=logging.INFO)
        return logger
