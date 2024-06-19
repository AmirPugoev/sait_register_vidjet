#config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# config.py
DB_SERVER = 'DESKTOP-KKHC1R6\\MSSQLSERVER01'
DB_NAME = 'dase'

MAIL_SERVER = 'connect.smtp.bz'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = '1032211672@pfur.ru'
MAIL_PASSWORD = '7i0ogq7L5NR1'

