cd %~dp0
call venv\Scripts\activate.bat
python initial.py
python test.py
python mask.py
python output.py