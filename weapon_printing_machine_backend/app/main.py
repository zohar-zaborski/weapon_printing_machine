from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import engine, Base, get_db, SessionLocal
from .routers import auth, customizations, weapons, print_jobs
from .init_data import initialize_weapon_data
from fastapi.middleware.cors import CORSMiddleware
from .models import Weapon  # Add your model import for checking data existence

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Configuration (for production, specify actual origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(customizations.router, prefix="/customizations", tags=["Customizations"])
app.include_router(weapons.router, prefix="/weapons", tags=["Weapons"])
app.include_router(print_jobs.router, prefix="/print_jobs", tags=["Print Jobs"])

# Health check endpoint
@app.get("/status")
def status():
    return {"status": "OK"}

# Application startup event
@app.on_event("startup")
def startup_event():
    with SessionLocal() as db:
        # Initialize weapon data if it's not already initialized
        if not db.query(Weapon).first():  # Check if weapon data exists
            initialize_weapon_data(db)

# Application shutdown event (if needed)
@app.on_event("shutdown")
def shutdown_event():
    # Handle any cleanup tasks
    pass
