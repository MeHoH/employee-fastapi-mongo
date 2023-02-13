from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from starlette.responses import JSONResponse

from core.dependens import get_motor_client
from schemas.employee import EmployeeModel, UpdateEmployeeModel

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create new employee",
             description="Create new employee", name="POST employee",
             response_description="Successfully create new employee", response_model=EmployeeModel)
async def create_employee(employee: EmployeeModel = Body(...), client: AsyncIOMotorClient = Depends(get_motor_client)):
    employee = jsonable_encoder(employee)
    del employee['_id']
    new_employee = await client.insert_one(employee)
    created_employee = await client.find_one({"_id": ObjectId(new_employee.inserted_id)})
    created_employee['_id'] = str(created_employee['_id'])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_employee)


@router.get("/", status_code=status.HTTP_200_OK, summary="List all employees",
            description="List all employees", name="POST employee",
            response_description="Successfully get list all employees", response_model=list[EmployeeModel])
async def list_employees(client: AsyncIOMotorClient = Depends(get_motor_client)):
    employees = await client.find().to_list(1000)
    return employees


@router.get(
    "/{id}", response_description="Get a single employee", response_model=EmployeeModel
)
async def show_employee(id: str, client: AsyncIOMotorClient = Depends(get_motor_client)):
    if (employee := await client.find_one({"_id": ObjectId(id)})) is not None:
        return employee

    raise HTTPException(status_code=404, detail=f"Employee {id} not found")


@router.put("/{id}", response_description="Update a employee", response_model=EmployeeModel)
async def update_employee(id: str, employee: UpdateEmployeeModel = Body(...),
                          client: AsyncIOMotorClient = Depends(get_motor_client)):
    employee = {k: v for k, v in employee.dict().items() if v is not None}

    if len(employee) >= 1:
        update_result = await client.update_one({"_id": ObjectId(id)}, {"$set": employee})

        if update_result.modified_count == 1:
            if (
                    updated_employee := await client.find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_employee

    if (existing_employee := await client.find_one({"_id": ObjectId(id)})) is not None:
        return existing_employee

    raise HTTPException(status_code=404, detail=f"Employee {id} not found")


@router.delete("/{id}", response_description="Delete a employee")
async def delete_employee(id: str, client: AsyncIOMotorClient = Depends(get_motor_client)):
    delete_result = await client.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=f"Employee {id} was delete!")

    raise HTTPException(status_code=404, detail=f"Employee {id} not found")
