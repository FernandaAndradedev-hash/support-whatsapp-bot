"""
Histórico de conversa por sessão.
"""
import time
from dataclasses import dataclass, field

import config

logger = __import__("logging").getLogger(__name__)


@dataclass
class Session:
    phone: str
    messages: list[dict] = field(default_factory=list)
    last_activity: float = field(default_factory=time.time)
    bot_attempts: int = 0    # conta quantas vezes o bot não conseguiu ajudar
    escalated: bool = False  # True se já foi escalado nesta sessão


_sessions: dict[str, Session] = {}


def _is_expired(session: Session) -> bool:
    return (time.time() - session.last_activity) > config.SESSION_TTL


def get_session(phone: str) -> Session:
    """Retorna a sessão ou cria uma nova."""
    session = _sessions.get(phone)
    if session is None or _is_expired(session):
        _sessions[phone] = Session(phone=phone)
    else:
        _sessions[phone].last_activity = time.time()
    return _sessions[phone]


def get_history(phone: str) -> list[dict]:
    session = get_session(phone)
    return session.messages.copy()


def add_message(phone: str, role: str, content: str) -> None:
    session = get_session(phone)
    session.messages.append({"role": role, "content": content})
    session.last_activity = time.time()

    if len(session.messages) > config.MAX_HISTORY_MESSAGES:
        excess = len(session.messages) - config.MAX_HISTORY_MESSAGES
        session.messages = session.messages[excess:]


def increment_bot_attempts(phone: str) -> int:
    """Incrementa contador de tentativas sem resposta. Retorna total."""
    session = get_session(phone)
    session.bot_attempts += 1
    return session.bot_attempts


def mark_escalated(phone: str) -> None:
    """Marca sessão como escalada."""
    session = get_session(phone)
    session.escalated = True


def is_escalated(phone: str) -> bool:
    """Verifica se sessão já foi escalada."""
    session = get_session(phone)
    return session.escalated


def clear_session(phone: str) -> None:
    _sessions.pop(phone, None)