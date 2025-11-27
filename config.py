import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
DB = os.getenv("DB")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")