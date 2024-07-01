from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from database import db

class QuestionsAndAnswers(db.Model):
    __tablename__ = 'QuestionsAndAnswers'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def save(self)->None:
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def save_all(cls, instances) -> None:
        db.session.add_all(instances)
        db.session.commit()
    
    @classmethod
    def get_all_questions_and_answers(cls):
        return cls.query.all()
    
class QuestionsAndAnswersSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = QuestionsAndAnswers
         load_instance = True
         sqla_session = db.session
     