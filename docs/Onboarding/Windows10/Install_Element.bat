@ECHO OFF
ECHO Installing Element Desktop...
start /w "" "%~dp0\Element Setup.exe" /s
ECHO Element Desktop for Windows 10 installed.
copy "%~dp0\config.json" "C:\Users\%username%\AppData\Roaming\Element\config.json"
ECHO Copying config.json file over. Done!
PAUSE