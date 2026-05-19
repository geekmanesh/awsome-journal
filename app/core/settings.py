from environs import env

env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
ALGORITHM = env.str("ALGORITHM")
DATABASE_URL = env.str("DATABASE_URL")
