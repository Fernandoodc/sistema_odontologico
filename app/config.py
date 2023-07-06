import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from filters import _jinja2_filter_strftime
load_dotenv()

templates = Jinja2Templates(directory="templates")
templates.env.filters["strftime"] = _jinja2_filter_strftime
class Settings:
    PROJECT_TITLE: str = ""
    PROJECT_VERSION: str = "0.1"
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT")
    MYSQL_DB: str = os.getenv("MYSQL_DB")
    DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    ALGORITHM = "HS256"
    HASH = "pbkdf2:sha256"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    KEY_TOKEN: str = "access-token"
    VIDA_TOKEN : int =  2  #Horas de vida del token de sesion
settings = Settings()

