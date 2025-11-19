"""
LangGraph-based agent implementation for Smart Water Saver.
Implements the conversational state machine with intent routing.
"""
from typing import TypedDict, Annotated, Sequence, Optional, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
import operator
import json
from tools import weather_tool, usage_tool, tip_generator
from config import settings


# Define the Agent State
class AgentState(TypedDict):
    """State object passed between nodes in the LangGraph."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_id: Optional[str]
    intent: Optional[str]
    weather_data: Optional[dict]
    usage_data: Optional[dict]
    final_response: Optional[str]


# Intent classification prompts
def get_llm():
    """
    Get the configured LLM based on settings.
    Supports OpenAI (paid) and Google Gemini (free).
    """
    if settings.llm_provider == "openai" and settings.openai_api_key:
        return ChatOpenAI(
            model=settings.openai_model,
            temperature=0,
            api_key=settings.openai_api_key
        )
    elif settings.llm_provider == "gemini" and settings.google_api_key:
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            temperature=0,
            google_api_key=settings.google_api_key
        )
    else:
        return None


ROUTER_SYSTEM_PROMPT = """You are an intent classifier for a Smart Water Saver assistant.
Analyze the user's message and classify it into ONE of these intents:

1. "watering_advice" - User asks about watering schedules, when to water, or watering recommendations
   Examples: "Should I water today?", "When should I water my garden?", "Is it a good time to water?"

2. "usage_query" - User asks about their water usage, consumption, or usage history
   Examples: "How much water did I use?", "Show my water usage", "What's my consumption?"

3. "general_tip" - User asks for water conservation tips or general advice
   Examples: "Give me a water saving tip", "How can I save water?", "Any conservation advice?"

4. "unknown" - User message doesn't clearly fit the above categories or is unclear

Respond with ONLY the intent name, nothing else."""


async def router_node(state: AgentState) -> AgentState:
    """
    Router node: Classifies user intent from the latest message.
    This is the conditional entry point that determines the flow.
    """
    messages = state["messages"]
    last_user_message = None
    
    # Find the last user message
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg.content
            break
    
    if not last_user_message:
        state["intent"] = "unknown"
        return state
    
    # Use LLM for intent classification if available
    llm = get_llm()
    if llm:
        try:
            classification_messages = [
                SystemMessage(content=ROUTER_SYSTEM_PROMPT),
                HumanMessage(content=last_user_message)
            ]
            
            response = await llm.ainvoke(classification_messages)
            intent = response.content.strip().lower()
            
            # Validate intent
            valid_intents = ["watering_advice", "usage_query", "general_tip", "unknown"]
            if intent not in valid_intents:
                intent = "unknown"
            
            state["intent"] = intent
            
        except Exception as e:
            print(f"Router error: {e}")
            state["intent"] = "unknown"
    else:
        # Fallback: Simple keyword-based classification
        message_lower = last_user_message.lower()
        
        if any(word in message_lower for word in ["water", "watering", "irrigate", "sprinkle", "should i water"]):
            state["intent"] = "watering_advice"
        elif any(word in message_lower for word in ["usage", "used", "consumption", "how much", "usage history"]):
            state["intent"] = "usage_query"
        elif any(word in message_lower for word in ["tip", "advice", "save", "conservation", "conserve", "reduce"]):
            state["intent"] = "general_tip"
        else:
            state["intent"] = "unknown"
    
    return state


async def fetch_weather_node(state: AgentState) -> AgentState:
    """Fetch weather data using the weather tool."""
    try:
        weather_data = await weather_tool.get_weather()
        state["weather_data"] = weather_data
    except Exception as e:
        print(f"Weather fetch error: {e}")
        state["weather_data"] = {"error": str(e)}
    
    return state


async def fetch_usage_node(state: AgentState) -> AgentState:
    """Fetch water usage data from Long-Term Memory (database)."""
    user_id = state.get("user_id", "anonymous")
    
    try:
        usage_data = await usage_tool.get_water_usage(user_id)
        state["usage_data"] = usage_data
    except Exception as e:
        print(f"Usage fetch error: {e}")
        state["usage_data"] = {"error": str(e)}
    
    return state


async def generate_response_node(state: AgentState) -> AgentState:
    """
    Generate the final response using LLM.
    This is the main 'brain' that synthesizes all data.
    """
    intent = state.get("intent", "unknown")
    weather_data = state.get("weather_data")
    usage_data = state.get("usage_data")
    messages = state["messages"]
    
    # Build context for the LLM
    system_context = """You are a Smart Water Saver assistant helping users conserve water.
