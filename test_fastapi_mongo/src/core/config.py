from os import path
from enum import Enum
from ipaddress import IPv4Address
from typing import Optional, Union

from fastapi.responses import ORJSONResponse
from pydantic import BaseSettings, BaseModel, DirectoryPath, PositiveInt, AnyUrl

from core.logger import LOGGING


class Base(BaseModel):
    base_dir: DirectoryPath = path.dirname(path.dirname(path.abspath(__file__)))
    project_name: str = 'employee'


class SettingsFastapiApp(BaseModel):
    description: str = 'Service for employee API'
    docs_url: AnyUrl = '/api/openapi'
    openapi_url: AnyUrl = '/api/openapi.json'
    default_response_class: ORJSONResponse = ORJSONResponse


class LogLevelEnum(str, Enum):
    debug = 'debug'
    info = 'info'
    warning = 'warning'
    error = 'error'
    critical = 'critical'


class SettingsUvicorn(BaseSettings):
    host: IPv4Address = '127.0.0.1'
    port: PositiveInt = 8000
    log_config: Optional[Union[dict, str]] = LOGGING
    log_level: LogLevelEnum = LogLevelEnum.info
    debug: bool

    class Config:
        env_file = '.env'


class MongoSettings(BaseSettings):
    mongodb_url = "mongodb://mongodbuser:mongodb_password@mongodb:27017/"


class Settings(BaseModel):
    base: Base = Base()
    settings_fastapi_app: SettingsFastapiApp = SettingsFastapiApp()
    settings_uvicorn: SettingsUvicorn = SettingsUvicorn()
    mongo_settings: MongoSettings = MongoSettings()


settings = Settings()
