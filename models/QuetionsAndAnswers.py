from database import db
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class QuestionsAndAnswers(db.Model):
    __tablename__ = 'QuestionsAndAnswers'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def save(self)->None:
        db.session.add(self)
        db.session.commit()
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def save_all(cls, instances) -> None:
        db.session.add_all(instances)
        db.session.commit()
    
    @classmethod
    def get_all_questions_and_answers(cls, search=None):
        if search:
            return cls.query.filter(cls.question.like(f'%{search}%')).all()
        return cls.query.all()
    
    @classmethod
    def get_question_and_answer_by_id(cls,id:int):
        return cls.query.get(id)
    
    @classmethod
    def delete_all_questions_and_answers(cls):
        cls.query.delete()
        db.session.commit()
    
class QuestionsAndAnswersSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = QuestionsAndAnswers
         load_instance = True
         sqla_session = db.session
     