"""
FastAPI application for the Smart Water Saver Agent.
Main entry point that exposes /health and /chat endpoints.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import sys

from models import AgentRequest, AgentResponse
from agent import process_chat
from config import settings
from database import get_db, create_or_update_user, log_conversation, db_manager
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import time
import dashboard_api

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info(f"Starting {settings.agent_name}")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"OpenAI API Key configured: {bool(settings.openai_api_key)}")
    logger.info(f"Google API Key configured: {bool(settings.google_api_key)}")
    logger.info(f"Weather API Key configured: {bool(settings.weather_api_key)}")
    logger.info(f"Database URL configured: {bool(settings.database_url)}")
    
    # Initialize database tables
    try:
        db_manager.create_tables()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.agent_name}")


# Create FastAPI app
app = FastAPI(
    title="Smart Water Saver Agent",
    description="A Worker agent for smart water conservation using LangGraph",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include dashboard API router
app.include_router(dashboard_api.router)


# Exception handler for uncaught exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to ensure all responses follow AgentResponse format."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    error_response = AgentResponse(
        agent_name=settings.agent_name,
        status="error",
        data=None,
        error_message=f"Internal server error: {str(exc)}"
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )


@app.get("/", response_model=AgentResponse)
async def root():
    """Root endpoint - redirects to health check."""
    return AgentResponse(
        agent_name=settings.agent_name,
        status="success",
        data={
            "message": "Smart Water Saver Agent is running",
            "endpoints": {
                "health": "/health",
                "chat": "/chat",
                "dashboard": "/dashboard",
                "api_docs": "/docs"
            }
        },
        error_message=None
    )


@app.get("/dashboard")
async def dashboard():
    """Serve the dashboard HTML page."""
    return FileResponse("static/dashboard.html")


@app.get("/health", response_model=AgentResponse)
async def health_check():
    """
    Health check endpoint for the Supervisor to monitor agent status.
    
    Returns:
        AgentResponse with status and operational message
    """
    logger.info("Health check requested")
    
    return AgentResponse(
        agent_name=settings.agent_name,
        status="success",
        data={
            "message": "Agent is operational",
            "version": "1.0.0",
            "capabilities": [
                "watering_advice",
                "usage_query",
                "general_tip"
            ]
        },
        error_message=None
    )


@app.post("/chat", response_model=AgentResponse)
async def chat(request: AgentRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint for processing user requests via LangGraph.
    
    Args:
        request: AgentRequest containing messages and optional user_id
        db: Database session
        
    Returns:
        AgentResponse with the agent's reply or error message
    """
    user_id = request.user_id or "anonymous"
    logger.info(f"Chat request received from user: {user_id}")
    logger.debug(f"Messages: {request.messages}")
    
    start_time = time.time()
    
    try:
        # Create or update user in database
        if user_id != "anonymous":
            create_or_update_user(db, user_id=user_id)
        

        # Validate request
        if not request.messages:
            raise HTTPException(
                status_code=400,
                detail="Messages list cannot be empty"
            )
        
        # Convert Pydantic messages to dict format
        messages_dict = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        # Process through LangGraph agent
        response_content, agent_state = await process_chat(
            messages=messages_dict,
            user_id=request.user_id
        )
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)  # milliseconds
        
        # Log conversation to database
        try:
            user_message = messages_dict[-1]["content"] if messages_dict else ""
            log_conversation(
                db,
                user_id=user_id,
                intent=agent_state.get("intent", "unknown"),
                user_message=user_message,
                bot_response=response_content,
                weather_data=agent_state.get("weather_data"),
                usage_data=agent_state.get("usage_data"),
                processing_time_ms=processing_time
            )
        except Exception as log_error:
            logger.warning(f"Failed to log conversation: {log_error}")
        
        logger.info(f"Successfully generated response for user: {user_id} (took {processing_time}ms)")
        
        return AgentResponse(
            agent_name=settings.agent_name,
            status="success",
            data={
                "content": response_content
            },
            error_message=None
        )
        
    except HTTPException as he:
        # Re-raise HTTP exceptions
        logger.warning(f"HTTP exception: {he.detail}")
        raise he
        
    except Exception as e:
        # Log and return error response
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        
        return AgentResponse(
            agent_name=settings.agent_name,
            status="error",
            data=None,
            error_message=f"Failed to process request: {str(e)}"
        )


# Development server entry point
if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT from environment (for Render/Railway) or default
    port = int(os.getenv("PORT", settings.api_port))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Required for cloud deployments
        port=port,
        reload=False,  # Disable auto-reload in production
        log_level="info"
    )

