from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import null
from .database import Base

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
