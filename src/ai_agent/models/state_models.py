from enum import Enum
from typing import Annotated, Any, Dict, List, Literal, Optional, TypedDict
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class Intent(str, Enum):
    CHIT_CHAT = "chit_chat"
    PRODUCT_INQUIRY = "product_inquiry"
    BOOK_APPOINTMENT = "book_appointment"
    
class AgentInput(TypedDict):
    """Simple input state for each subagent."""
    query: str


class AgentOutput(TypedDict):
    """Output from each subagent."""
    source: str
    result: str


class Classification(TypedDict):
    """A single routing decision: which agent to call with what query."""
    source: Intent
    query: str

class WhatsAppState(TypedDict):
    # Session Management
    sender_id: str          # User's WhatsApp ID (phone number)
    sender_name: str        # User's profile name
    message_id: str         # Unique WhatsApp message ID (for deduplication)
    message_type: Literal["text", "audio", "image", "document", "other"]
    text_content: str | None = None    # Plain text message string
    media_id: str | None = None        # ID used to fetch audio/images from WhatsApp API


class RouterState(TypedDict):
    query: str
    classifications: list[Classification]
    results: Annotated[list[AgentOutput], operator.add]  # Reducer collects parallel results
    final_answer: str



    
