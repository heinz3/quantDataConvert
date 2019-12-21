# -*- coding: UTF-8 -*-
#
"""
Convert intraday stock and forex quotes from QuantDataManager to format readable with Zipline
"""

import logging
logger = logging.getLogger(__name__)
# ----------------------------------------------------------------------------
import sys, os, argparse 
from datetime import datetime
import core.basicLogger as minilog
import core.basicConfigReader as miniConfig
import core.batchCaller as quantBatchCaller
# ----------------------------------------------------------------------------

def main():
    # -------------------------------------------
    # initiate logging
    minilog.initiate(logging.INFO)

    # program start message
    logger.info(f"""--- START '{sys.argv[0]}' on {datetime.now().strftime("%Y-%b-%d")} ---""")

    # -------------------------------------------
    # command line parser 

    # initiate the command line parser
    parser = argparse.ArgumentParser(
            prog=os.path.basename(sys.argv[0]), # source = https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
            description="convert quotes from QuantDataManager to Zipline",
            epilog="default parameters are in '/config/config.cnf'")
    
    # add long and short command line arguments
    parser.add_argument("--configfile", "-c", help="name of config file")
        

    # read arguments from the command line
    args = parser.parse_args()
    # -------------------------------------------    
    # check for command line argument --configfile file
    if args.configfile:
        theConfig = miniConfig.defaultConfig(args.configfile)
    else :
        # no config file specified, taking default config file
        theConfig = miniConfig.defaultConfig()      
    logger.info(f"Taking configuration from '{theConfig.configFileName}'")
    logger.info(" ")
    # -------------------------------------------
    # connecting to Quant Data Manager
    theDataManager = quantBatchCaller.callQuantDataManager(theConfig)

    # # -------------------------------------------
    # logger.info("--- STEP 1 of 3: updating list of symbols  ---")
    # isOk = theDataManager.updateSymbolsList()
    # if not isOk:
    #     logger.critical("update of symbols list failed")
    #     sys.exit(1)  
    # logger.info(" ")
    # # -------------------------------------------
    # logger.info("--- STEP 2 of 3: updating quotes  ---")
    # isOk = theDataManager.updateQuotes()
    # if not isOk:
    #     logger.critical("update of quotes failed")
    #     sys.exit(1)      
    # logger.info(" ")
    # -------------------------------------------    
    logger.info("--- STEP 3 of 3: exporting to csv  ---")
    isOk = theDataManager.exportQuotes()    
    if not isOk:
        logger.critical("export to CSV failed")
        sys.exit(1)      
    logger.info(" ")

    # -------------------------------------------
    # program end message
    logger.info(f"--- END '{os.path.basename(sys.argv[0])}' ---")

if __name__ == '__main__':
    main()    
