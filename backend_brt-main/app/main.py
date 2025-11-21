from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import datetime


from app.api.api import api_router
from app.core.config import settings
from app.db.postgres import Base, engine, get_db
from app.db.mongodb import get_mongodb

# Create PostgreSQL tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    """
    Root endpoint
    """
    return {"message": "Welcome to the Business Resilience Tool API", "status": "online"}

@app.get("/test")
def test_endpoint():
    """
    Test endpoint that doesn't require authentication or database access
    """
    return {"test": "success", "time": str(datetime.datetime.now())}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    """
    try:
        # Check PostgreSQL connection
        db.execute(text("SELECT 1"))
        postgres_status = "healthy"
    except Exception as e:
        postgres_status = f"unhealthy: {str(e)}"
    
    # Check MongoDB connection
    try:
        # This will raise an exception if MongoDB is not available
        next(get_mongodb())
        mongodb_status = "healthy"
    except Exception as e:
        mongodb_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "ok",
        "database_status": {
            "postgres": postgres_status,
            "mongodb": mongodb_status
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    