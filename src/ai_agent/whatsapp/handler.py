# Simulated API Endpoint Handler
import json

from src.ai_agent.models.webhook import WhatsAppWebhookPayload

from .models import MediaReference, WhatsAppContext
from .parser import normalize_whatsapp_input, parse_whatsapp_webhook
from ..services.agents import customer_support_agent


def handle_whatsapp_webhook(
    payload: WhatsAppWebhookPayload
):

    # payload = json.loads(
    #     raw_json
    # )

    # --------------------------------
    # 1. Parse WhatsApp payload
    # --------------------------------

    parsed_message = (
        parse_whatsapp_webhook(
            payload
        )
    )

    if not parsed_message:

        return (
            "Event ignored",
            200,
        )

    # --------------------------------
    # 2. Normalize input
    # --------------------------------

    normalized_input = (
        normalize_whatsapp_input(
            parsed_message
        )
    )

    if not normalized_input.text:

        return (
            "No textual input available",
            200,
        )

    # --------------------------------
    # 3. Build WhatsApp runtime context
    # --------------------------------

    whatsapp_context = WhatsAppContext(

        sender_id=parsed_message[
            "sender_id"
        ],

        sender_name=parsed_message[
            "sender_name"
        ],

        message_id=parsed_message[
            "message_id"
        ],

        message_type=parsed_message[
            "message_type"
        ],

        media=(
            MediaReference(
                media_id=parsed_message[
                    "media_id"
                ],
                mime_type=parsed_message[
                    "mime_type"
                ] or "application/octet-stream",
            )
            if parsed_message.get(
                "media_id"
            )
            else None
        ),
    )

    # --------------------------------
    # 4. Conversation identity
    # --------------------------------

    config = {
        "configurable": {
            "thread_id": parsed_message[
                "sender_id"
            ]
        }
    }

    # --------------------------------
    # 5. Invoke conversational agent
    # --------------------------------

    result = customer_support_agent.invoke(

        {
            "messages": [
                {
                    "role": "user",
                    "content": normalized_input.text,
                }
            ]
        },

        context=whatsapp_context,

        config=config,
        print_mode="debug"
    )

    # print("\n--- ALL MESSAGES ---")

    # for i, message in enumerate(result["messages"]):
    #     print(f"\nMESSAGE {i}")
    #     print("TYPE:", type(message).__name__)
    #     print("CONTENT:", message.content)

    # final_message = result["messages"][-1]

    # print(
    #     f"\nAssistant: {final_message.content}"
    # )


    # --------------------------------
    # 6. Extract final response
    # --------------------------------

    final_message = result[
        "messages"
    ][-1]

    # print(
    #     f"Assistant: {final_message.content}"
    # )

    return (
        final_message.content,
        200,
    )