You provide friendly, actionable advice based on weather forecasts and usage data.
Keep responses concise and helpful."""
    
    # Add context based on available data
    context_parts = []
    
    if weather_data and "error" not in weather_data:
        context_parts.append(f"Weather Data: {json.dumps(weather_data, indent=2)}")
    
    if usage_data and "error" not in usage_data:
        context_parts.append(f"User Water Usage: {json.dumps(usage_data, indent=2)}")
    
    if context_parts:
        system_context += "\n\nContext:\n" + "\n".join(context_parts)
    
    # Use LLM if available
    llm = get_llm()
    if llm:
        try:
            generation_messages = [SystemMessage(content=system_context)] + list(messages)
            response = await llm.ainvoke(generation_messages)
            state["final_response"] = response.content
            
        except Exception as e:
            print(f"LLM generation error: {e}")
            state["final_response"] = _generate_fallback_response(intent, weather_data, usage_data)
    else:
        # Fallback: Template-based responses
        state["final_response"] = _generate_fallback_response(intent, weather_data, usage_data)
    
    return state


def _generate_fallback_response(intent: str, weather_data: Optional[dict], usage_data: Optional[dict]) -> str:
    """Generate template-based response when LLM is unavailable."""
    
    if intent == "watering_advice" and weather_data:
        recommendation = weather_data.get("recommendation", {})
        should_water = recommendation.get("should_water", True)
        reason = recommendation.get("reason", "")
        
        if should_water:
            return f"Yes, you should water your garden today. {reason}"
        else:
            return f"No, I would not recommend watering today. {reason}"
    
    elif intent == "usage_query" and usage_data:
        total = usage_data.get("total_usage_liters", 0)
        avg = usage_data.get("average_daily_usage", 0)
        days = usage_data.get("period_days", 0)
        
        return (f"Over the last {days} days, you've used {total:.0f} liters of water "
                f"(average: {avg:.2f}L per day). "
                f"Your usage trend is {usage_data.get('analytics', {}).get('trend', 'stable')}.")
    
    elif intent == "general_tip":
        return tip_generator.get_contextual_tip(weather_data, usage_data)
    
    else:
        return "I'm here to help you save water! Ask me about watering schedules, your usage, or water-saving tips."


async def fallback_node(state: AgentState) -> AgentState:
    """Handle unknown or unclear intents."""
    state["final_response"] = (
        "I'm not sure I understand. I can help you with:\n"
        "• Watering recommendations based on weather\n"
        "• Your water usage history and analytics\n"
        "• Water conservation tips\n\n"
        "What would you like to know?"
    )
    return state


def route_after_classification(state: AgentState) -> Literal["fetch_weather", "fetch_usage", "generate_tip", "fallback"]:
    """
    Conditional edge function that routes based on classified intent.
    """
    intent = state.get("intent", "unknown")
    
    if intent == "watering_advice":
        return "fetch_weather"
    elif intent == "usage_query":
        return "fetch_usage"
    elif intent == "general_tip":
        return "generate_tip"
    else:
        return "fallback"


def create_agent_graph():
    """
    Create and compile the LangGraph state machine.
    This is the main assembly point for the agent.
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("fetch_weather", fetch_weather_node)
    workflow.add_node("fetch_usage", fetch_usage_node)
    workflow.add_node("generate_tip", generate_response_node)  # Reuse for tips
    workflow.add_node("generate_response", generate_response_node)
    workflow.add_node("fallback", fallback_node)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        route_after_classification,
        {
            "fetch_weather": "fetch_weather",
            "fetch_usage": "fetch_usage",
            "generate_tip": "generate_tip",
            "fallback": "fallback"
        }
    )
    
    # Add edges from tool nodes to response generation
    workflow.add_edge("fetch_weather", "generate_response")
    workflow.add_edge("fetch_usage", "generate_response")
    
    # Add edges to END
    workflow.add_edge("generate_response", END)
    workflow.add_edge("generate_tip", END)
    workflow.add_edge("fallback", END)
    
    # Compile the graph
    return workflow.compile()


# Global compiled graph instance
agent_graph = create_agent_graph()


async def process_chat(messages: list, user_id: Optional[str] = None) -> tuple[str, dict]:
    """
    Process a chat request through the agent graph.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        user_id: Optional user identifier for personalization
        
    Returns:
        Tuple of (final response string, agent state dict)
    """
    # Convert messages to LangChain format
    lc_messages = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
        elif role == "system":
            lc_messages.append(SystemMessage(content=content))
    
    # Initialize state
    initial_state = {
        "messages": lc_messages,
        "user_id": user_id,
        "intent": None,
        "weather_data": None,
        "usage_data": None,
        "final_response": None
    }
    
    # Run the graph
    try:
        final_state = await agent_graph.ainvoke(initial_state)
        response = final_state.get("final_response", "I apologize, but I encountered an error processing your request.")
        return response, final_state
    except Exception as e:
        print(f"Agent graph error: {e}")
        error_state = {"intent": "error", "error": str(e)}
        return f"I encountered an error: {str(e)}", error_state

