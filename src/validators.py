"""
Segurança específica para atendente de suporte via WhatsApp.
Reutiliza padrões do Projeto 2 com adições para e-commerce.
"""
import logging
import re
import time

import 

import config

logger = logging.getLogger(__name__)

_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions?",
    r"disregard\s+(all\s+)?instructions?",
    r"forget\s+(everything|all)",
    r"you\s+are\s+now\s+(a|an)",
    r"new\s+instructions?\s*:",
    r"system\s+prompt\s*:",
    r"jailbreak",
    r"do\s+anything\s+now",
    r"\[INST\]",
    r"\[SYSTEM\]",
]

_INJECTION_RE = re.compile("|".join(_INJECTION_PATTERNS), re.IGNORECASE)

# Rate limiting em memória
_rate_store: dict[str, list[float]] = {}


def check_rate_limit(phone: str) -> bool:
    """Rate limiting por sliding window."""
    now = time.time()
    window = config.RATE_LIMIT_WINDOW_SECONDS
    max_msgs = config.RATE_LIMIT_MAX_MESSAGES

    if phone not in _rate_store:
        _rate_store[phone] = []

    _rate_store[phone] = [ts for ts in _rate_store[phone] if now - ts < window]

    if len(_rate_store[phone]) >= max_msgs:
        logger.warning("Rate limit excedido: %s", phone[-4:])
        return False

    _rate_store[phone].append(now)
    return True


def sanitize_message(text: str) -> str:
    """
    Sanitiza mensagem recebida do WhatsApp.

    Raises:
        ValueError: Se mensagem for inválida ou suspeita.
    """
    if not isinstance(text, str):
        raise ValueError("Mensagem deve ser texto.")

    clean = bleach.clean(text, tags=[], strip=True)
    clean = re.sub(r"\s+", " ", clean).strip()

    if not clean:
        raise ValueError("Mensagem vazia.")

    if len(clean) > config.MAX_MESSAGE_LENGTH:
        raise ValueError(f"Mensagem muito longa ({len(clean)} chars).")

    if _INJECTION_RE.search(clean):
        logger.warning("Prompt injection detectado de %s", "***")
        raise ValueError("Mensagem com conteúdo inválido.")

    return clean


def extract_message_from_webhook(payload: dict) -> dict | None:
    """Extrai dados relevantes do payload da Evolution API."""
    try:
        if payload.get("event") != "messages.upsert":
            return None

        data = payload.get("data", {})
        key = data.get("key", {})
        message = data.get("message", {})

        if key.get("fromMe", False):
            return None

        remote_jid = key.get("remoteJid", "")
        phone = remote_jid.replace("@s.whatsapp.net", "").replace("@g.us", "")

        if not phone:
            return None

        text = (
            message.get("conversation")
            or message.get("extendedTextMessage", {}).get("text")
        )

        if not text:
            return None

        return {"phone": phone, "message": text}

    except Exception as exc:
        logger.error("Erro ao extrair mensagem: %s", exc)
        return None


def validate_response_safety(response: str) -> str:
    """Verifica se a resposta não vaza dados do sistema."""
    patterns = [
        r"system\s+prompt",
        r"ANTHROPIC_API_KEY",
        r"sk-ant-",
        r"minhas\s+instruções",
    ]
    for pattern in patterns:
        if re.search(pattern, response, re.IGNORECASE):
            logger.warning("Possível vazamento detectado na resposta.")
            return (
                "Desculpe, ocorreu um erro. "
                "Nossa equipe foi notificada. "
                "Tente novamente ou ligue: (11) 99000-1234"
            )
    return response