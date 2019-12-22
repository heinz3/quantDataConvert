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
module for converting QuantDataManager files
"""

import logging
logger = logging.getLogger(__name__)
# ----------------------------------------------------------------------------
import sys, os, errno, csv, configparser, pathlib, tempfile
from tqdm import tqdm
# ----------------------------------------------------------------------------

def getTempFileName() -> str:
    """create temporary file name"""
    # source: https://stackoverflow.com/questions/26541416/generate-temporary-file-names-without-creating-actual-file-in-python
    temp_name = next(tempfile._get_candidate_names())
    default_tmp_dir = tempfile._get_default_tempdir()
   
    theFileName = os.path.join(default_tmp_dir, temp_name)        
    logger.debug(f"Temporary file name created:'{theFileName}'")
    return theFileName

def removeFile(aFileName : str) -> None:
    """delete a file"""
    try:
        os.remove(aFileName)
    except OSError as e:
        # https://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred    

def convertSymbolList(nameOfSourceFile:str, nameOfDestinationFile:str) -> bool:
    """convert symbol list from QuantDataManager"""
    try:
        logger.debug(f"convert Quant Data Symbollist at '{nameOfSourceFile}' and save as '{nameOfDestinationFile}'")
        with open(nameOfSourceFile) as sourcefile:
            theReader = csv.DictReader(sourcefile, delimiter=',', quotechar='"')

            with open(nameOfDestinationFile, mode='w+t', newline='', encoding='UTF8') as destinationfile:
                theWriter = csv.DictWriter(destinationfile, 
                                           fieldnames= theReader.fieldnames,
                                           delimiter=',',
                                           quotechar='"', 
                                           quoting=csv.QUOTE_MINIMAL)
                theWriter.writeheader()
                for aRow in theReader:
                    # at column 'Date from' convert date format to ISO date
                    aDateValue = aRow['Date from']
                    theISOdateValue = aDateValue.replace('.','-')
                    aRow['Date from'] = theISOdateValue

                    # at column 'Date to' convert date format to ISO date
                    aDateValue = aRow['Date to']
                    theISOdateValue = aDateValue.replace('.','-')
                    aRow['Date to'] = theISOdateValue

                    for name,value in aRow.items():
                        logger.debug(f'{name}:{value}')

                    theWriter.writerow(aRow) # write a row to file
        fileConvertIsOk = True
    except Exception as inst:
        logger.error(type(inst))     # the exception instance
        logger.error(inst.args)      # arguments stored in .args
        logger.error(inst)           # __str__ allows args to be printed directly
        fileConvertIsOk = False
    finally:
        removeFile(nameOfSourceFile)
    return fileConvertIsOk

def getSymbolsList(nameOfCSVFile : str) -> list:
    """return the symbols in CSV File as list"""
    theResult = []
    try:
        logger.debug(f"read CSV symbollist at '{nameOfCSVFile}' and return as list")

        with open(nameOfCSVFile, mode='r+t') as sourcefile:
            theReader = csv.DictReader(sourcefile, delimiter=',', quotechar='"')
            for aRow in theReader:
                aSymbol = aRow['Symbol']
                theResult.append(aSymbol)
                logger.debug(f"Symbol='{aSymbol}'")
    except Exception as inst:
        logger.error(type(inst))     # the exception instance
        logger.error(inst.args)      # arguments stored in .args
        logger.error(inst)           # __str__ allows args to be printed directly
    return theResult

def getNumberOfLinesOfFile(nameOfTextFile:str) -> int:
    # source = https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
    lines = 0    
    buf_size = 1024 * 1024
    with open(nameOfTextFile, mode='rb') as f:
        read_f = f.raw.read
        buf = read_f(buf_size)
        while buf:
            lines += buf.count(b'\n')
            buf = read_f(buf_size)            
    return lines

def convertQuotes(nameOfSourceFile:str, nameOfDestinationFile:str) -> bool:
    """convert quotes from QuantDataManager Format to Zipline compatible format"""
    try:
        logger.debug(f"convert Quant Data Quotes from '{nameOfSourceFile}' and save as '{nameOfDestinationFile}'")

        # if destination file exists already, delete it
        removeFile(nameOfDestinationFile)

        theCSVfieldnames = ['date', 'open', 'high', 'low', 'close', 'volume']
        numberOfLines = getNumberOfLinesOfFile(nameOfSourceFile)

        with open(nameOfSourceFile) as sourcefile:
                        
            theReader = csv.reader(sourcefile, delimiter=',', quotechar='"')

            with open(nameOfDestinationFile, mode='w+t', newline='', encoding='UTF8') as destinationfile:
                theWriter = csv.DictWriter(destinationfile, 
                                           fieldnames= theCSVfieldnames,
                                           delimiter=',',
                                           quotechar='"', 
                                           quoting=csv.QUOTE_MINIMAL)
                theWriter.writeheader()
                # source= https://blog.nelsonliu.me/2016/07/30/progress-bars-for-python-file-reading-with-tqdm/
                for aRow in tqdm(theReader, total=numberOfLines ):
                    # at column 0 convert date format to ISO date
                    aDateValue = aRow[0]
                    anISOdateValue = aDateValue.replace('.','-')
                    
                    # at column 1 convert time format to ISO time
                    aTimeValue = aRow[1]
                    anISOtimeValue = f"T{aTimeValue}Z" # = timezone UTC

                    anOpen  = aRow[2]
                    aHigh   = aRow[3]
                    aLow    = aRow[4]
                    aClose  = aRow[5]
                    aVolume = aRow[6]

                    theWriter.writerow(
                        {'date'  : f"{anISOdateValue}{anISOtimeValue}", 
                         'open'  : f"{anOpen}", 
                         'high'  : f"{aHigh}" , 
                         'low'   : f"{aLow}" ,
                         'close' : f"{aClose}",
                         'volume': f"{aVolume}"
                        })

        # when conversion is complete, delete source-file
        removeFile(nameOfSourceFile)                    

        fileConvertIsOk = True
    except Exception as inst:
        logger.error(type(inst))     # the exception instance
        logger.error(inst.args)      # arguments stored in .args
        logger.error(inst)           # __str__ allows args to be printed directly
        fileConvertIsOk = False
    return fileConvertIsOk


def main():
    logger.info("--- Module for converting QuantDataManager files ---")

if __name__ == '__main__':
    main()    
