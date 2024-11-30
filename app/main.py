from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import treatment_plan, availability

app = FastAPI(
    title="Dementia Treatment Planner",
    description="Rule-based expert system for generating dementia treatment plans",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(treatment_plan.router, prefix="/api/treatment-plan")
app.include_router(availability.router, prefix="/api/availability")


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Dementia Treatment Planner API",
        "version": "1.0.0",
        "endpoints": ["/api/treatment-plan", "/api/availability"]
    }
