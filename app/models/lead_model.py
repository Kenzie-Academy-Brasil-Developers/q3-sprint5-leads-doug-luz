from email.policy import default
from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

@dataclass
class LeadModel(db.Model):
    # _id:int
    name:str
    email:str
    phone:str
    creation_date:str
    last_visit:str
    visits:int

    __tablename__ = 'leads'

    _id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    creation_date = Column(DateTime, default=datetime.now())
    last_visit = Column(DateTime, default=datetime.now())
    visits = Column(Integer, default=1)