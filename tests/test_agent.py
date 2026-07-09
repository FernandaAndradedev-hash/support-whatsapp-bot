import os
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-fake")
os.environ.setdefault("OPENAI_API_KEY", "sk-test-fake")
os.environ.setdefault("EVOLUTION_API_KEY", "test-key")

from unittest.mock import MagicMock, patch
from memory import _sessions


class TestAgent:

    def setup_method(self):
        _sessions.clear()

    @patch("agent._client")
    @patch("agent.retrieve")
    def test_resposta_normal(self, mock_retrieve, mock_client):
        mock_retrieve.return_value = [
            {"text": "Prazo: 3 dias úteis.", "title": "Entrega", "category": "entrega", "score": 0.9}
        ]
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="O prazo de entrega é de 3 dias úteis.")]
        mock_client.messages.create.return_value = mock_response

        from agent import process_message
        result = process_message("5511999999999", "Qual o prazo de entrega?")

        assert isinstance(result, str)
        assert len(result) > 0

    def test_escalonamento_por_trigger(self):
        from agent import process_message
        result = process_message("5511888888888", "Quero falar com um atendente humano")

        assert "protocolo" in result.lower() or "TKT-" in result or "equipe" in result.lower()

    def test_encerramento_limpa_sessao(self):
        from agent import process_message
        result = process_message("5511777777777", "obrigado")

        assert "ajud" in result.lower() or "compras" in result.lower()

    def test_ja_escalado_redireciona(self):
        from agent import process_message
        from memory import mark_escalated

        mark_escalated("5511666666666")
        result = process_message("5511666666666", "Outra pergunta")

        assert "equipe" in result.lower() or "suporte" in result.lower()