"""
Base de conhecimento fictícia da VendaMais E-commerce.
Cobre as principais dúvidas de suporte de um e-commerce de eletrônicos.
"""

KNOWLEDGE_DOCUMENTS = [
    {
        "title": "Sobre a VendaMais",
        "category": "geral",
        "content": """
A VendaMais é um e-commerce especializado em eletrônicos e eletrodomésticos,
fundado em 2015, com sede em São Paulo, SP.

Contatos:
- WhatsApp Suporte: (11) 99000-1234
- E-mail: suporte@vendamais.com.br
- Site: www.vendamais.com.br
- Horário de atendimento humano: segunda a sexta, 8h às 18h

Formas de pagamento aceitas:
- Cartão de crédito (até 12x sem juros para pedidos acima de R$ 300)
- Cartão de débito
- Pix (5% de desconto)
- Boleto bancário (vencimento em 3 dias úteis)

A VendaMais não realiza atendimento presencial. Todo suporte é feito
remotamente via WhatsApp, e-mail ou chat no site.
        """,
    },
    {
        "title": "Prazo e política de entrega",
        "category": "entrega",
        "content": """
PRAZOS DE ENTREGA

Prazo padrão por região:
- São Paulo capital: 1 a 2 dias úteis
- Grande São Paulo e interior SP: 2 a 4 dias úteis
- Sul e Sudeste (exceto SP): 3 a 6 dias úteis
- Nordeste, Norte e Centro-Oeste: 5 a 10 dias úteis

Os prazos começam a contar após a confirmação do pagamento.
Para boleto, o prazo inicia após a compensação (geralmente 2 dias úteis após pagamento).

RASTREAMENTO
Após o envio, você recebe o código de rastreio por e-mail e WhatsApp.
Rastreie em: www.vendamais.com.br/rastrear ou nos sites dos Correios e transportadoras.

ATRASO NA ENTREGA
Se o pedido não chegar no prazo estimado:
1. Verifique o rastreamento pelo link enviado
2. Se estiver parado há mais de 3 dias, entre em contato conosco
3. Pedidos extraviados são ressarcidos ou reenviados em até 10 dias úteis

ENTREGA NÃO REALIZADA
Se você não estava no local na hora da entrega:
- Os Correios fazem até 3 tentativas de entrega
- Após 3 tentativas, o produto fica disponível para retirada por 7 dias
- Se não retirado, retorna à VendaMais e um novo envio pode ser agendado
        """,
    },
    {
        "title": "Política de troca e devolução",
        "category": "troca_devolucao",
        "content": """
DIREITO DE ARREPENDIMENTO (Código de Defesa do Consumidor)
- Prazo: 7 dias corridos a partir do recebimento
- Produto deve estar sem uso, na embalagem original com todos os acessórios
- O frete de devolução é por nossa conta neste caso
- Reembolso em até 10 dias úteis após recebimento do produto

TROCA POR DEFEITO
- Prazo: 90 dias para defeitos de fabricação (garantia legal)
- Eletrônicos têm garantia adicional de 12 meses da VendaMais
- Processo: abra chamado pelo WhatsApp com foto/vídeo do defeito
- Nossa equipe técnica avalia em até 48 horas
- Se confirmado defeito: troca imediata ou reembolso, à sua escolha

COMO SOLICITAR DEVOLUÇÃO
1. Entre em contato pelo WhatsApp: (11) 99000-1234
2. Informe o número do pedido e motivo da devolução
3. Aguarde aprovação (até 24h em dias úteis)
4. Você receberá a etiqueta de postagem por e-mail
5. Poste o produto nos Correios
6. Após recebimento, processamos o reembolso em até 10 dias úteis

PRODUTOS QUE NÃO ACEITAMOS DEVOLUÇÃO
- Produtos com lacre violado (exceto defeito de fabricação)
- Produtos com danos causados pelo cliente
- Software e jogos com lacre aberto
- Produtos personalizados
        """,
    },
    {
        "title": "Reembolso e cancelamento de pedido",
        "category": "reembolso",
        "content": """
CANCELAMENTO DE PEDIDO

Pedido ainda não enviado:
- Cancele pelo site em "Meus Pedidos" ou pelo WhatsApp
- Reembolso em até 5 dias úteis (cartão de crédito pode levar até 2 faturas)

Pedido já enviado:
- Não é possível cancelar após o envio
- Você pode recusar a entrega ou devolver após receber
- O produto retorna à VendaMais e o reembolso é processado em até 10 dias úteis

FORMAS DE REEMBOLSO
- Pix: reembolso em até 2 dias úteis no mesmo CPF do pagamento
- Cartão de crédito: estorno em até 2 faturas (30 a 60 dias)
- Boleto: reembolso via transferência bancária em até 5 dias úteis
- Vale-crédito VendaMais: disponível em até 24h (opcional, válido por 1 ano)

REEMBOLSO PARCIAL
Em casos de pedidos com múltiplos itens onde apenas um é devolvido,
o reembolso é proporcional ao valor do item devolvido.

PEDIDOS ACIMA DE R$ 500
Reembolsos acima de R$ 500 passam por aprovação do time financeiro
e podem levar até 5 dias úteis adicionais para processamento.
        """,
    },
    {
        "title": "Garantia dos produtos",
        "category": "garantia",
        "content": """
GARANTIA LEGAL (Código de Defesa do Consumidor)
- Produtos duráveis (eletrônicos, eletrodomésticos): 90 dias

GARANTIA ADICIONAL VENDAMAIS
- Eletrônicos (smartphones, notebooks, tablets): 12 meses
- Eletrodomésticos de grande porte: 12 meses
- Eletrodomésticos de pequeno porte: 6 meses
- Acessórios (cabos, capas, carregadores): 3 meses

A garantia cobre defeitos de fabricação. Não cobre:
- Danos por mau uso, quedas ou líquidos
- Desgaste natural pelo uso
- Modificações não autorizadas
- Danos causados por tensão elétrica inadequada

COMO ACIONAR A GARANTIA
1. Fotografe ou grave vídeo do defeito
2. Entre em contato pelo WhatsApp com o número do pedido
3. Nossa equipe técnica analisa em até 48 horas
4. Opções: reparo, substituição ou reembolso (a critério da VendaMais)

ASSISTÊNCIA TÉCNICA AUTORIZADA
Para produtos com mais de 12 meses de uso, indicamos as assistências
técnicas autorizadas do fabricante. Lista disponível em:
www.vendamais.com.br/assistencia-tecnica
        """,
    },
    {
        "title": "Perguntas frequentes",
        "category": "faq",
        "content": """
P: Como acompanho meu pedido?
R: Você recebe o código de rastreio por e-mail e WhatsApp após o envio.
Rastreie em www.vendamais.com.br/rastrear informando o número do pedido ou CPF.

P: Posso alterar o endereço de entrega após finalizar o pedido?
R: Sim, mas apenas se o pedido ainda não foi enviado. Entre em contato imediatamente
pelo WhatsApp. Após o envio, não é possível alterar o endereço.

P: O produto chegou com a caixa danificada. E agora?
R: Se o produto interno estiver funcionando, pode ser apenas dano na embalagem
durante o transporte. Se houver dano no produto, fotografe e entre em contato
em até 48h do recebimento para acionar a garantia.

P: Vocês entregam em todo o Brasil?
R: Sim, entregamos para todo o território nacional. Locais remotos podem
ter prazo adicional. Verifique a disponibilidade de entrega no site.

P: Posso retirar meu pedido numa loja física?
R: Não, a VendaMais opera exclusivamente online. Não temos lojas físicas.

P: Como emito a nota fiscal do meu pedido?
R: A nota fiscal eletrônica é enviada por e-mail automaticamente após a confirmação
do pagamento. Também está disponível em "Meus Pedidos" no site.

P: Vocês vendem para CNPJ?
R: Sim. No checkout, informe o CNPJ para emissão da nota fiscal empresarial.
Temos condições especiais para empresas — consulte pelo e-mail corporativo@vendamais.com.br.

P: O produto que recebi é diferente do anunciado. O que fazer?
R: Entre em contato imediatamente com fotos do produto recebido e do anúncio.
Casos de produto errado são tratados como prioridade — troca ou reembolso em até 5 dias úteis.
        """,
    },
]


def get_all_documents() -> list[dict]:
    return KNOWLEDGE_DOCUMENTS


def get_full_text(doc: dict) -> str:
    return f"{doc['title']}\n\n{doc['content'].strip()}"