import os
from dotenv import load_dotenv

load_dotenv()

UPBIT_ACCESS_KEY = os.environ.get('UPBIT_ACCESS_KEY')
UPBIT_SECRET_KEY = os.environ.get('UPBIT_SECRET_KEY')

if not UPBIT_ACCESS_KEY:
    raise ValueError("UPBIT_ACCESS_KEY not found")
if not UPBIT_SECRET_KEY:
    raise ValueError("UPBIT_SECRET_KEY not found")