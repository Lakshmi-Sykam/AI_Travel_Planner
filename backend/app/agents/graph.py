from typing import Dict, Any
from langgraph.graph import StateGraph, END
from backend.app.agents.state import TripAgentState
from backend.app.agents.travel_agent import travel_agent_node
from backend.app.agents.hotel_agent import hotel_agent_node
from backend.app.agents.activity_agent import activity_agent_node
from backend.app.agents.synthesis_agent import synthesis_agent_node
from backend.app.tools.weather_tool import get_weather_info
from backend.app.tools.budget_tool import analyze_and_distribute_budget

def prep_tools_node(state: TripAgentState) -> Dict[str, Any]:
    """
    Initial tool retrieval node: fetches weather insights & calculates initial budget splits.
    """
    destination = state.get("destination", "Goa")
    duration_days = state.get("duration_days", 4)
    budget = state.get("budget", 20000)
    currency = state.get("currency", "INR")
    travel_style = state.get("travel_style", "Budget")

    weather_data = get_weather_info(destination)
    budget_data = analyze_and_distribute_budget(budget, duration_days, travel_style, currency)

    logs = state.get("logs", [])
    logs.append({
        "agent": "Tool Orchestrator",
        "action": f"Retrieved climate data for {destination} & computed budget allocations",
        "status": "Ready for multi-agent execution"
    })

    return {
        "weather_info": weather_data,
        "budget_analysis": budget_data,
        "logs": logs
    }

def build_travel_planner_graph():
    """
    Assembles the LangGraph StateGraph connecting all specialized agents.
    """
    workflow = StateGraph(TripAgentState)

    # Add Nodes
    workflow.add_node("prep_tools", prep_tools_node)
    workflow.add_node("travel_agent", travel_agent_node)
    workflow.add_node("hotel_agent", hotel_agent_node)
    workflow.add_node("activity_agent", activity_agent_node)
    workflow.add_node("synthesis_agent", synthesis_agent_node)

    # Set Entry Point
    workflow.set_entry_point("prep_tools")

    # Wire Edges (Sequential multi-agent execution with state accumulation)
    workflow.add_edge("prep_tools", "travel_agent")
    workflow.add_edge("travel_agent", "hotel_agent")
    workflow.add_edge("hotel_agent", "activity_agent")
    workflow.add_edge("activity_agent", "synthesis_agent")
    workflow.add_edge("synthesis_agent", END)

    return workflow.compile()

# Singleton compiled graph
travel_planner_app = build_travel_planner_graph()

def run_travel_planner(trip_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the multi-agent graph with the provided trip parameters.
    """
    initial_state: TripAgentState = {
        "origin": trip_request.get("origin", "Mumbai"),
        "destination": trip_request.get("destination", "Goa"),
        "duration_days": trip_request.get("duration_days", 4),
        "budget": trip_request.get("budget", 20000.0),
        "currency": trip_request.get("currency", "INR"),
        "travel_style": trip_request.get("travel_style", "Budget/Backpacker"),
        "interests": trip_request.get("interests", ["Beaches", "Food", "Sightseeing"]),
        "group_size": trip_request.get("group_size", 1),
        "special_requirements": trip_request.get("special_requirements"),
        "logs": [],
        "errors": []
    }
    
    final_output = travel_planner_app.invoke(initial_state)
    return final_output
