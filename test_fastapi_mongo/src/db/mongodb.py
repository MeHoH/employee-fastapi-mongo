import aiofiles
from bson import json_util
from motor import motor_asyncio
from core.config import settings


DATABASE_URL = settings.mongo_settings.mongodb_url

client = motor_asyncio.AsyncIOMotorClient(f"{DATABASE_URL}")
db = client.employees
collection = db.empl_collection


async def create_employees_collection():
    async with aiofiles.open('db/employees.json', mode='r') as f:
        contents = await f.read()
    data = json_util.loads(contents)
    collection.insert_many(data)
    collection.create_index('email', unique=True)
