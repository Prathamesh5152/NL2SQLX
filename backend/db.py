import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

print("ENV LOADED:")
print("MYSQL_USER =", MYSQL_USER)
print("MYSQL_PASSWORD =", MYSQL_PASSWORD)
print("MYSQL_HOST =", MYSQL_HOST)
print("MYSQL_PORT =", MYSQL_PORT)
print("MYSQL_DB =", MYSQL_DB)

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
print("DATABASE_URL =", DATABASE_URL)

engine = create_engine(DATABASE_URL)
print("ENGINE CREATED SUCCESSFULLY")
