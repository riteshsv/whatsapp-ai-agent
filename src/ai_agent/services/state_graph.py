
from langgraph.graph import END, START, StateGraph
from ..models.state_models import RouterState
from .nodes import intent_classification
from .edges import chit_chat_agent_handler,product_inquiry_agent_handler,book_appointment_agent_handler,route_to_agents

workflow = StateGraph(RouterState)
workflow.add_node("classifier", intent_classification)
workflow.add_node("chit_chat", chit_chat_agent_handler)
workflow.add_node("product_inquiry", product_inquiry_agent_handler)
workflow.add_node("book_appointment", book_appointment_agent_handler)
workflow.add_conditional_edges(
    "classifier",
    route_to_agents,
    ['chit_chat', 'product_inquiry', 'book_appointment']
)
workflow.add_edge(START, "classifier")
workflow.add_edge("chit_chat", END)
workflow.add_edge("product_inquiry", END)
workflow.add_edge("book_appointment", END)
app = workflow.compile()
app