#Universal Devices
#MIT License
import logging
import os
from typing import Literal
import traceback

# Set up the basic configuration for the logger
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger instance
oadr3_logger = logging.getLogger('oadr3.logger')
logging_inited = False

def init_oadr3_logging(path:str):
    global logging_inited
    if logging_inited:
        return
    if path == None:
        raise Exception ("need the path for logger to create the log file ...")
    logging_inited = True
    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler(os.path.join(path, 'oadr3.log'))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Create a stream handler to output logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Add the file handler and stream handler to the logger
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(console_handler)

    # Use the logger in your extension
    #logger.debug('Debug message')
    #logger.info('Information message')
    #logger.warning('Warning message')
    #logger.error('Error message')
    #logger.critical('Critical message')



def oadr3_log(level:Literal['debug', 'info', 'warning', 'error', 'critical'], message:str, traceback:bool=False):
    if message == None:
        return
    try:
        method = getattr(oadr3_logger, level)
        if method == None:
            return
        method(message, exc_info=traceback)
    except Exception as ex:
        oadr3_logger.exception("Critical Exception ...")

def oadr3_log_debug(message:str):
    oadr3_log('debug', message)

def oadr3_log_info(message:str):
    oadr3_log('info', message)

def oadr3_log_warning(message:str):
    oadr3_log('warning', message)

def oadr3_log_error(message:str, traceback:bool=False):
    oadr3_log('warning', message, traceback)

def oadr3_log_critical(message:str, traceback:bool=True): oadr3_log('critical', message, traceback)

class Oadr3LoggedException(Exception):

    '''
        Use this class to log exceptions including traceback
        log + level + include traceback.
        level can only be debug, info, warning, error, critical
    '''
    def __init__(level:Literal['debug', 'info', 'warning', 'error', 'critical'], message:str, traceback:bool=False):
        super.__init__(message)
        oadr3_log(level, message, traceback)
        
