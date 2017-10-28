echo off
set PYTHONPATH=collectopiniondefenses
python collectopiniondefenses/main.py -%1 configuration.txt
pause
