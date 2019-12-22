@echo off
rem #
rem # Copyright 2019 Heinrich Gerull
rem #
rem # Licensed under the GNU GENERAL PUBLIC LICENSE version 3
rem # you may not use this file except in compliance with the License.
rem # You may obtain a copy of the License at
rem #
rem #     https://www.gnu.org/licenses/gpl-3.0.html
rem #
rem # Unless required by applicable law or agreed to in writing, software
rem # distributed under the License is distributed on an "AS IS" BASIS,
rem # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
rem # See the License for the specific language governing permissions and
rem # limitations under the License
rem ----------------------------
rem call Quant Data Manager Console, passed as parameter 1
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
echo "%~f1" -de symbols=%2 timeframe=%3 outputdir=%4
"%~f1" -de symbols=%2 timeframe=%3 outputdir=%4
goto continue

rem error handling 
:error_occured
rem source = https://www.robvanderwoude.com/parameters.php
rem exit with error code 2
exit /B 2

:continue
rem exit without error
exit /B 0
