# ShopBot — Suporte Técnico com Escalonamento Inteligente

> Atendente automático de suporte via WhatsApp para a VendaMais E-commerce.
> Responde dúvidas sobre pedidos e devoluções usando RAG, e escala automaticamente
> para humano quando necessário.

---

## Funcionalidades

- Atendimento automático via WhatsApp (Evolution API)
- RAG sobre base de conhecimento do e-commerce (Qdrant)
- Memória de conversa por sessão
- Escalonamento inteligente automático:
  - Pedido de humano → escala imediatamente
  - Fraude/produto danificado → escala com prioridade urgente
  - Reembolso > R$ 500 → escala para aprovação
  - Bot sem resposta 2x → escala automaticamente
- Sistema de tickets em JSON para a equipe
- Rate limiting, sanitização e proteção contra injection

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| WhatsApp | Evolution API v2 |
| Webhook | FastAPI (async) |
| RAG | Qdrant + OpenAI Embeddings |
| LLM | Anthropic Claude Haiku |
| Memória | Dict em memória |

---

## Como rodar

```bash
git clone https://github.com/FernandaAndradedev-hash/support-whatsapp-bot
cd support-whatsapp-bot
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Preencha as chaves no .env

docker-compose up -d
python src/ingest.py
uvicorn src.api:app --reload --port 8000
```

---

## Testes

```bash
pytest tests/ -v
```

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.