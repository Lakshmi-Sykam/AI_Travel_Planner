import uuid
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.db.database import get_db, init_db
from backend.app.db.models import TripPlanModel, UserModel
from backend.app.schemas.trip_schema import (
    TripRequest,
    ModifyTripRequest,
    TripResponse,
    TripItinerary
)
from backend.app.schemas.auth_schema import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse
)
from backend.app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_optional_current_user,
    get_current_user
)
from backend.app.agents.graph import run_travel_planner
from backend.app.agents.llm import invoke_llm_json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("travel_planner.api")

# Initialize database
init_db()

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-Agent AI Travel Planning system with LangGraph, Groq LLM & User Authentication.",
    version="2.0.0",
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "llm_model": settings.GROQ_MODEL,
        "groq_configured": bool(settings.GROQ_API_KEY and settings.GROQ_API_KEY != "your_groq_api_key_here")
    }

# ================= AUTHENTICATION ENDPOINTS =================

@app.post("/api/auth/register", response_model=TokenResponse)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new user and return JWT token."""
    existing_user = db.query(UserModel).filter(UserModel.email == request.email.lower().strip()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    hashed = hash_password(request.password)
    new_user = UserModel(
        email=request.email.lower().strip(),
        full_name=request.full_name.strip(),
        hashed_password=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token({"sub": new_user.id, "email": new_user.email})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**new_user.to_dict())
    )

@app.post("/api/auth/login", response_model=TokenResponse)
def login_user(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate user with email/password and return JWT token."""
    user = db.query(UserModel).filter(UserModel.email == request.email.lower().strip()).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token = create_access_token({"sub": user.id, "email": user.email})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**user.to_dict())
    )

@app.get("/api/auth/me", response_model=UserResponse)
def get_current_user_profile(user: UserModel = Depends(get_current_user)):
    """Retrieve currently authenticated user's profile."""
    return UserResponse(**user.to_dict())

# ================= TRIP PLANNING ENDPOINTS =================

@app.post("/api/plan-trip", response_model=TripResponse)
def plan_trip(
    request: TripRequest, 
    db: Session = Depends(get_db),
    current_user: Optional[UserModel] = Depends(get_optional_current_user)
):
    """
    Generate an end-to-end trip itinerary using the LangGraph Multi-Agent Orchestrator.
    Saves the generated plan to SQLite database, linked to authenticated user if present.
    """
    try:
        logger.info(f"Received trip planning request: {request.origin} -> {request.destination} ({request.duration_days} days)")
        
        # Execute LangGraph Multi-Agent Workflow
        result_state = run_travel_planner(request.model_dump())
        final_itinerary = result_state.get("final_itinerary")
        
        if not final_itinerary:
            raise HTTPException(status_code=500, detail="Failed to synthesize itinerary from agents.")

        trip_id = str(uuid.uuid4())

        # Persist to Database
        trip_record = TripPlanModel(
            id=trip_id,
            user_id=current_user.id if current_user else None,
            origin=request.origin,
            destination=request.destination,
            duration_days=request.duration_days,
            budget=request.budget,
            currency=request.currency,
            travel_style=request.travel_style,
            interests=request.interests,
            itinerary_json=final_itinerary,
            raw_response=str(result_state.get("logs", []))
        )
        db.add(trip_record)
        db.commit()
        db.refresh(trip_record)

        return TripResponse(
            success=True,
            trip_id=trip_id,
            request=request,
            itinerary=TripItinerary(**final_itinerary),
            raw_logs={"logs": result_state.get("logs", [])}
        )
    except Exception as e:
        logger.error(f"Error executing trip plan: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trips")
def list_trips(
    limit: int = 20, 
    mine_only: bool = False,
    db: Session = Depends(get_db),
    current_user: Optional[UserModel] = Depends(get_optional_current_user)
):
    """
    List travel plans. Filter by user if mine_only is requested and user is authenticated.
    """
    query = db.query(TripPlanModel)
    if mine_only and current_user:
        query = query.filter(TripPlanModel.user_id == current_user.id)
    records = query.order_by(TripPlanModel.created_at.desc()).limit(limit).all()
    return [r.to_dict() for r in records]

@app.get("/api/trips/{trip_id}")
def get_trip(trip_id: str, db: Session = Depends(get_db)):
    """
    Get full details of a specific saved trip.
    """
    record = db.query(TripPlanModel).filter(TripPlanModel.id == trip_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Trip plan not found")
    return record.to_dict()

@app.delete("/api/trips/{trip_id}")
def delete_trip(
    trip_id: str, 
    db: Session = Depends(get_db),
    current_user: Optional[UserModel] = Depends(get_optional_current_user)
):
    """
    Delete a saved trip plan.
    """
    record = db.query(TripPlanModel).filter(TripPlanModel.id == trip_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Trip plan not found")
    
    # If the trip is owned by a specific user and an authenticated user requested deletion, check ownership
    if record.user_id and current_user and record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this trip.")
        
    db.delete(record)
    db.commit()
    return {"success": True, "message": f"Trip {trip_id} deleted successfully"}

@app.post("/api/modify-trip")
def modify_trip(request: ModifyTripRequest, db: Session = Depends(get_db)):
    """
    Modify an existing trip itinerary with a natural language instruction.
    """
    record = db.query(TripPlanModel).filter(TripPlanModel.id == request.trip_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Trip plan not found")

    current_itinerary = record.itinerary_json
    system_prompt = (
        "You are an expert Travel Revision AI Agent. Your task is to update and adjust a travel itinerary "
        "according to the user's specific feedback or modifications while keeping unchanged parts intact. "
        "Return the updated TripItinerary JSON."
    )

    prompt = f"""
    Destination: {record.destination}
    Current Itinerary: {current_itinerary}
    User Modification Request: {request.modification_prompt}

    Return the complete updated itinerary JSON matching the original structure.
    """

    updated_result = invoke_llm_json(prompt, system_prompt)
    if updated_result and "daily_itinerary" in updated_result:
        new_itinerary = updated_result
    else:
        # Fallback minor adjustment note
        new_itinerary = current_itinerary
        new_itinerary["destination_overview"] += f" (Updated: {request.modification_prompt})"
    
    # Save back to database
    record.itinerary_json = new_itinerary
    db.commit()
    db.refresh(record)

    return {
        "success": True,
        "trip_id": record.id,
        "updated_itinerary": new_itinerary
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)
