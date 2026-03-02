import smtplib
import logging
import traceback
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from config import settings

# ─── Logger dedicado para el servicio de email ────────────────────────────────
logger = logging.getLogger("email_service")

if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setLevel(logging.DEBUG)
    _fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [EMAIL_SERVICE] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    _handler.setFormatter(_fmt)
    logger.addHandler(_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
# ──────────────────────────────────────────────────────────────────────────────


class EmailService:
    """Servicio interno para envío de emails desde la infraestructura"""
    
    @staticmethod
    def send_email(
        to: str,
        subject: str,
        message: str,
        company_id: Optional[int] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        html: bool = True
    ) -> bool:

        EMAIL_ENABLED = True  # Cambiar a False para deshabilitar envíos

        logger.info("=" * 60)
        logger.info("INICIO send_email()")
        logger.info(f"  EMAIL_ENABLED : {EMAIL_ENABLED}")
        logger.info(f"  Destinatario  : {to!r}")
        logger.info(f"  Asunto        : {subject!r}")
        logger.info(f"  company_id    : {company_id!r}")
        logger.info(f"  CC entrada    : {cc}")
        logger.info(f"  BCC entrada   : {bcc}")
        logger.info(f"  HTML          : {html}")
        logger.info(f"  SMTP_HOST     : {settings.SMTP_HOST}")
        logger.info(f"  SMTP_PORT     : {settings.SMTP_PORT}")
        logger.info(f"  SMTP_USER     : {settings.SMTP_USER!r}")
        logger.info(f"  FROM_EMAIL    : {settings.SMTP_FROM_EMAIL!r}")
        logger.info(f"  FROM_NAME     : {settings.SMTP_FROM_NAME!r}")

        if not EMAIL_ENABLED:
            logger.warning("Envío deshabilitado (EMAIL_ENABLED=False). Email NO enviado.")
            return True

        # ── Validaciones previas ──────────────────────────────────────────────
        if not to or not to.strip():
            logger.error("FALLO: El campo 'to' está vacío o es None. No se puede enviar.")
            return False

        if not subject or not subject.strip():
            logger.warning("El campo 'subject' está vacío.")

        if not message or not message.strip():
            logger.warning("El campo 'message' está vacío.")

        try:
            # ── Construir mensaje MIME ────────────────────────────────────────
            logger.debug("Construyendo mensaje MIME...")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            msg['To'] = to

            # ── CC / BCC ──────────────────────────────────────────────────────
            if company_id != 90:
                default_cc  = ['dalmaquinaria@ddg.com.mx', 'david@ddg.com.mx', 'ventas.unm@ddg.com.mx']
                default_bcc = ['operacionmbackup@gmail.com']
                cc  = list(set((cc  or []) + default_cc))
                bcc = list(set((bcc or []) + default_bcc))
                logger.debug(f"company_id != 90 → CC/BCC por defecto aplicados.")
            else:
                logger.debug("company_id == 90 → Sin CC/BCC por defecto.")

            logger.info(f"  CC final  : {cc}")
            logger.info(f"  BCC final : {bcc}")

            if cc:
                msg['Cc'] = ', '.join(cc)

            # ── Body ──────────────────────────────────────────────────────────
            mime_type = 'html' if html else 'plain'
            msg.attach(MIMEText(message, mime_type, 'utf-8'))
            logger.debug(f"Body adjuntado como text/{mime_type}.")

            # ── Lista de destinatarios reales ─────────────────────────────────
            recipients = [to] + (cc or []) + (bcc or [])
            logger.info(f"  Recipients reales (SMTP RCPT TO): {recipients}")

            # ── Conectar al servidor SMTP ─────────────────────────────────────
            logger.debug(f"Resolviendo DNS para {settings.SMTP_HOST!r}...")
            try:
                ip = socket.gethostbyname(settings.SMTP_HOST)
                logger.debug(f"DNS OK → {settings.SMTP_HOST} = {ip}")
            except socket.gaierror as dns_err:
                logger.error(f"FALLO DNS: No se pudo resolver {settings.SMTP_HOST!r} → {dns_err}")
                raise

            logger.debug(f"Abriendo conexión TCP a {settings.SMTP_HOST}:{settings.SMTP_PORT}...")
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
                logger.debug("Conexión TCP establecida. Iniciando EHLO...")
                server.set_debuglevel(1)   # <── muestra diálogo SMTP crudo en consola

                logger.debug("Ejecutando STARTTLS...")
                server.starttls()
                logger.debug("STARTTLS OK.")

                logger.debug(f"Autenticando como {settings.SMTP_USER!r}...")
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                logger.debug("Login OK.")

                logger.debug("Enviando mensaje (sendmail)...")
                refused = server.sendmail(settings.SMTP_FROM_EMAIL, recipients, msg.as_string())

                if refused:
                    logger.error(f"ATENCIÓN: Algunos destinatarios fueron rechazados: {refused}")
                else:
                    logger.debug("sendmail() completado sin rechazos.")

            logger.info("Email enviado EXITOSAMENTE.")
            logger.info("=" * 60)
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"FALLO AUTENTICACIÓN SMTP: {e.smtp_code} – {e.smtp_error}")
            logger.error(traceback.format_exc())
        except smtplib.SMTPConnectError as e:
            logger.error(f"FALLO CONEXIÓN SMTP: {e}")
            logger.error(traceback.format_exc())
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"DESTINATARIOS RECHAZADOS: {e.recipients}")
            logger.error(traceback.format_exc())
        except smtplib.SMTPException as e:
            logger.error(f"ERROR SMTP GENÉRICO: {e}")
            logger.error(traceback.format_exc())
        except socket.timeout:
            logger.error(f"TIMEOUT: No se pudo conectar a {settings.SMTP_HOST}:{settings.SMTP_PORT} en 30 s.")
            logger.error(traceback.format_exc())
        except Exception as e:
            logger.error(f"ERROR INESPERADO: {type(e).__name__}: {e}")
            logger.error(traceback.format_exc())

        logger.info("=" * 60)
        return False
