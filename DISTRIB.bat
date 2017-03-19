@echo off

if [%1]==[] (
	set /p TMP="DISTRIB.bat Must be called with a valid ouput path as first argument !"
	exit /b
)

if [%2]==[] (
	set /p TMP="DISTRIB.bat Must be called with a Maya Name as second argument!"
	exit /b
)

robocopy /MIR /S /NFL /NDL /NJH *.* %~dp0\Maya %1\%2 /XF DISTRIB.bat /XD examples