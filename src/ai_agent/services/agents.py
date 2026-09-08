#agents
from langchain.agents import create_agent
from .llm import model
from ..tools import perform_user_task
from ..whatsapp.models import WhatsAppContext


chit_chat_agent = create_agent(
    model,
    system_prompt=("You are a chit-chat agent. Your task is to engage in casual conversation with the user." 
                   "Respond in a friendly and conversational manner."
    )
)

product_inquiry_agent = create_agent(
    model,
    system_prompt=("You are a product inquiry agent. Your task is to provide information about products and answer user questions related to products." 
                   "Respond in a helpful and informative manner.")
)
book_appointment_agent = create_agent(
    model,
    system_prompt=("You are a book appointment agent. Your task is to help users book appointments." 
                   "Respond in a helpful and informative manner.")
)

from langgraph.checkpoint.memory import InMemorySaver

customer_support_agent_prompt = """
You are a helpful customer support assistant.

You receive normalized user requests from WhatsApp.

Use the perform_user_task tool whenever the user
is asking for a task that should be handled by
a specialist agent.

The tool will classify the request, route it to
the appropriate specialist and return the result.

Respond naturally to the user based on the result.

Do not expose internal routing, agent names,
tool execution details or implementation details.
"""
customer_support_agent = create_agent(
    model=model,
    tools=[perform_user_task],
    system_prompt=customer_support_agent_prompt,
    checkpointer=InMemorySaver(),
    context_schema=WhatsAppContext
)