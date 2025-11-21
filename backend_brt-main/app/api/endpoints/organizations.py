from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Organization])
def read_organizations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve organizations.
    """
    if current_user.is_superuser:
        organizations = db.query(models.Organization).offset(skip).limit(limit).all()
    else:
        # Regular users can only see their own organization
        organizations = [db.query(models.Organization).filter(models.Organization.id == current_user.org_id).first()]
    return organizations

@router.post("/", response_model=schemas.Organization)
def create_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_in: schemas.OrganizationCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new organization.
    """
    organization = models.Organization(**organization_in.dict())
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization

@router.get("/{organization_id}", response_model=schemas.Organization)
def read_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get organization by ID.
    """
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Check if user has access to this organization
    if not current_user.is_superuser and current_user.org_id != organization.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return organization

@router.put("/{organization_id}", response_model=schemas.Organization)
def update_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: str,
    organization_in: schemas.OrganizationUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an organization.
    """
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    update_data = organization_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(organization, field, value)
    
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization

@router.delete("/{organization_id}", response_model=schemas.Organization)
def delete_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an organization.
    """
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    db.delete(organization)
    db.commit()
    return organization
