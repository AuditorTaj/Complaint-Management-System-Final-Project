import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .init import init_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from pydantic import BaseModel
from .database import engine, get_db
from app.models import User, Complaint
from app.auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from app.kafka_producer import send_complaint_message

Base = declarative_base()

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str

class ComplaintCreate(BaseModel):
    title: str
    description: str

class Complaint(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).filter(User.username == user.username))
    if db_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/complaints/", response_model=Complaint)
async def create_complaint(complaint: ComplaintCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_complaint = Complaint(**complaint.dict(), owner_id=current_user.id)
    db.add(db_complaint)
    await db.commit()
    await db.refresh(db_complaint)
    send_complaint_message(db_complaint.id, db_complaint.title, db_complaint.description)
    return db_complaint
