"""
Webhook FastAPI para o ShopBot.
Recebe mensagens da Evolution API e coordena o processamento.
"""
import logging
import sys

import httpx
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

import config
from agent import process_message
from validators import (
    check_rate_limit,
    extract_message_from_webhook,
    sanitize_message,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ShopBot — Suporte VendaMais",
    description="Atendente automático com escalonamento inteligente.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


async def send_whatsapp_message(phone: str, message: str) -> bool:
    """Envia mensagem via Evolution API."""
    url = f"{config.EVOLUTION_API_URL}/message/sendText/{config.EVOLUTION_INSTANCE}"
    headers = {
        "apikey": config.EVOLUTION_API_KEY,
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                json={"number": phone, "text": message},
                headers=headers,
            )
            response.raise_for_status()
            return True
    except Exception as exc:
        logger.error("Erro ao enviar mensagem: %s", exc)
        return False


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ShopBot — VendaMais"}


@app.post("/webhook", status_code=status.HTTP_200_OK)
async def webhook(request: Request):
    """Recebe eventos da Evolution API."""
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Payload inválido.")

    message_data = extract_message_from_webhook(payload)

    if message_data is None:
        return {"status": "ignored"}

    phone = message_data["phone"]
    raw_message = message_data["message"]

    logger.info("Mensagem de %s (len: %d)", phone[-4:], len(raw_message))

    # Rate limiting
    if not check_rate_limit(phone):
        await send_whatsapp_message(
            phone,
            "Você enviou muitas mensagens em pouco tempo. "
            "Aguarde um momento antes de continuar. 🙏",
        )
        return {"status": "rate_limited"}

    # Sanitização
    try:
        clean_message = sanitize_message(raw_message)
    except ValueError as exc:
        logger.info("Mensagem inválida de %s: %s", phone[-4:], exc)
        await send_whatsapp_message(
            phone,
            "Não entendi sua mensagem. "
            "Por favor, envie apenas texto simples.",
        )
        return {"status": "invalid"}

    # Processamento
    try:
        response = process_message(phone, clean_message)
        await send_whatsapp_message(phone, response)
        return {"status": "ok"}
    except Exception as exc:
        logger.error("Erro ao processar: %s", exc, exc_info=True)
        await send_whatsapp_message(
            phone,
            "Ops! Tive um problema técnico. "
            "Tente novamente ou ligue: (11) 99000-1234 📞",
        )
        return {"status": "error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)