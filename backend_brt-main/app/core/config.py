import os
from typing import Any, List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic.networks import PostgresDsn
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Business Resilience Tool"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # PostgreSQL
    # Support both direct connection string and individual components
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("SQLALCHEMY_DATABASE_URI")
    
    # Individual PostgreSQL connection parameters (used if SQLALCHEMY_DATABASE_URI is not provided)
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "business_resilience")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_postgres_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str) and v:
            return v
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "business_resilience")
    
    # Document types
    DOCUMENT_TYPES: List[str] = [
        "SOP",
        "RISK_REGISTER",
        "ROLE_CHART",
        "PROCESS_MANUAL",
        "ARCHITECTURE_DIAGRAM",
        "INCIDENT_LOG",
        "VENDOR_CONTRACT",
        "POLICY",
        "DR_BCP_PLAN",
        "CHAT_HISTORY",
        "EXTERNAL_DOCUMENT"
    ]
    
    class Config:
        case_sensitive = True

settings = Settings()
