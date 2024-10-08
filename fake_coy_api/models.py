from pydantic import BaseModel
from typing import List, Any
from datetime import datetime

class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    job_title: str
    email: str
    created_at: datetime
    updated_at: datetime

class Company(BaseModel):
    id: int
    name: str
    industry: str
    created_at: datetime
    updated_at: datetime
    employees: List[Employee]
    valuation: float

class CompanyWithoutEmployees(BaseModel):
    id: int
    name: str
    industry: str
    created_at: datetime
    updated_at: datetime
    valuation: float


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    total_pages: int