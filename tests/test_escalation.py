import os
os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-fake")
os.environ.setdefault("OPENAI_API_KEY", "sk-test-fake")
os.environ.setdefault("EVOLUTION_API_KEY", "test-key")

import pytest
from escalation import check_escalation_triggers, create_ticket, is_business_hours


class TestEscalationTriggers:

    def test_pedido_de_humano_escala(self):
        should, reason = check_escalation_triggers("Quero falar com um atendente")
        assert should is True

    def test_fraude_escala(self):
        should, reason = check_escalation_triggers("Acho que fui vítima de fraude")
        assert should is True

    def test_produto_quebrado_escala(self):
        should, reason = check_escalation_triggers("O produto chegou quebrado")
        assert should is True

    def test_procon_escala(self):
        should, reason = check_escalation_triggers("Vou reclamar no Procon")
        assert should is True

    def test_mensagem_normal_nao_escala(self):
        should, reason = check_escalation_triggers("Qual o prazo de entrega?")
        assert should is False

    def test_valor_alto_escala(self):
        should, reason = check_escalation_triggers("Quero reembolso de R$ 600,00")
        assert should is True

    def test_valor_baixo_nao_escala(self):
        should, reason = check_escalation_triggers("Quero reembolso de R$ 100,00")
        assert should is False

    def test_gerente_escala(self):
        should, reason = check_escalation_triggers("Preciso falar com o gerente")
        assert should is True


class TestCreateTicket:

    def test_cria_ticket_com_id(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "tickets").mkdir()

        ticket = create_ticket(
            phone="5511999999999",
            message="Produto quebrado",
            reason="Produto danificado",
            history=[],
            priority="urgent",
        )

        assert "id" in ticket
        assert ticket["id"].startswith("TKT-")
        assert ticket["priority"] == "urgent"
        assert ticket["status"] == "open"

    def test_telefone_anonimizado(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "tickets").mkdir()

        ticket = create_ticket(
            phone="5511999999999",
            message="Teste",
            reason="Teste",
            history=[],
        )

        assert "5511999999999" not in ticket["phone"]
        assert "****" in ticket["phone"]