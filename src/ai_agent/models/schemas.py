
from pydantic import BaseModel, Field
from state_models import Classification


class ClassificationResult(BaseModel):
    """Result of classifying a user query into agent-specific sub-questions."""
    classifications: list[Classification] = Field(
        description="List of agents to invoke with their targeted sub-questions"
    )
class FinalOutput(BaseModel):
    """The final result of the graph"""
    source: str
    result: str


