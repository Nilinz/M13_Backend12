from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from . import models, schemas, db
from .db import get_db
from routes import auth

app = FastAPI()
security = HTTPBearer()

app.include_router(auth.router)
# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/contacts/", response_model=schemas.Contact, status_code=status.HTTP_201_CREATED)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get("/contacts/", response_model=schemas.ContactResponse)
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).offset(skip).limit(limit).all()
    return {"contacts": contacts}

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for var, value in vars(contact).items():
        setattr(db_contact, var, value) if value else None
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact

@app.get("/contacts/search/", response_model=List[schemas.Contact])
def search_contacts(query: str, db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).filter(
        (models.Contact.first_name.ilike(f"%{query}%")) |
        (models.Contact.last_name.ilike(f"%{query}%")) |
        (models.Contact.email.ilike(f"%{query}%"))
    ).all()
    return contacts

@app.get("/contacts/birthday/", response_model=List[schemas.Contact])
def upcoming_birthdays(days: int = 7, db: Session = Depends(get_db)):
    today = db.query(db.func.current_date()).scalar()
    end_date = today + timedelta(days=days)
    contacts = db.query(models.Contact).filter(
        (db.func.extract('month', models.Contact.birthday) == db.func.extract('month', today)) &
        (db.func.extract('day', models.Contact.birthday) <= db.func.extract('day', end_date))
    ).all()
    return contacts