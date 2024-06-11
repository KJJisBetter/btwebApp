import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7q)+870p=)21%ew(3og)+l$4hieg)($a8i5su-&zx&)2f=*9(3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # print('SQLALCHEMY_DATABASE_URI:', SQLALCHEMY_DATABASE_URI)