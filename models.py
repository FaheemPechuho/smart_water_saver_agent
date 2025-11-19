"""
Pydantic models for the Smart Water Saver Agent.
Defines the API contract between Supervisor and Worker agent.
"""
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Individual message in a conversation."""
    role: str = Field(..., description="Role of the message sender (user, assistant, system)")
    content: str = Field(..., description="Content of the message")


class AgentRequest(BaseModel):
    """
    Request model for the /chat endpoint.
    This is the format the Supervisor will send to our agent.
    """
    messages: List[Message] = Field(
        ..., 
        description="List of conversation messages",
        min_length=1
    )
    user_id: Optional[str] = Field(
        None, 
        description="Optional user ID for long-term memory access"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Should I water my garden today?"
                    }
                ],
                "user_id": "user_123"
            }
        }


class AgentResponse(BaseModel):
    """
    Response model for all agent endpoints.
    Standardized format for communication with the Supervisor.
    """
    agent_name: str = Field(
        default="SmartWaterSaverAgent",
        description="Name of this agent"
    )
    status: str = Field(
        ..., 
        description="Status of the request: 'success' or 'error'"
    )
    data: Optional[Dict[str, Any]] = Field(
        None,
        description="Response data when status is 'success'"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message when status is 'error'"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_name": "SmartWaterSaverAgent",
                "status": "success",
                "data": {
                    "content": "No, I would not recommend watering today. The forecast shows 5mm of rain expected around 4:00 PM."
                },
                "error_message": None
            }
        }

