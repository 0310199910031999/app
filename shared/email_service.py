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
        """
        Envía un email usando SMTP
        
        Args:
            to: Email destinatario
            subject: Asunto
            message: Contenido del mensaje (HTML o texto)
            company_id: ID de empresa (si es 90, no agrega CC/BCC por defecto)
            cc: Lista de emails en copia
            bcc: Lista de emails en copia oculta
            html: Si el mensaje es HTML
            
        Returns:
            True si se envió exitosamente, False en caso contrario
        """
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
    
    @staticmethod
    def send_document_signed_notification(
        to: str,
        document_id: str,
        document_type: str,
        company_id: int,
        client_name: str = "Cliente",
        signed_date: str = "N/A"
    ) -> bool:
        """
        Notificación cuando se firma un documento
        
        Args:
            to: Email destinatario
            document_id: ID del documento
            document_type: Tipo de documento (FOSP01, FOOS01, etc)
            company_id: ID de empresa
            client_name: Nombre del cliente
            signed_date: Fecha de firma
            
        Returns:
            True si se envió exitosamente
        """
        subject = f"Documento {document_type} #{document_id} Firmado"
        
        message = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0066cc;">Documento Firmado</h2>
                <p>El siguiente documento ha sido firmado:</p>
                <div style="background-color: #f4f4f4; padding: 15px; margin: 20px 0;">
                    <p><strong>Tipo:</strong> {document_type}</p>
                    <p><strong>Folio:</strong> {document_id}</p>
                    <p><strong>Cliente:</strong> {client_name}</p>
                    <p><strong>Fecha de firma:</strong> {signed_date}</p>
                </div>
                <p style="color: #666; font-size: 12px;">
                    Este es un correo automático, por favor no responder.
                </p>
            </div>
        </body>
        </html>
        """
        
        return EmailService.send_email(to, subject, message, company_id)
