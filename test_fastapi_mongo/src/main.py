import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.logger import logger
from core.router import api_router
from db.mongodb import client, create_employees_collection

app = FastAPI(
    title=settings.base.project_name,
    description=settings.settings_fastapi_app.description,
    docs_url=settings.settings_fastapi_app.docs_url,
    openapi_url=settings.settings_fastapi_app.openapi_url,
    default_response_class=settings.settings_fastapi_app.default_response_class
)


@app.on_event('startup')
async def startup():
    logger.info('Started')
    db = client.employees
    names = await db.list_collection_names()
    if "empl_collection" not in names:
        await create_employees_collection()


@app.on_event('shutdown')
async def shutdown():
    logger.info('Shutdown')
    client.close()


app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.settings_uvicorn.host.__str__(),
        port=settings.settings_uvicorn.port,
        log_config=settings.settings_uvicorn.log_config,
        log_level=settings.settings_uvicorn.log_level,
    )
