from .utils import extract_text
from ..models.state_models import AgentInput
from ..services.agents import book_appointment_agent, chit_chat_agent,product_inquiry_agent
from ..models.state_models import RouterState

def book_appointment_agent_handler(state: AgentInput) -> dict:
    """
    Simulated book appointment agent.
    In a real implementation, this would handle booking appointments.
    """
    result = book_appointment_agent.invoke({
        "messages" : [
            {
                "role": "user",
                "content": state["query"]
            }
        ]
        }
    )
    final_message = result["messages"][-1]

    return {
        "results": [{
            "source": "book_appointment",
            "result": extract_text(final_message)
        }]
    }
def chit_chat_agent_handler(state: AgentInput) -> dict:
    """
    Simulated chit-chat agent.
    In a real implementation, this would handle casual conversation.
    """
    result = chit_chat_agent.invoke({
            "messages" : [
                {
                    "role": "user",
                    "content": state["query"]
                }
            ]
            }
        )
    final_message = result["messages"][-1]

    return {
        "results": [{
            "source": "chat_chat",
            "result": extract_text(final_message)
        }]
    }
def product_inquiry_agent_handler(state: AgentInput) -> dict:
    """
    Simulated product inquiry agent.
    In a real implementation, this would handle product inquiries.
    """
    result = product_inquiry_agent.invoke({
            "messages" : [
                {
                    "role": "user",
                    "content": state["query"]
                }
            ]
            }
        )
    final_message = result["messages"][-1]

    return {
        "results": [{
            "source": "product_inquiry",
            "result": extract_text(final_message)
        }]
    }

from langgraph.types import Send
def route_to_agents(state: RouterState) -> list[Send]:
    """
    Route the query to the appropriate agents based on the classifications.
    This function simulates calling different agents and collecting their responses.
    """
    return [
        Send(
            c["source"],
            {"query": c["query"]},
        ) for c in state["classifications"]
    ]