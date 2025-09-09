import logging

class Logger:
    def __init__(self, log_file):
        logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
        open(log_file, 'w').close()
            
    def log_and_print(self, *args, **kwargs):
        """Logs and prints messages simultaneously, supporting multiple arguments like print()"""
        message = " ".join(str(arg) for arg in args)
        print(message, **kwargs)
        logging.info(message)
        
        
    def log_only (self,*args, **kwargs):
        """Logs messages, supporting multiple arguments like print()"""
        message = " ".join(str(arg) for arg in args)
        logging.info(message)
        