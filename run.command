cd "$(dirname "$0")"
source ./venv/bin/activate
python3 initial.py
python3 test.py
python3 mask.py
python3 output.py