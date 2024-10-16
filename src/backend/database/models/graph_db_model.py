from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from backend.database.database_conn import Base
from backend.database.models.user_db_model import User

class Graph(Base):
    __tablename__ = 'graphs'

    graphId = Column(Integer, primary_key=True, index=True)
    userIdFK = Column(ForeignKey(User.userId), index=True)
    graphName = Column(String)
    fileName = Column(String)
    createDate = Column(DateTime)