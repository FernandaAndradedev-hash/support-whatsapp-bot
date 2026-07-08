import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


def _require(key: str) -> str:
    value = os.getenv(key, "").strip()
    if not value:
        print(f"\nERRO: Variável '{key}' não encontrada no .env\n", file=sys.stderr)
        sys.exit(1)
    return value


# APIs ──────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = _require("ANTHROPIC_API_KEY")
OPENAI_API_KEY: str = _require("OPENAI_API_KEY")

# Qdrant ────────────────────────────────────────────────────────────────────
QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "shopbot_knowledge")

# Evolution API ─────────────────────────────────────────────────────────────
EVOLUTION_API_URL: str = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
EVOLUTION_API_KEY: str = _require("EVOLUTION_API_KEY")
EVOLUTION_INSTANCE: str = os.getenv("EVOLUTION_INSTANCE", "vendamais-suporte")
WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")

# Modelos ───────────────────────────────────────────────────────────────────
EMBEDDING_MODEL: str = "text-embedding-3-small"
EMBEDDING_DIMENSIONS: int = 1536
LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-haiku-4-5")

# Segurança ─────────────────────────────────────────────────────────────────
MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "500"))
RATE_LIMIT_MAX_MESSAGES: int = int(os.getenv("RATE_LIMIT_MAX_MESSAGES", "10"))
RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

# RAG ───────────────────────────────────────────────────────────────────────
RETRIEVAL_TOP_K: int = 4
MIN_SCORE_THRESHOLD: float = 0.72
CHUNK_SIZE: int = 600
CHUNK_OVERLAP: int = 100

# Escalonamento ─────────────────────────────────────────────────────────────
MAX_BOT_ATTEMPTS: int = int(os.getenv("MAX_BOT_ATTEMPTS", "2"))
ESCALATION_REFUND_THRESHOLD: float = float(os.getenv("ESCALATION_REFUND_THRESHOLD", "500"))
BUSINESS_HOURS_START: int = int(os.getenv("BUSINESS_HOURS_START", "8"))
BUSINESS_HOURS_END: int = int(os.getenv("BUSINESS_HOURS_END", "18"))

# Conversa ──────────────────────────────────────────────────────────────────
MAX_HISTORY_MESSAGES: int = 10
SESSION_TTL: int = 1800