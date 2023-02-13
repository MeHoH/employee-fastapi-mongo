from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from pydantic.schema import datetime
from pydantic.typing import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class EmployeeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    age: int = Field(..., gt=0)
    company: str = Field(...)
    join_date: datetime = Field(...)
    job_title: str = Field(...)
    gender: str = Field(...)
    salary: int = Field(..., gt=0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Flynn Vang",
                "email": "turpis.non@Nunc.edu",
                "age": 69,
                "company": "Twitter",
                "join_date": "2003-12-28T18:18:10-08:00",
                "job_title": "janitor",
                "gender": "female",
                "salary": 9632
            }
        }


class UpdateEmployeeModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    age: Optional[int]
    company: Optional[str]
    join_date: Optional[datetime]
    job_title: Optional[str]
    gender: Optional[str]
    salary: Optional[int]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Flynn Vang",
                "email": "turpis.non@Nunc.edu",
                "age": 69,
                "company": "Twitter",
                "join_date": "2003-12-28T18:18:10-08:00",
                "job_title": "janitor",
                "gender": "female",
                "salary": 9632
            }
        }
