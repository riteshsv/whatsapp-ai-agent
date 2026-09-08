
from langchain.tools import InjectedState, ToolRuntime, tool
from langgraph.runtime import Runtime
from ..whatsapp.models import WhatsAppContext
from ..services.state_graph import app


@tool
def perform_user_task(query: str,
                      runtime: ToolRuntime[WhatsAppContext]) -> str:
    """
    Classify users intent and route to the relevant agent
    """
    inputs = {
                "query": query
            }
    # result = exe_graph_verbose(app,inputs)
    result = app.invoke(inputs,
                        config={
                            "max_concurrency":1
                        },
                        print_mode="debug")
    results = result.get("results", [])

    if not results:
        return "I was unable to process your request."

    responses = []

    for item in results:
        response = item.get("result")

        if response:
            responses.append(response)

    if not responses:
        return "I was unable to process your request."

    return "\n\n".join(responses)