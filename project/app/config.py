import os


SECRET_KEY = 'secret-key'
PER_PAGE = 5
DB_LOGIN=os.environ.get("DB_LOGIN")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
DB_IP=os.environ.get("DB_IP")
DB_NAME=os.environ.get("DB_NAME")
DB_PORT=str(os.environ.get("DB_PORT"))


# SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
#SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_LOGIN}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://nail:nail@172.20.0.23:3306/nail_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')

# . ve/bin/activate
# cd app
#flask run