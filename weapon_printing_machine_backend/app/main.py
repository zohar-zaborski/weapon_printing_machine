# app/main.py
from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from .routers import auth, customizations, weapons, print_jobs
from fastapi.middleware.cors import CORSMiddleware
from .init_data import initialize_weapon_data

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize app instance
app = FastAPI()

# Initialize predefined weapon data
def startup_event():
    db = SessionLocal()
    initialize_weapon_data(db)  # Call the function to add predefined weapon data
    db.close()

# Run the startup event function when the application starts
app.add_event_handler("startup", startup_event)

# Configure CORS settings (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust based on your requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(customizations.router, prefix="/customizations", tags=["Customizations"])
app.include_router(weapons.router, prefix="/weapons", tags=["Weapons and Parts"])
app.include_router(print_jobs.router, prefix="/print_jobs", tags=["Print Jobs"])

# Health check endpoint
@app.get("/status")
def status():
    return {"status": "OK"}
