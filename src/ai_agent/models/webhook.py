from typing import List, Optional
from pydantic import BaseModel, Field


class TextMessage(BaseModel):
    body: str


class Message(BaseModel):
    from_number: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[TextMessage] = None


class Profile(BaseModel):
    name: Optional[str] = None


class Contact(BaseModel):
    profile: Optional[Profile] = None
    wa_id: str


class Value(BaseModel):
    messaging_product: str
    metadata: dict
    contacts: Optional[List[Contact]] = None
    messages: Optional[List[Message]] = None


class Change(BaseModel):
    value: Value
    field: str


class Entry(BaseModel):
    id: str
    changes: List[Change]


class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[Entry]