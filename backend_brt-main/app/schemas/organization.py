from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

# Shared properties
class OrganizationBase(BaseModel):
    name: str
    industry: Optional[str] = None
    size: Optional[int] = None
    address: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None

# Properties to receive on organization creation
class OrganizationCreate(OrganizationBase):
    pass

# Properties to receive on organization update
class OrganizationUpdate(OrganizationBase):
    name: Optional[str] = None

# Properties shared by models stored in DB
class OrganizationInDBBase(OrganizationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties to return to client
class Organization(OrganizationInDBBase):
    pass

# Properties stored in DB
class OrganizationInDB(OrganizationInDBBase):
    pass
