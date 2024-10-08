from faker import Faker
from .models import Company, Employee
from datetime import datetime
import random as rd

fake = Faker()

industries = ['Steel', 'Renewable Energy', 'Aviation', 'Health', 'Engineering', 'IT Consulting']

def create_fake_employee(employee_id: int) -> Employee:
    created_at = fake.date_time_this_year()
    return Employee(
        id=employee_id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        job_title=fake.job(),
        email=fake.email(),
        created_at=created_at,
        updated_at=created_at,
    )

def create_fake_company(company_id: int, num_employees: int) -> Company:
    created_at = fake.date_time_this_year()
    employees = [create_fake_employee(i) for i in range(1, num_employees + 1)]
    
    # Generate a random valuation between 10 million and 1 billion
    valuation = round(rd.uniform(10_000_000, 1_000_000_000), 2)
    return Company(
        id=company_id,
        name=fake.company(),
        industry=rd.choice(industries),
        created_at=created_at,
        updated_at=created_at,
        employees=employees,
        valuation=valuation,
    )

def get_fake_companies(num_companies: int = 300) -> list:
    return [create_fake_company(i, fake.random_int(min=5, max=20)) for i in range(1, num_companies + 1)]
