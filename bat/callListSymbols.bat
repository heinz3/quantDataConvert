@echo off
rem ----------------------------
rem call Quant Data Manager Console, passed as parameter 1
rem parameter 2 = full path and name of CSV-File
rem ----------------------------
rem source = https://www.robvanderwoude.com/parameters.php

rem check for parameter 1
IF "%~1"=="" GOTO error_occured

rem switch to target drive:
rem drive = "%~d1"
%~d1

rem switch to target directory:
rem path = "%~p1"
cd "%~p1"

rem call the program
rem source = http://steve-jansen.github.io/guides/windows-batch-scripting/part-2-variables.html
rem Quant Data Manager Command Reference = https://strategyquant.com/doc/quant-data-manager-command-line-interface-help/
echo "%~f1" -l csv=%2
"%~f1" -l csv=%2
goto continue

rem error handling 
:error_occured
rem source = https://www.robvanderwoude.com/parameters.php
rem exit with error code 2
exit /B 2

:continue
rem exit without error
exit /B 0
