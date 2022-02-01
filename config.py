import os
from dotenv import load_dotenv
from pathlib import Path


base_dir = Path(__file__).resolve().parent
env_file = base_dir / ".env"
load_dotenv(env_file)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("CLEARDB_DATABASE_URL")


class TestingConfig(Config):
    DB_FILE_PATH = base_dir / "tests" / "test.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_FILE_PATH}"
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DB_HOST = os.environ.get("")
    DB_USERNAME = os.environ.get("")
    DB_PASSWORD = os.environ.get("")
    DB_NAME = os.environ.get("")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_NAME}?charset=utf8mb4"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
