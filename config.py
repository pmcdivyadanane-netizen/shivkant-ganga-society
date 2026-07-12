import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")