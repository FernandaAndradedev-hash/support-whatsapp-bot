"""
Lógica de escalonamento inteligente.

O bot decide autonomamente quando escalar para humano baseado em:
- Palavras-chave de urgência na mensagem
- Número de tentativas sem resposta
- Valor de reembolso solicitado
- Horário de atendimento
- Pedido explícito do cliente
"""
import json
import logging
import re
from datetime import datetime
from pathlib import Path

import config

logger = logging.getLogger(__name__)

# Padrões que disparam escalonamento imediato ───────────────────────────────

_ESCALATION_TRIGGERS = [
    # Pedido explícito de humano
    r"\b(humano|atendente|pessoa|falar\s+com\s+alguém|gerente|responsável)\b",
    # Reclamações graves
    r"\b(fraude|golpe|enganado|roubado|processando|advogado|procon|reclame\s+aqui)\b",
    # Produto danificado na entrega
    r"\b(chegou\s+quebrado|chegou\s+danificado|produto\s+errado|não\s+funciona)\b",
    # Urgência extrema
    r"\b(urgentíssimo|emergência|socorro)\b",
]

_ESCALATION_RE = re.compile("|".join(_ESCALATION_TRIGGERS), re.IGNORECASE)

# Padrão para detectar valor de reembolso mencionado
_MONEY_RE = re.compile(r"R\$\s*(\d+(?:[.,]\d+)?)", re.IGNORECASE)


def check_escalation_triggers(message: str) -> tuple[bool, str]:
    """
    Verifica se a mensagem dispara escalonamento imediato.

    Returns:
        Tupla (deve_escalar, motivo).
    """
    # Pedido de humano ou situação grave
    match = _ESCALATION_RE.search(message)
    if match:
        return True, f"Trigger detectado: '{match.group()}'"

    # Valor de reembolso acima do threshold
    money_match = _MONEY_RE.search(message)
    if money_match:
        value_str = money_match.group(1).replace(".", "").replace(",", ".")
        try:
            value = float(value_str)
            if value >= config.ESCALATION_REFUND_THRESHOLD:
                return True, f"Reembolso de R$ {value:.2f} requer aprovação humana"
        except ValueError:
            pass

    return False, ""


def is_business_hours() -> bool:
    """Verifica se está no horário de atendimento humano."""
    now = datetime.now()
    # Verifica dia útil (segunda=0 a sexta=4)
    if now.weekday() > 4:
        return False
    return config.BUSINESS_HOURS_START <= now.hour < config.BUSINESS_HOURS_END


def create_ticket(
    phone: str,
    message: str,
    reason: str,
    history: list[dict],
    priority: str = "normal",
) -> dict:
    """
    Cria um ticket de suporte para atendimento humano.

    Salva em JSON na pasta tickets/ para que a equipe possa visualizar.

    Args:
        phone: Número do cliente.
        message: Última mensagem do cliente.
        reason: Motivo do escalonamento.
        history: Histórico da conversa.
        priority: "urgent" ou "normal".

    Returns:
        Dict com dados do ticket.
    """
    from datetime import datetime
    import uuid

    ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:4].upper()}"

    ticket = {
        "id": ticket_id,
        "phone": phone[-4:] + "****",    # anonimiza por privacidade
        "priority": priority,
        "reason": reason,
        "last_message": message,
        "created_at": datetime.now().isoformat(),
        "status": "open",
        "conversation_turns": len(history) // 2,
        "history_summary": [
            {"role": m["role"], "preview": m["content"][:80]}
            for m in history[-6:]  # últimas 3 trocas
        ],
    }

    # Salva o ticket em arquivo JSON
    tickets_dir = Path("tickets")
    tickets_dir.mkdir(exist_ok=True)

    filepath = tickets_dir / f"{ticket_id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ticket, f, ensure_ascii=False, indent=2)

    logger.info(
        "Ticket criado: %s | Prioridade: %s | Motivo: %s",
        ticket_id,
        priority,
        reason,
    )

    return ticket


def get_escalation_message(ticket: dict) -> str:
    """
    Gera a mensagem enviada ao cliente quando há escalonamento.
    Varia conforme horário e prioridade.
    """
    ticket_id = ticket["id"]

    if is_business_hours():
        if ticket["priority"] == "urgent":
            return (
                "⚠️ Entendi que você está passando por uma situação urgente.\n\n"
                f"Estou transferindo para um atendente humano agora.\n"
                f"Seu protocolo: *{ticket_id}*\n\n"
                "Um especialista entrará em contato em breve. "
                "Se preferir ligar: (11) 99000-1234"
            )
        return (
            "Vou transferir você para um atendente especialista. 👨‍💼\n\n"
            f"Seu protocolo de atendimento: *{ticket_id}*\n\n"
            "Tempo de espera estimado: até 30 minutos em dias úteis. "
            "Você também pode ligar: (11) 99000-1234"
        )
    else:
        return (
            "Nosso horário de atendimento humano é segunda a sexta, das 8h às 18h. 🕐\n\n"
            f"Registramos sua solicitação com o protocolo: *{ticket_id}*\n\n"
            "Nossa equipe entrará em contato no próximo dia útil. "
            "Para urgências, envie e-mail para: suporte@vendamais.com.br"
        )