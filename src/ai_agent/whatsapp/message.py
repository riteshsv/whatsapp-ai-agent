import logging
import httpx
from ...config import settings

logger = logging.getLogger(__name__)


async def send_whatsapp_message(to_phone_number: str, text: str) -> bool:
    """Posts an outbound text message to Meta WhatsApp Cloud API."""
    url = f"https://graph.facebook.com/v19.0/{settings.whatsapp_phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.meta_access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone_number,
        "type": "text",
        "text": {"body": text}
    }

    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                logger.info(f"Successfully sent message to {to_phone_number}")
                return True
            else:
                logger.error(
                    f"Failed to send message. Status: {response.status_code}, Payload: {response.text}"
                )
                return False
        except httpx.HTTPError as err:
            logger.error(f"HTTP error occurred while calling Meta Graph API: {err}")
            return False