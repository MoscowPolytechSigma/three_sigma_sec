import os

SECRET_KEY = 'secret-key'
PER_PAGE = 5

# SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2448_lab6:std_2448_lab6@std-mysql.ist.mospolytech.ru/std_2448_lab6'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
