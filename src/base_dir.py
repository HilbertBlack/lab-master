from pathlib import Path
import sys


BASE_DIR = ""

if (getattr(sys,"frozen",False)):
    BASE_DIR  = Path(sys._MEIPASS).resolve()
else:
    BASE_DIR = Path(__file__).resolve().parent
