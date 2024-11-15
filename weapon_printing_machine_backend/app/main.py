from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import engine, Base, get_db, SessionLocal
from .routers import auth, customizations, weapons, print_jobs
from .init_data import initialize_weapon_data
from fastapi.middleware.cors import CORSMiddleware

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Configuration (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
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
    # Initialize database with predefined weapon data
    with SessionLocal() as db:
        initialize_weapon_data(db)
