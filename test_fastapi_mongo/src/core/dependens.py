from functools import lru_cache
from logging import Logger

from fastapi import Depends
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import Settings, settings
from core.logger import logger


@lru_cache()
def get_settings() -> Settings:
    return settings


@lru_cache()
def get_logger() -> Logger:
    return logger


def get_motor_client(settings: Settings = Depends(get_settings)) -> AsyncIOMotorClient:
    client = motor_asyncio.AsyncIOMotorClient(settings.mongo_settings.mongodb_url)
    db = client.employees
    collection = db.empl_collection

    return collection
