from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import random as rd


from fake_coy_api.models import Company, Employee, CompanyWithoutEmployees, PaginatedResponse
from fake_coy_api.dependencies import verify_api_key
from fake_coy_api.data import get_fake_companies

# Initialize FastAPI app and set Swagger docs to root
app = FastAPI(docs_url="/")

# In-memory storage for fake data
companies = get_fake_companies()




@app.get("/companies", response_model=PaginatedResponse)
def get_companies(
    api_key: str = Depends(verify_api_key),
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    industry: Optional[str] = None,
    start_dt: Optional[datetime] = None,
    end_dt: Optional[datetime] = None,
):
    """Get paginated list of companies with optional filtering by industry and dates."""
    if end_dt and not start_dt:
        raise HTTPException(status_code=400, detail="end_dt cannot be used without start_dt")

    filtered_companies = [
        c for c in companies 
        if (industry is None or c.industry == industry) and
           (start_dt is None or c.updated_at >= start_dt) and
           (end_dt is None or c.updated_at <= end_dt)
    ]

    total = len(filtered_companies)
    start = (page - 1) * size
    end = start + size
    paginated_companies = filtered_companies[start:end]
    total_pages = (total + size - 1) // size

    # Convert to CompanyWithoutEmployees model
    paginated_companies_without_employees = [
        CompanyWithoutEmployees(**company.dict(exclude={"employees"}))
        for company in paginated_companies
    ]

    return {
        "items": paginated_companies_without_employees,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }

@app.get("/companies/{company_id}/employees", response_model=PaginatedResponse)
def get_employees(
    company_id: int,
    api_key: str = Depends(verify_api_key),
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    job_title: Optional[str] = None,
    start_dt: Optional[datetime] = None,
    end_dt: Optional[datetime] = None,
):
    """Get paginated list of employees for a specific company with optional filtering by job title and dates."""
    if end_dt and not start_dt:
        raise HTTPException(status_code=400, detail="end_dt cannot be used without start_dt")

    company = next((c for c in companies if c.id == company_id), None)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    filtered_employees = [
        e for e in company.employees 
        if (job_title is None or e.job_title == job_title) and
           (start_dt is None or e.updated_at >= start_dt) and
           (end_dt is None or e.updated_at <= end_dt)
    ]
    
    total = len(filtered_employees)
    start = (page - 1) * size
    end = start + size
    paginated_employees = filtered_employees[start:end]
    total_pages = (total + size - 1) // size

    return {
        "items": paginated_employees,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }


@app.get("/companies/update-valuation", response_model=List[dict])
def update_random_companies_valuation(
    api_key: str = Depends(verify_api_key),
):
    """Randomly pick up to 10 companies and update their valuation."""
    # Pick up to 10 random companies
    selected_companies = rd.sample(companies, k=min(10, len(companies)))
    
    updated_companies = []
    
    for company in selected_companies:
        # Update the valuation to a new random value between 10 million and 1 billion
        company.valuation = round(rd.uniform(10_000_000, 1_000_000_000), 2)

        # Update the updated_at timestamp to the current time
        company.updated_at = datetime.utcnow()
        
        # Append the updated company's id and name to the list
        updated_companies.append({
            "id": company.id,
            "name": company.name
        })
    
    # Return the list of updated companies
    return updated_companies