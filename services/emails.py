from pathlib import Path
import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from services.auth import auth_service

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=os.getenv('MAIL_PORT', default=465),
    MAIL_SERVER=os.getenv('MAIL_SERVER', default='smtp.meta.ua'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME', default='Example email'),
    MAIL_STARTTLS=os.getenv('MAIL_STARTTLS', default=False),
    MAIL_SSL_TLS=os.getenv('MAIL_SSL_TLS', default=True),
    USE_CREDENTIALS=os.getenv('USE_CREDENTIALS', default=True),
    VALIDATE_CERTS=os.getenv('VALIDATE_CERTS', default=True),
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

async def send_email(email: EmailStr, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)

print(f"Template Folder Path: {conf.TEMPLATE_FOLDER}")