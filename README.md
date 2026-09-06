# Enviador de E-mails HTML

Aplicação web desenvolvida em Python com Streamlit para envio de e-mails no formato HTML.

## Funcionalidades

- **Carregar arquivo HTML**: Faça upload de um arquivo `.html` ou `.htm` existente e envie-o como corpo do e-mail.
- **Criar e-mail do zero**: Utilize modelos profissionais prontos (Newsletter Corporativa, Convite Formal, Aviso/Comunicado e E-mail Minimalista), preencha os campos e visualize o resultado em tempo real.
- **Pré-visualização**: Visualize o e-mail exatamente como será recebido.
- **Configuração SMTP flexível**: Compatível com Gmail, Outlook, servidores corporativos e outros provedores.
- **Segurança**: Utiliza STARTTLS e recomenda o uso de senhas de aplicativo.

## Requisitos

- Python 3.9 ou superior
- Bibliotecas listadas em `requirements.txt`

## Instalação

1. Crie e ative um ambiente virtual (recomendado):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# ou
venv\Scripts\activate      # Windows
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador (geralmente em `http://localhost:8501`).

## Configuração de e-mail (Gmail)

Se você utiliza o Gmail com verificação em duas etapas:

1. Acesse sua Conta Google → Segurança.
2. Em "Como fazer login no Google", selecione **Senhas de app**.
3. Gere uma nova senha de aplicativo para "E-mail" ou "Outro".
4. Utilize o e-mail completo como usuário e a senha gerada (16 caracteres) no campo de senha da aplicação.

Configurações típicas:

| Provedor     | Servidor SMTP       | Porta | TLS  |
|--------------|---------------------|-------|------|
| Gmail        | smtp.gmail.com      | 587   | Sim  |
| Outlook      | smtp.office365.com  | 587   | Sim  |
| Yahoo        | smtp.mail.yahoo.com | 587   | Sim  |

## Estrutura do projeto

```
email_html_sender/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências
└── README.md           # Este arquivo
```

## Observações importantes

- As credenciais de e-mail nunca são armazenadas. Elas existem apenas durante a sessão.
- Recomenda-se fortemente o uso de senhas de aplicativo em vez da senha principal da conta.
- O conteúdo HTML é enviado com uma versão texto simples como fallback para clientes de e-mail que não suportam HTML.
- Teste sempre o envio para um endereço próprio antes de utilizá-lo em produção.

## Licença

Este projeto é fornecido como está, para fins educacionais e de uso pessoal/profissional. Adapte-o conforme suas necessidades.
