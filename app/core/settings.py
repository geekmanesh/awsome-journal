from environs import env
from fastapi.templating import Jinja2Templates

env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
ALGORITHM = env.str("ALGORITHM")

DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PORT = env.str("DB_PORT")
DB_HOST = env.str("DB_HOST")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
