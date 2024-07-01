from sqlalchemy import Column,Text,Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class QuestionsAndAnswers(Base):
    __tablename__ = 'QuestionsAndAnswers'
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, question:{self.question}, answer:{self.answer}"
