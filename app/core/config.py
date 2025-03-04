import os
import sys
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from app.core.constants import FORMAT

load_dotenv()


def setup_logging(name):
    """Setup logging"""
    logger = logging.getLogger(name)
    for h in logger.handlers:
        logger.removeHandler(h)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger


LOG = setup_logging(__name__)


async def log_entry_point(req):
    LOG.debug("[%s] - %s", req.method, req.url)


class Settings(BaseSettings):

    API_V1_STR: str = "/v1"
    API_KEY: str = os.environ.get("API_KEY")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_TEST_DB: str = os.environ.get("POSTGRES_TEST_DB")
    POSTGRES_TEST_HOST: str = os.environ.get("POSTGRES_TEST_HOST")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    TEST_DATABASE_URL: str = os.environ.get("TEST_DATABASE_URL")
    ENV: str = os.environ.get("ENV")

    class Config:
        case_sensitive = True


settings = Settings()
