import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from config import settings

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
        if True : 
            try:
                # Crear mensaje
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
                msg['To'] = to
                
                # Agregar CC/BCC por defecto si no es empresa 90
                if company_id != 90:
                    default_cc = ['dalmaquinaria@ddg.com.mx', 'david@ddg.com.mx', 'ddgbecarioti@outlook.com']
                    default_bcc = ['operacionmbackup@gmail.com']
                    
                    cc = list(set((cc or []) + default_cc))
                    bcc = list(set((bcc or []) + default_bcc))
                
                if cc:
                    msg['Cc'] = ', '.join(cc)
                
                # Adjuntar contenido
                msg.attach(MIMEText(message, 'html' if html else 'plain', 'utf-8'))
                
                # Enviar
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    
                    recipients = [to] + (cc or []) + (bcc or [])
                    server.sendmail(settings.SMTP_FROM_EMAIL, recipients, msg.as_string())
                
                return True
                
            except Exception as e:
                print(f"[EMAIL ERROR] Error al enviar email: {str(e)}")
                return False
        return True  # Modo deshabilitado para envío de emails
