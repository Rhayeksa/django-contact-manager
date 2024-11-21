import os
import urllib.parse

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_DB_USERNAME = os.getenv("MYSQL_DB_USERNAME")
MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD")
MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST")
MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT")

URI = f"mysql+pymysql://{MYSQL_DB_USERNAME}:{urllib.parse.quote_plus(MYSQL_DB_PASSWORD)}@{MYSQL_DB_HOST}:{MYSQL_DB_PORT}/{MYSQL_DB}"

engine = create_engine(url=URI, pool_pre_ping=True)
session = sessionmaker(bind=engine)
session = session()
