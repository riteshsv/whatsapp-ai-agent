from typing import Any, Dict, Optional

from .models import MediaReference, NormalizedUserInput


def parse_whatsapp_webhook(
    payload: Dict[str, Any]
) -> Optional[Dict[str, Any]]:

    try:

        entry = payload.get("entry", [{}])[0]

        change = entry.get(
            "changes",
            [{}]
        )[0]

        value = change.get(
            "value",
            {}
        )

        # Ignore status updates
        if "messages" not in value:
            return None

        message = value["messages"][0]

        contact = value.get(
            "contacts",
            [{}]
        )[0]

        message_type = message.get(
            "type",
            "other"
        )

        parsed = {
            "sender_id": message.get("from"),

            "sender_name": contact.get(
                "profile",
                {}
            ).get(
                "name",
                "Unknown"
            ),

            "message_id": message.get("id"),

            "message_type": message_type,

            "text_content": None,

            "media_id": None,

            "mime_type": None,
        }

        # -------------------------
        # TEXT
        # -------------------------

        if message_type == "text":

            parsed["text_content"] = (
                message
                .get("text", {})
                .get("body", "")
            )

        # -------------------------
        # AUDIO
        # -------------------------

        elif message_type == "audio":

            audio = message.get(
                "audio",
                {}
            )

            parsed["media_id"] = audio.get("id")

            parsed["mime_type"] = audio.get(
                "mime_type",
                "audio/ogg"
            )

        # -------------------------
        # IMAGE
        # -------------------------

        elif message_type == "image":

            image = message.get(
                "image",
                {}
            )

            parsed["media_id"] = image.get("id")

            parsed["mime_type"] = image.get(
                "mime_type",
                "image/jpeg"
            )

            parsed["text_content"] = image.get(
                "caption"
            )

        # -------------------------
        # DOCUMENT
        # -------------------------

        elif message_type == "document":

            document = message.get(
                "document",
                {}
            )

            parsed["media_id"] = document.get(
                "id"
            )

            parsed["mime_type"] = document.get(
                "mime_type"
            )

            parsed["text_content"] = document.get(
                "caption"
            )

        # -------------------------
        # VIDEO
        # -------------------------

        elif message_type == "video":

            video = message.get(
                "video",
                {}
            )

            parsed["media_id"] = video.get(
                "id"
            )

            parsed["mime_type"] = video.get(
                "mime_type",
                "video/mp4"
            )

            parsed["text_content"] = video.get(
                "caption"
            )

        return parsed

    except (
        IndexError,
        KeyError,
        TypeError,
    ):

        return None

def transcribe_audio(media: MediaReference) -> str:
    """
    Retrieve audio using media.media_id and send it to
    your transcription service.

    Replace this mock implementation with the actual
    WhatsApp media download + transcription implementation.
    """

    print(
        f"Transcribing audio: "
        f"{media.media_id} ({media.mime_type})"
    )

    # MOCK
    return "I would like to book an appointment for next week."


def normalize_whatsapp_input(
    parsed_message: Dict[str, Any]
) -> NormalizedUserInput:

    message_type = parsed_message["message_type"]

    # -------------------------
    # TEXT
    # -------------------------

    if message_type == "text":

        return NormalizedUserInput(
            text=parsed_message.get("text_content"),
            source_type="text",
            media=None,
        )

    # -------------------------
    # AUDIO
    # -------------------------

    if message_type == "audio":

        media = MediaReference(
            media_id=parsed_message["media_id"],
            mime_type=parsed_message.get(
                "mime_type",
                "audio/ogg"
            ),
        )

        transcript = transcribe_audio(media)

        return NormalizedUserInput(
            text=transcript,
            source_type="audio",
            media=media,
        )

    # -------------------------
    # IMAGE
    # -------------------------

    if message_type == "image":

        media = MediaReference(
            media_id=parsed_message["media_id"],
            mime_type=parsed_message.get(
                "mime_type",
                "image/jpeg"
            ),
        )

        # For now we don't convert image to text.
        # A multimodal conversational model can receive it directly.

        return NormalizedUserInput(
            text=parsed_message.get("text_content"),
            source_type="image",
            media=media,
        )

    # -------------------------
    # DOCUMENT
    # -------------------------

    if message_type == "document":

        media = MediaReference(
            media_id=parsed_message["media_id"],
            mime_type=parsed_message.get(
                "mime_type",
                "application/octet-stream"
            ),
        )

        # Later:
        # 1. download document
        # 2. extract text
        # 3. optionally create document reference

        return NormalizedUserInput(
            text=parsed_message.get("text_content"),
            source_type="document",
            media=media,
        )

    # -------------------------
    # VIDEO
    # -------------------------

    if message_type == "video":

        media = MediaReference(
            media_id=parsed_message["media_id"],
            mime_type=parsed_message.get(
                "mime_type",
                "video/mp4"
            ),
        )

        # Later we can:
        # - extract audio
        # - transcribe
        # - process frames
        # - use multimodal model

        return NormalizedUserInput(
            text=parsed_message.get("text_content"),
            source_type="video",
            media=media,
        )

    # -------------------------
    # OTHER
    # -------------------------

    return NormalizedUserInput(
        text=parsed_message.get("text_content"),
        source_type="other",
        media=None,
    )