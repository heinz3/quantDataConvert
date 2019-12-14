# -*- coding: UTF-8 -*-
#
"""
class for calling QuantDataManger on windows
"""

import logging
logger = logging.getLogger(__name__)
# ----------------------------------------------------------------------------
import sys, os, configparser, pathlib, subprocess, errno
import core.basicConfigReader as miniConfig
# ----------------------------------------------------------------------------

class callQuantDataManager:
    """call QuantDataManger on windows, optionally passing parameters"""
    def __init__(self, 
        aConfig : miniConfig.defaultConfig
        ):

        self._config = aConfig

        # data manager program
        theQuantDataManager_SectionName = "quantdatamanager"
        theQuantDataManager_Path               = self._config.getValue(theQuantDataManager_SectionName,"path")
        theQuantDataManager_ConsoleApplication = self._config.getValue(theQuantDataManager_SectionName,"application")
        theQuantDataManagerProgram             = os.path.join(theQuantDataManager_Path, theQuantDataManager_ConsoleApplication)

        # source:https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
        theFilePath = pathlib.Path(theQuantDataManagerProgram)
        if not theFilePath.is_file():
            logger.error(f"Quant Data Manager not found at '{theFilePath}'.")
            raise FileNotFoundError 
        self._QuantDataManager = theQuantDataManagerProgram
       
        # # calling QuantDataManager via .bat file
        # # .bat file location and name = bat/callProgram.bat
        # theBatchFile_Path    = "bat"
        # theBatchFile_Name    = "callProgram.bat"
        # theBatchFile_Program = os.path.join(os.getcwd(), theBatchFile_Path, theBatchFile_Name)

        # theFilePath = pathlib.Path(theBatchFile_Program)
        # if not theFilePath.is_file():
        #     logger.error(f"Batch File not found at '{theFilePath}'.")
        #     raise FileNotFoundError 
        # self._BatchFile = theBatchFile_Program

        # create data directory, if not exists
        theDataDirectory_SectionName = "data"
        theDataDirectory_Path        = aConfig.getValue(theDataDirectory_SectionName,"path")
        theDataDirectory_Path        = os.path.join(os.getcwd(), theDataDirectory_Path)
        # source: https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
        pathlib.Path(theDataDirectory_Path).mkdir(parents=True, exist_ok=True) 


    @property
    def QuantDataManagerFileName(self) -> str:
        """Get full path and name of Quant Data Manager Console Application"""
        return self._QuantDataManager

    @property
    def DataDirectory(self) -> str:
        """Get full path and name of the Data Directory"""
        theDataDirectory_SectionName = "data"
        theDataDirectory_Path        = self._config.getValue(theDataDirectory_SectionName,"path")
        theDataDirectory_Path        = os.path.join(os.getcwd(), theDataDirectory_Path)        
        return theDataDirectory_Path

    @property
    def SymbolListFileName(self) -> str:
        """Get full path and name of the Symbols List"""
        theDataDirectory_SectionName = "data"
        theSymbolListFileName        = self._config.getValue(theDataDirectory_SectionName,"symbollist")
        theSymbolListFileName        = os.path.join(os.getcwd(), self.DataDirectory,theSymbolListFileName)          
        return theSymbolListFileName

    def _getBatFileName(self,anOption : str) -> str:
        """check config file at 'bat'-section for an option,
           returns option value on success
        """
        theBatchFile_Path    = "bat" # .bat file directory = bat
        theBatchFile_Name    = self._config.getValue("quantdatamanager",anOption)
        theBatchFile_Program = os.path.join(os.getcwd(), theBatchFile_Path, theBatchFile_Name)        

        theFilePath = pathlib.Path(theBatchFile_Program)
        if not theFilePath.is_file():
            logger.error(f"Batch File not found at '{theFilePath}'.")
            raise FileNotFoundError 

        return theBatchFile_Program

    def updateSymbolsList(self) -> bool:
        """call Quant Data Manager to import list of symbols to csv-file"""
        # remove old outputfile before calling Quant Data Manager
        try:
            os.remove(self.SymbolListFileName)
        except OSError as e:
            # https://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred

        # calling QuantDataManager via .bat file
        theBatchFile = self._getBatFileName("getsymbols")

        # build the batch command with command line arguments
        theCommandList = [theBatchFile, 
                          self.QuantDataManagerFileName,
                          self.SymbolListFileName]
        isOk = self.BatchRun(theCommandList)
        return isOk

    def BatchRun(self,aCommandList : list) -> bool:
        """call Quant Data Manager with a list of commands"""
        try:
            logger.info("calling Quant Data Manager:")
            theCommands = ' '.join(map(str, aCommandList)) # source=https://www.decalage.info/en/python/print_list
            logger.debug(f">Commands ='{theCommands}'")
            # source=https://stackoverflow.com/questions/41171791/how-to-suppress-or-capture-the-output-of-subprocess-run
            theResult = subprocess.run(
                            aCommandList, 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=True, check=True,text=True)
            # source= https://www.python-forum.de/viewtopic.php?t=39382
            for line in theResult.stdout.splitlines():
                logger.info(f"> {line}")
            for line in theResult.stderr.splitlines():
                logger.warning(f"> {line}")  
            if theResult.returncode != 0:
                logger.warning(f"Returncode = {theResult.returncode}")
                batchRunSuccess = False
            else:
                batchRunSuccess = True            
        except Exception as inst:
            logger.error(type(inst))     # the exception instance
            logger.error(inst.args)      # arguments stored in .args
            logger.error(inst)           # __str__ allows args to be printed directly
            batchRunSuccess = False
        return batchRunSuccess

def main():
    logger.info("--- Class for calling the QuantDataManger on windows ---")

if __name__ == '__main__':
    main()    
