from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS, 
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS, 
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=False
)

async def send_email(to_email: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)