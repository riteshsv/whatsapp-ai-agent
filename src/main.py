import logging
from fastapi import FastAPI, Request, Response, HTTPException, Query, status

from src.ai_agent.whatsapp.handler import handle_whatsapp_webhook
from .config import settings
from .ai_agent.models.webhook import WhatsAppWebhookPayload
from .ai_agent.whatsapp.message import send_whatsapp_message

logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("WhatsAppMiddleware")

app = FastAPI(
    title="WhatsApp AI Agent API",
    version="0.1.0",
    description="Middleware for Meta WhatsApp Cloud API connected to OpenAI"
)


@app.get("/")
async def root():
    return {"status": "online", "environment": settings.app_env}


@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    """Meta Webhook Challenge Verification."""
    if hub_mode == "subscribe" and hub_verify_token == settings.meta_verify_token:
        logger.info("Webhook verification challenge successful.")
        return Response(content=hub_challenge, media_type="text/plain")
    
    logger.warning("Webhook verification challenge failed.")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Verification token mismatch"
    )


@app.post("/webhook")
async def process_webhook(request: Request):
    """Processes incoming Meta WhatsApp events asynchronously."""
    body = await request.json()
    
    try:
        payload = WhatsAppWebhookPayload(**body)
        
        ai_response,status = handle_whatsapp_webhook(payload=payload)
        await send_whatsapp_message(payload.entry[0].changes[0].value.messages[0].get("from"), ai_response)
        
        return {"status": "success"}

    except Exception as e:
        logger.error(f"Failed to process webhook event: {e}")
        # Return 200 to Meta even on internal errors to prevent repetitive retries from Meta servers
        return {"status": "error_handled", "detail": str(e)}