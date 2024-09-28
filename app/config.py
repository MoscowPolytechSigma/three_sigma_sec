import os


SECRET_KEY = 'secret-key'
PER_PAGE = 5

# SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2448_lab6:std_2448_lab6@std-mysql.ist.mospolytech.ru/std_2448_lab6'
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://nail:nail@127.0.0.1:3306/nail_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')

# . ve/bin/activate
# cd app
#flask run