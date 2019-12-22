# -*- coding: UTF-8 -*-
#
#
# Copyright 2019 Heinrich Gerull
#
# Licensed under the GNU GENERAL PUBLIC LICENSE version 3
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
"""
setup basic logging capabilities
"""

import logging
logger = logging.getLogger(__name__)
# ----------------------------------------------------------------------------
import sys, os, pathlib
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
                                       backupCount=7)

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
