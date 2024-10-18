from sqlalchemy import Column, Integer, String

from backend.database.database_conn import Base

class Users(Base):
    __tablename__ = 'users'
    
    userId = Column(Integer, primary_key=True, index=True)
    userName = Column(String(32), index=True)
    userEmail = Column(String(64))
    userPassword = Column(String(255), index=True)
    userRole = Column(String(16), default='user')