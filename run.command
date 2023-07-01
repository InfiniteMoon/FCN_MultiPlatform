cd "$(dirname "$0")"
source activate fcnM
python3 initial.py
python3 test.py
python3 mask.py
python3 output.py