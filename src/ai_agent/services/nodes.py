from langchain.messages import HumanMessage, SystemMessage
from ..models.schemas import ClassificationResult
from ..models.state_models import RouterState
from .llm import model

CLASSIFIER_SYSTEM_PROMPT = """
You are an intent classification and query decomposition agent.

Your job is to analyze the user's request and divide it into
independent tasks that can be handled by specialist agents.

Available intents:

1. "chit_chat"
   - Casual conversation
   - Greetings
   - Small talk

2. "product_inquiry"
   - Questions about products
   - Product availability
   - Product specifications
   - Product recommendations
   - Product pricing
   - Purchasing-related product questions

3. "book_appointment"
   - Book an appointment
   - Schedule an appointment
   - Reschedule an appointment
   - Arrange a demo
   - Find an appointment time
   - Meet with sales, support, consultants, etc.

IMPORTANT - PRESERVE SHARED CONTEXT:

If the user asks for multiple things, create ONE classification
for EACH independent task.

The "query" field MUST contain ONLY the part of the user's request
that belongs to that specific intent.

DO NOT copy the complete original user request into every query.

When decomposing a multi-intent request, preserve entities and
context from the original request when they are relevant to more
than one intent.

Example:

User:
"Is the X100 available and could you book a demo please?"

Correct output:

[
    {
        "source": "product_inquiry",
        "query": "Is the X100 available?"
    },
    {
        "source": "book_appointment",
        "query": "Could you book a demo for the X100 please?"
    }
]

Incorrect output:

[
    {
        "source": "product_inquiry",
        "query": "Is the X100 available and could you book a demo please?"
    },
    {
        "source": "book_appointment",
        "query": "Is the X100 available and could you book a demo please?"
    }
]

Another example:

User:
"Hi, can you tell me whether the X100 is available and arrange
a demo for next Tuesday?"

Correct decomposition:

[
    {
        "source": "chit_chat",
        "query": "Hi"
    },
    {
        "source": "product_inquiry",
        "query": "Is the X100 available?"
    },
    {
        "source": "book_appointment",
        "query": "Arrange a demo for X100 on next Tuesday."
    }
]

Another example:

User:
"I want to buy the X100."

Correct output:

[
    {
        "source": "product_inquiry",
        "query": "I want to buy the X100."
    }
]

Rules:

- Classify by meaning, not communication channel.
- Never create an intent for "voice", "audio", "image", etc.
- Do not invent information.
- Preserve important entities, product names, dates, times,
  quantities and constraints in each sub-query.
- Each sub-query must be understandable by the specialist agent
  without needing to see the original query.
- Do not include information belonging to another intent.
- If only one intent exists, return one classification.
- If multiple independent intents exist, return multiple classifications.
"""

def intent_classification(state: RouterState) -> RouterState:
    """
    Classify the user's query into one or more supported intents.
    """

    query = state.get("query", "").strip()

    if not query:
        return {
            **state,
            "classifications": [],
        }

    structured_llm = model.with_structured_output(
        ClassificationResult
    )

    system_prompt = CLASSIFIER_SYSTEM_PROMPT

    llm_response = structured_llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ]
    )
    
    return {
        **state,
        "query": query,
        "classifications": llm_response.classifications,
    }