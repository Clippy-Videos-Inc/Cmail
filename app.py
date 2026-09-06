"""
Aplicação Streamlit para envio de e-mails HTML.
Permite carregar um arquivo HTML existente ou criar um e-mail profissional a partir de modelos.
"""

import streamlit as st
import smtplib
from email.message import EmailMessage
from io import StringIO
import html

# Configuração da página
st.set_page_config(
    page_title="Enviador de E-mails HTML",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a5568;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f7fafc;
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    .preview-box {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px;
        background-color: #ffffff;
        max-height: 600px;
        overflow-y: auto;
    }
    .success-box {
        padding: 1rem;
        background-color: #c6f6d5;
        border-left: 5px solid #38a169;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #fed7d7;
        border-left: 5px solid #e53e3e;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #ebf8ff;
        border-left: 5px solid #3182ce;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def get_professional_templates():
    """Retorna dicionário de modelos HTML profissionais."""
    templates = {
        "Newsletter Corporativa": """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter</title>
</head>
<body style="margin:0; padding:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color:#f4f7fa;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:#f4f7fa;">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color:#ffffff; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.08); overflow:hidden;">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%); padding: 30px 40px; text-align:center;">
                            <h1 style="margin:0; color:#ffffff; font-size:28px; font-weight:700;">{{TITULO}}</h1>
                            <p style="margin:8px 0 0; color:#bee3f8; font-size:14px;">{{SUBTITULO}}</p>
                        </td>
                    </tr>
                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin:0 0 20px; color:#2d3748; font-size:16px; line-height:1.6;">Olá {{NOME}},</p>
                            <p style="margin:0 0 20px; color:#4a5568; font-size:15px; line-height:1.7;">{{CONTEUDO}}</p>
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:30px 0;">
                                <tr>
                                    <td style="background-color:#2b6cb0; border-radius:6px;">
                                        <a href="{{LINK_BOTAO}}" style="display:inline-block; padding:14px 28px; color:#ffffff; text-decoration:none; font-weight:600; font-size:15px;">{{TEXTO_BOTAO}}</a>
                                    </td>
                                </tr>
                            </table>
                            <p style="margin:20px 0 0; color:#718096; font-size:14px; line-height:1.6;">{{RODAPE}}</p>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color:#edf2f7; padding:20px 40px; text-align:center;">
                            <p style="margin:0; color:#718096; font-size:12px;">© 2026 {{EMPRESA}}. Todos os direitos reservados.</p>
                            <p style="margin:8px 0 0; color:#a0aec0; font-size:11px;">Este é um e-mail automático. Por favor, não responda diretamente.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>""",

        "Convite Formal": """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Convite</title>
</head>
<body style="margin:0; padding:0; font-family: Georgia, 'Times New Roman', serif; background-color:#faf5f0;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:#faf5f0;">
        <tr>
            <td align="center" style="padding: 50px 20px;">
                <table role="presentation" width="560" cellspacing="0" cellpadding="0" border="0" style="background-color:#ffffff; border:1px solid #e2d5c3; border-radius:4px;">
                    <tr>
                        <td style="padding: 50px 40px; text-align:center;">
                            <p style="margin:0 0 10px; color:#8b7355; font-size:13px; letter-spacing:3px; text-transform:uppercase;">{{TIPO_EVENTO}}</p>
                            <h1 style="margin:0 0 25px; color:#3d2b1f; font-size:32px; font-weight:400; line-height:1.3;">{{TITULO}}</h1>
                            <div style="width:60px; height:2px; background-color:#c9a66b; margin:0 auto 30px;"></div>
                            <p style="margin:0 0 25px; color:#5a4a3a; font-size:16px; line-height:1.7;">{{CONVIDADO}},</p>
                            <p style="margin:0 0 30px; color:#5a4a3a; font-size:15px; line-height:1.8;">{{MENSAGEM}}</p>
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin:30px 0; background-color:#f9f5f0; border-radius:4px;">
                                <tr>
                                    <td style="padding:25px; text-align:center;">
                                        <p style="margin:0 0 8px; color:#8b7355; font-size:12px; letter-spacing:1px;">DATA E HORÁRIO</p>
                                        <p style="margin:0 0 15px; color:#3d2b1f; font-size:18px; font-weight:600;">{{DATA_HORA}}</p>
                                        <p style="margin:0 0 8px; color:#8b7355; font-size:12px; letter-spacing:1px;">LOCAL</p>
                                        <p style="margin:0; color:#3d2b1f; font-size:16px;">{{LOCAL}}</p>
                                    </td>
                                </tr>
                            </table>
                            <p style="margin:30px 0 0; color:#8b7355; font-size:14px; font-style:italic;">{{CONFIRMACAO}}</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color:#3d2b1f; padding:20px; text-align:center;">
                            <p style="margin:0; color:#e2d5c3; font-size:12px;">{{ORGANIZADOR}}</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>""",

        "Aviso / Comunicado": """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comunicado</title>
</head>
<body style="margin:0; padding:0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color:#f0f4f8;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr>
            <td align="center" style="padding: 30px 15px;">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color:#ffffff; border-radius:6px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                    <tr>
                        <td style="background-color:#2c5282; padding:18px 30px;">
                            <p style="margin:0; color:#ffffff; font-size:14px; font-weight:600; letter-spacing:0.5px;">{{CATEGORIA}}</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 35px 30px;">
                            <h2 style="margin:0 0 20px; color:#1a202c; font-size:22px; font-weight:700;">{{TITULO}}</h2>
                            <p style="margin:0 0 18px; color:#2d3748; font-size:15px; line-height:1.65;">Prezado(a) {{DESTINATARIO}},</p>
                            <p style="margin:0 0 18px; color:#4a5568; font-size:15px; line-height:1.65;">{{CORPO}}</p>
                            <div style="background-color:#ebf8ff; border-left:4px solid #3182ce; padding:16px 20px; margin:25px 0; border-radius:0 4px 4px 0;">
                                <p style="margin:0; color:#2c5282; font-size:14px; font-weight:600;">{{DESTAQUE_TITULO}}</p>
                                <p style="margin:6px 0 0; color:#2d3748; font-size:14px; line-height:1.5;">{{DESTAQUE_TEXTO}}</p>
                            </div>
                            <p style="margin:20px 0 0; color:#4a5568; font-size:14px; line-height:1.6;">{{ENCERRAMENTO}}</p>
                            <p style="margin:25px 0 0; color:#2d3748; font-size:14px;">Atenciosamente,<br><strong>{{REMETENTE}}</strong><br><span style="color:#718096;">{{CARGO}}</span></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color:#edf2f7; padding:16px 30px; text-align:center;">
                            <p style="margin:0; color:#718096; font-size:11px;">{{EMPRESA}} • {{CONTATO}}</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>""",

        "E-mail Minimalista": """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-mail</title>
</head>
<body style="margin:0; padding:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color:#ffffff;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="520" cellspacing="0" cellpadding="0" border="0">
                    <tr>
                        <td style="padding-bottom: 24px; border-bottom: 2px solid #000000;">
                            <h1 style="margin:0; color:#111111; font-size:24px; font-weight:700;">{{TITULO}}</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 32px 0;">
                            <p style="margin:0 0 16px; color:#333333; font-size:16px; line-height:1.6;">{{SAUDACAO}}</p>
                            <p style="margin:0 0 16px; color:#333333; font-size:16px; line-height:1.7;">{{CORPO}}</p>
                            <p style="margin:24px 0 0; color:#333333; font-size:16px;">{{ASSINATURA}}</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-top: 24px; border-top: 1px solid #e5e5e5;">
                            <p style="margin:0; color:#888888; font-size:12px;">{{RODAPE}}</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
    }
    return templates


def render_template(template_html: str, replacements: dict) -> str:
    """Substitui placeholders {{CHAVE}} pelos valores fornecidos."""
    result = template_html
    for key, value in replacements.items():
        # Escapa HTML para segurança, exceto se o usuário inserir HTML intencional
        safe_value = html.escape(str(value)) if value else ""
        result = result.replace(f"{{{{{key}}}}}", safe_value)
    return result


def send_html_email(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    from_email: str,
    to_email: str,
    subject: str,
    html_content: str,
    use_tls: bool = True
) -> tuple[bool, str]:
    """
    Envia um e-mail HTML usando SMTP.
    Retorna (sucesso: bool, mensagem: str).
    """
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        # Versão texto simples como fallback
        plain_text = "Este e-mail contém conteúdo HTML. Por favor, visualize-o em um cliente que suporte HTML."
        msg.set_content(plain_text)
        msg.add_alternative(html_content, subtype="html")

        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            if use_tls:
                server.starttls()
            server.login(username, password)
            server.send_message(msg)

        return True, "E-mail enviado com sucesso."
    except smtplib.SMTPAuthenticationError:
        return False, "Erro de autenticação. Verifique o usuário e a senha (utilize senha de aplicativo se necessário)."
    except smtplib.SMTPConnectError:
        return False, "Não foi possível conectar ao servidor SMTP. Verifique o host e a porta."
    except smtplib.SMTPException as e:
        return False, f"Erro SMTP: {str(e)}"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def smtp_sidebar():
    """Renderiza a seção de configuração SMTP na barra lateral."""
    st.sidebar.header("Configurações SMTP")
    st.sidebar.markdown(
        '<div class="info-box">Insira as credenciais do seu provedor de e-mail. '
        'Para Gmail, utilize uma <strong>senha de aplicativo</strong>.</div>',
        unsafe_allow_html=True
    )

    smtp_host = st.sidebar.text_input("Servidor SMTP", value="smtp.gmail.com", help="Ex.: smtp.gmail.com, smtp.office365.com")
    smtp_port = st.sidebar.number_input("Porta", min_value=1, max_value=65535, value=587)
    use_tls = st.sidebar.checkbox("Usar TLS (STARTTLS)", value=True)

    username = st.sidebar.text_input("Usuário / E-mail", placeholder="seu@email.com")
    password = st.sidebar.text_input("Senha / Senha de aplicativo", type="password")

    from_email = st.sidebar.text_input("Remetente (From)", value=username if username else "", help="Geralmente o mesmo e-mail de autenticação")
    to_email = st.sidebar.text_input("Destinatário (To)", placeholder="destinatario@email.com")
    subject = st.sidebar.text_input("Assunto", placeholder="Assunto do e-mail")

    return {
        "smtp_host": smtp_host,
        "smtp_port": int(smtp_port),
        "use_tls": use_tls,
        "username": username,
        "password": password,
        "from_email": from_email,
        "to_email": to_email,
        "subject": subject
    }


def main():
    st.markdown('<p class="main-header">📧 Enviador de E-mails HTML</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Carregue um arquivo HTML ou crie um e-mail profissional a partir de modelos prontos.</p>',
        unsafe_allow_html=True
    )

    config = smtp_sidebar()

    tab1, tab2 = st.tabs(["📁 Carregar arquivo HTML", "✏️ Criar e-mail do zero"])

    # ========== ABA 1: Upload de arquivo ==========
    with tab1:
        st.subheader("Selecionar arquivo HTML")
        uploaded_file = st.file_uploader(
            "Escolha um arquivo .html ou .htm",
            type=["html", "htm"],
            help="O conteúdo do arquivo será utilizado como corpo do e-mail."
        )

        html_content = None
        if uploaded_file is not None:
            try:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                html_content = stringio.read()
                st.success(f"Arquivo carregado: **{uploaded_file.name}** ({len(html_content)} caracteres)")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")

        if html_content:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("**Código HTML**")
                st.code(html_content[:3000] + ("..." if len(html_content) > 3000 else ""), language="html")
            with col2:
                st.markdown("**Pré-visualização**")
                st.components.v1.html(html_content, height=500, scrolling=True)

            if st.button("🚀 Enviar e-mail (arquivo carregado)", type="primary", key="send_upload"):
                if not all([config["username"], config["password"], config["from_email"], config["to_email"], config["subject"]]):
                    st.error("Preencha todos os campos obrigatórios na barra lateral (usuário, senha, remetente, destinatário e assunto).")
                else:
                    with st.spinner("Enviando e-mail..."):
                        success, message = send_html_email(
                            smtp_host=config["smtp_host"],
                            smtp_port=config["smtp_port"],
                            username=config["username"],
                            password=config["password"],
                            from_email=config["from_email"],
                            to_email=config["to_email"],
                            subject=config["subject"],
                            html_content=html_content,
                            use_tls=config["use_tls"]
                        )
                    if success:
                        st.markdown(f'<div class="success-box">{message}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">{message}</div>', unsafe_allow_html=True)

    # ========== ABA 2: Criar do zero ==========
    with tab2:
        st.subheader("Criar e-mail profissional a partir de modelo")

        templates = get_professional_templates()
        selected_template = st.selectbox(
            "Escolha um modelo",
            options=list(templates.keys()),
            help="Selecione um dos modelos profissionais disponíveis."
        )

        st.markdown("---")
        st.markdown("**Preencha os campos do modelo**")

        # Campos dinâmicos conforme o modelo
        replacements = {}

        if selected_template == "Newsletter Corporativa":
            col_a, col_b = st.columns(2)
            with col_a:
                replacements["TITULO"] = st.text_input("Título principal", value="Novidades da Empresa")
                replacements["SUBTITULO"] = st.text_input("Subtítulo", value="Edição mensal • Setembro 2026")
                replacements["NOME"] = st.text_input("Nome do destinatário", value="Cliente")
                replacements["EMPRESA"] = st.text_input("Nome da empresa", value="Sua Empresa Ltda.")
            with col_b:
                replacements["TEXTO_BOTAO"] = st.text_input("Texto do botão", value="Saiba mais")
                replacements["LINK_BOTAO"] = st.text_input("Link do botão", value="https://www.exemplo.com")
                replacements["RODAPE"] = st.text_area("Texto de rodapé", value="Agradecemos a sua atenção e preferência.")
            replacements["CONTEUDO"] = st.text_area(
                "Conteúdo principal",
                value="Estamos felizes em compartilhar as novidades deste mês. Nossa equipe tem trabalhado intensamente para trazer melhorias e novos recursos que irão transformar a sua experiência.",
                height=120
            )

        elif selected_template == "Convite Formal":
            col_a, col_b = st.columns(2)
            with col_a:
                replacements["TIPO_EVENTO"] = st.text_input("Tipo de evento", value="Convite Especial")
                replacements["TITULO"] = st.text_input("Título do evento", value="Jantar de Confraternização")
                replacements["CONVIDADO"] = st.text_input("Nome do convidado", value="Sr(a). Nome")
                replacements["DATA_HORA"] = st.text_input("Data e horário", value="15 de outubro de 2026, às 19h30")
            with col_b:
                replacements["LOCAL"] = st.text_input("Local", value="Salão Nobre – Hotel Exemplo, São Paulo")
                replacements["ORGANIZADOR"] = st.text_input("Organizador", value="Diretoria de Relacionamento")
                replacements["CONFIRMACAO"] = st.text_input("Pedido de confirmação", value="Por favor, confirme sua presença até 10 de outubro.")
            replacements["MENSAGEM"] = st.text_area(
                "Mensagem do convite",
                value="Temos a honra de convidá-lo(a) para o nosso tradicional jantar de confraternização. Será uma ocasião especial para celebrarmos juntos os resultados do ano e fortalecermos nossos laços.",
                height=100
            )

        elif selected_template == "Aviso / Comunicado":
            col_a, col_b = st.columns(2)
            with col_a:
                replacements["CATEGORIA"] = st.text_input("Categoria / Tag", value="COMUNICADO OFICIAL")
                replacements["TITULO"] = st.text_input("Título do comunicado", value="Atualização importante sobre o serviço")
                replacements["DESTINATARIO"] = st.text_input("Destinatário", value="Colaborador(a)")
                replacements["DESTAQUE_TITULO"] = st.text_input("Título do destaque", value="Atenção")
            with col_b:
                replacements["REMETENTE"] = st.text_input("Nome do remetente", value="Departamento de Comunicação")
                replacements["CARGO"] = st.text_input("Cargo", value="Gerência de Relacionamento")
                replacements["EMPRESA"] = st.text_input("Empresa", value="Empresa Exemplo S.A.")
                replacements["CONTATO"] = st.text_input("Contato", value="contato@exemplo.com")
            replacements["CORPO"] = st.text_area(
                "Corpo do comunicado",
                value="Informamos que a partir do próximo mês serão implementadas melhorias em nossos processos internos. Estas mudanças visam aumentar a eficiência e a qualidade do atendimento.",
                height=100
            )
            replacements["DESTAQUE_TEXTO"] = st.text_area(
                "Texto do destaque",
                value="As alterações entrarão em vigor a partir de 1º de outubro de 2026. Não será necessária nenhuma ação da sua parte.",
                height=80
            )
            replacements["ENCERRAMENTO"] = st.text_input(
                "Encerramento",
                value="Em caso de dúvidas, nossa equipe permanece à disposição."
            )

        else:  # Minimalista
            replacements["TITULO"] = st.text_input("Título", value="Mensagem importante")
            replacements["SAUDACAO"] = st.text_input("Saudação", value="Olá,")
            replacements["CORPO"] = st.text_area(
                "Corpo da mensagem",
                value="Escreva aqui o conteúdo principal do seu e-mail. Mantenha o texto claro, objetivo e profissional.",
                height=150
            )
            replacements["ASSINATURA"] = st.text_area(
                "Assinatura",
                value="Atenciosamente,\nSeu Nome\nCargo | Empresa",
                height=80
            )
            replacements["RODAPE"] = st.text_input("Rodapé", value="Empresa Exemplo • www.exemplo.com")

        # Gerar HTML final
        template_html = templates[selected_template]
        final_html = render_template(template_html, replacements)

        # Opção de editar o HTML gerado
        with st.expander("Editar HTML gerado (avançado)", expanded=False):
            final_html = st.text_area(
                "Código HTML",
                value=final_html,
                height=300,
                key="html_editor"
            )

        # Pré-visualização
        st.markdown("**Pré-visualização do e-mail**")
        st.components.v1.html(final_html, height=550, scrolling=True)

        # Botão de envio
        if st.button("🚀 Enviar e-mail criado", type="primary", key="send_created"):
            if not all([config["username"], config["password"], config["from_email"], config["to_email"], config["subject"]]):
                st.error("Preencha todos os campos obrigatórios na barra lateral (usuário, senha, remetente, destinatário e assunto).")
            elif not final_html.strip():
                st.error("O conteúdo HTML está vazio.")
            else:
                with st.spinner("Enviando e-mail..."):
                    success, message = send_html_email(
                        smtp_host=config["smtp_host"],
                        smtp_port=config["smtp_port"],
                        username=config["username"],
                        password=config["password"],
                        from_email=config["from_email"],
                        to_email=config["to_email"],
                        subject=config["subject"],
                        html_content=final_html,
                        use_tls=config["use_tls"]
                    )
                if success:
                    st.markdown(f'<div class="success-box">{message}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-box">{message}</div>', unsafe_allow_html=True)

    # Rodapé
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; color:#718096; font-size:0.85rem;">
            Aplicação desenvolvida em Python com Streamlit.<br>
            Utilize sempre senhas de aplicativo e conexões seguras (TLS).<br>
            Não armazene credenciais em código-fonte ou repositórios públicos.
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
