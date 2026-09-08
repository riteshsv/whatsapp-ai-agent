from typing import Literal
from pydantic import BaseModel, Field
class WhatsAppContext(BaseModel):
    sender_id: str          # User's WhatsApp ID (phone number)
    sender_name: str        # User's profile name
    message_id: str         # Unique WhatsApp message ID (for deduplication)
    message_type: Literal["text", "audio", "image", "document", "other"]

class MediaReference(BaseModel):
    media_id: str
    mime_type: str
    url: str | None = None

class NormalizedUserInput(BaseModel):
    text: str
    source_type: Literal[
        "text",
        "audio",
        "image",
        "document",
        "video",
        "other",
    ]
    media: MediaReference | None = None