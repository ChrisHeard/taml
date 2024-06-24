import logging

class CustomLogger:
    
    _instance: object = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CustomLogger, cls).__new__(cls)
            cls._instance._initialize_logger(*args, **kwargs)
        return cls._instance

    def _initialize_logger(self, name: str, info_log_file: str = 'info.log', error_log_file: str = 'error.log', level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:

            info_handler = logging.FileHandler(info_log_file, mode='a')
            info_handler.setLevel(logging.INFO)
            info_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            info_handler.setFormatter(info_formatter)
            
            error_handler = logging.FileHandler(error_log_file, mode='a')
            error_handler.setLevel(logging.ERROR)
            error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            error_handler.setFormatter(error_formatter)
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            
            self.logger.addHandler(info_handler)
            self.logger.addHandler(error_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def critical(self, message: str):
        self.logger.critical(message)
