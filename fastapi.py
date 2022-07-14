from fastapi import FastAPI
from fastapi import WebSocket
from fastapi_socketio import SocketManager
import sqlalchemy
from sqlalchemy.orm import Session
from pydantic import BaseModel

import app
from app.models.user import Base
from app.db.database import SessionLocal, engine
app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
def index():
    return {"Hello everyone!"}

## User model
from sqlalchemy import Column , Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String)

    def __repr__(self):
        return f"id:{self.id}, username:{self.username}, " \
               f"name:{self.first_name}, surname:{self.last_name}"


## Database 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

## Login functionality
SECRET = 'your-secret-key'
from fastapi_login import LoginManager

manager = LoginManager(SECRET, token_url='/auth/token')

@manager.user_loader()
def load_user(email: str):  
    user = fake_db.get(email)
    return user

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  
    if not user:
        raise InvalidCredentialsException  
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

    
@app.get("/logout")
def logout(response : Response):
  response = RedirectResponse('*your login page*', status_code= 302)
  response.delete_cookie(key ='*your access token name*')
  return response