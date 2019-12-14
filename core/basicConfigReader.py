# -*- coding: UTF-8 -*-
#
"""
read details of configfile
"""

import logging
logger = logging.getLogger(__name__)
# ----------------------------------------------------------------------------
import sys, os, configparser, pathlib
# ----------------------------------------------------------------------------

class defaultConfig:
    """Access config file details, parameter 'configFileName' is optional, default value = 'config/config.cnf'"""
    def __init__(self, 
        configFileName = os.path.join(os.getcwd(), 'config','config.cnf')
        ):
        # source:https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
        theFilePath = pathlib.Path(configFileName)
        if theFilePath.is_file():
            self._configFileName = configFileName
            logger.debug(f"config file = '{self._configFileName}'")
            self._readConfigFile()
        else:
            self._configFileName = configFileName            
            logger.error(f"config file '{self._configFileName}' does not exist.")
            raise FileNotFoundError 
        
    def _readConfigFile(self):
        """load and evaluate configuration file"""
        self._config = configparser.ConfigParser() 
        self._config.read(self._configFileName)

    def getValue(self, section : str ,  option : str)  -> str:
        """get value from configfile"""
        if not self._config.has_section(section):
            logger.error(f"section '{section}' not found in '{self._configFileName}''")
            raise configparser.ParsingError
        if not self._config.has_option(section,option):
            logger.error(f"option '{option}' not found at section '{section}' in '{self._configFileName}''")
            raise configparser.ParsingError
        theValue=self._config.get(section,option)
        if len(theValue)== 0:
            logger.error(f"option '{option}' has no value at section '{section}' in '{self._configFileName}''")
            raise configparser.ParsingError
        return theValue

    @property
    def configFileName(self):
        """Get full path and name of config file"""
        return self._configFileName

    @configFileName.setter
    def configFileName(self,configFileName : str):
        """set full path and name of config file"""
        # source:https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
        theFilePath = pathlib.Path(configFileName)
        self._configFileName = configFileName
        if theFilePath.is_file():
            logger.debug(f"config file = '{self.configFileName()}'")
            self._readConfigFile()
        else:
            logger.error(f"config file '{self.configFileName()}' does not exist.")
            raise FileNotFoundError 

def main():
    logger.info("--- Basic Config File Reader Class ---")

if __name__ == '__main__':
    main()    
