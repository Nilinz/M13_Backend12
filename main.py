from pathlib import Path
import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from app.db import Base, engine

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


app = FastAPI()

# @app.post("/send-email")
# async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
#     message = MessageSchema(
#         subject="Fastapi mail module",
#         recipients=[body.email],
#         template_body={"fullname": "Billy Jones"},
#         subtype=MessageType.html
#     )

#     fm = FastMail(conf)

#     background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

#     return {"message": "email has been sent"}


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    uvicorn.run('main:app', port=8000, reload=True)