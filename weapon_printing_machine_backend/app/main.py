from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import engine, Base, get_db, SessionLocal
from .routers import auth, customizations, weapons, print_jobs
from .init_data import initialize_admin_user, initialize_weapon_data, initialize_weapon_parts_data
from fastapi.middleware.cors import CORSMiddleware
from .models import Weapon, WeaponPart  # Add your model import for checking data existence

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Configuration (for production, specify actual origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(customizations.router, prefix="/customize", tags=["Customizations"])
app.include_router(weapons.router, prefix="/weapons", tags=["Weapons"])
app.include_router(print_jobs.router, prefix="/print-jobs", tags=["Print Jobs"])

# Health check endpoint
@app.get("/status")
def status():
    return {"status": "OK"}

# Application startup event
@app.on_event("startup")
def startup_event():
    with SessionLocal() as db:
        # Initialize weapon data if not already initialized
        if not db.query(Weapon).first():  # Check if weapon data exists
            initialize_weapon_data(db)

        # Initialize weapon parts data if not already initialized
        if not db.query(WeaponPart).first():  # Check if weapon parts exist
            initialize_weapon_parts_data(db)
        initialize_admin_user(db)
# Application shutdown event (if needed)
@app.on_event("shutdown")
def shutdown_event():
    # Handle any cleanup tasks
    pass
