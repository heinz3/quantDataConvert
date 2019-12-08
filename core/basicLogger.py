# -*- coding: UTF-8 -*-
#
"""
setup basic logging capabilities
"""

import logging
logger = logging.getLogger(__name__)
# ----------------------------------------------------------------------------
import sys, os, argparse, errno, time, pathlib
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
# ----------------------------------------------------------------------------


def main():
    initiate(logging.INFO)
    logger.info("--- Basic Logger Modul  ---")

def initiate(theLogLevel=logging.INFO):    
    # -------------------------------------------
    # setup logging with minimalistic features
        
    # log level
    # theLogLevel = logging.INFO

    # log date format
    theLogDateFormat = "%H:%M:%S"
    
    # log format
    theLogFormat = '%(asctime)s [%(levelname)-8s] %(message)s'

    # log file location
    theLogDirectory = os.path.join(os.getcwd(), 'log')
    # source: https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
    pathlib.Path(theLogDirectory).mkdir(parents=True, exist_ok=True) 
    theLogFileName = os.path.join(theLogDirectory,'log.txt')  

    # log setup

    # source: https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
    theConsoleHandler = logging.StreamHandler(sys.stdout)

    # source: http://www.blog.pythonlibrary.org/2014/02/11/python-how-to-create-rotating-logs/
    theFileHandler = TimedRotatingFileHandler(theLogFileName, encoding="utf-8",
                                       when="d",
                                       interval=1,
                                       backupCount=5)

    # source: http://plumberjack.blogspot.com/2011/04/added-functionality-for-basicconfig-in.html                                       
    logging.basicConfig(
                        level=theLogLevel,
                        format=theLogFormat,
                        datefmt=theLogDateFormat,
                        handlers=[
                            theConsoleHandler,
                            theFileHandler
                        ]
                        )


if __name__ == '__main__':
    main()    
