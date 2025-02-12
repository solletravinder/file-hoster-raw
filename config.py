import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-key")
    SPACE_NAME = os.getenv("SPACE_NAME")
    REGION = os.getenv("REGION_NAME")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    SECRET_KEY_DO = os.getenv("SECRET_KEY_DO")
    ENDPOINT_URL = os.getenv("ENDPOINT_URL")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", '5242880000'))  # 5GB max file size
    ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "").split(","))

config = Config()
