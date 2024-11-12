import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Fetch database credentials from environment variables or set default values
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'cookie_db')

engine = create_engine(
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}',
    pool_size=20,
    max_overflow=0
)

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
