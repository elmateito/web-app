from sqlalchemy import Column, Integer, String

from backend.database.database_conn import Base

class UserDB(Base):
    __tablename__ = 'users'
    
    userId = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    userEmail = Column(String)
    userPassword = Column(String)
    userRole = Column(String, default='user')