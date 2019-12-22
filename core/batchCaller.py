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
class for calling QuantDataManger on windows
"""

import logging
logger = logging.getLogger(__name__)
# ----------------------------------------------------------------------------
import sys, os, configparser, pathlib, subprocess, errno
import core.basicConfigReader as miniConfig
import core.quantDataConverter as dataConverter
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
       
        # calling QuantDataManager via .bat file
        # .bat file location and name = bat/callProgram.bat
        theBatchFile_Path    = "bat"
        theBatchFile_Name    = "callProgram.bat"
        theBatchFile_Program = os.path.join(os.getcwd(), theBatchFile_Path, theBatchFile_Name)

        theFilePath = pathlib.Path(theBatchFile_Program)
        if not theFilePath.is_file():
            logger.error(f"Batch File not found at '{theFilePath}'.")
            raise FileNotFoundError 
        self._BatchFile = theBatchFile_Program

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
        """call Quant Data Manager to export list of symbols to csv-file"""
        # get temporary file name
        theTempfileName = dataConverter.getTempFileName()

        # remove old outputfile before calling Quant Data Manager
        dataConverter.removeFile(self.SymbolListFileName)

        # calling QuantDataManager via .bat file
        theBatchFile = self._getBatFileName("getsymbols")

        # build the batch command with command line arguments
        theCommandList = [theBatchFile, 
                          self.QuantDataManagerFileName,
                          theTempfileName]
        isOk = self.BatchRun(theCommandList)
        if not isOk:
            return False

        # converting the CSV-File into pandas compatible format            
        isOk = dataConverter.convertSymbolList(theTempfileName,self.SymbolListFileName)
        return isOk

    def updateQuotes(self) -> bool:
        """call Quant Data Manager to update all quotes"""
        # calling QuantDataManager via .bat file
        theBatchFile = self._getBatFileName("updatequotes")

        # build the batch command with command line arguments
        theCommandList = [theBatchFile, 
                          self.QuantDataManagerFileName
                         ]
        isOk = self.BatchRun(theCommandList)
        return isOk

    def exportQuotes(self,aTimeframe='M1') -> bool:
        """call Quant Data Manager to export all quotes to csv-files"""
        # calling QuantDataManager via .bat file
        theBatchFile = self._getBatFileName("exportquotes")        

        # get list of symbols
        theSymbols = dataConverter.getSymbolsList(self.SymbolListFileName)

        for aSymbol in theSymbols:
            logger.info(f"exporting '{aSymbol}' to CSV")
            theResult = True

            # build the batch command with command line arguments
            theCommandList = [theBatchFile, 
                              self.QuantDataManagerFileName,
                              aSymbol,
                              aTimeframe.upper(),
                              self.DataDirectory]
            isOk = self.BatchRun(theCommandList)
            theResult = theResult and isOk
            if isOk:
                theSourceFileName = f"{aSymbol}-{aTimeframe.upper()}-No Session.csv"
                theSourceFileName = os.path.join(self.DataDirectory,theSourceFileName)
                theTargetFileName = f"{aSymbol}-{aTimeframe.upper()}.csv"
                theTargetFileName = os.path.join(self.DataDirectory,theTargetFileName)
                # convert the quotes into pandas compatible format     
                isOk = dataConverter.convertQuotes(theSourceFileName,theTargetFileName)               
                theResult = theResult and isOk
        return theResult

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
