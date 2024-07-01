from http import HTTPStatus
from models.QuetionsAndAnswers import QuestionsAndAnswers, QuestionsAndAnswersSchema
from utils.initOpenAI import init_open_ai_client

client = init_open_ai_client()

class QuestionsAndAnswersService:
    @staticmethod
    def generate_answer(question: str) -> str:
       
        completion = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "user", "content": question}
            ]
        )
   
        answer = completion.choices[0].message.content
        return answer


    @staticmethod
    def save_question_and_answer(validated_data):
    
        answer = QuestionsAndAnswersService.generate_answer(validated_data.question)
        to_save = {"question":validated_data.question,"answer":answer}
        new_qa = QuestionsAndAnswers(**to_save)
        new_qa.save()

        return "Question and answer created successfully",answer,HTTPStatus.CREATED


    @staticmethod
    def get_all_questions_and_answers(search=None):
        return QuestionsAndAnswersService.serialize_questions_and_answers(
            QuestionsAndAnswers.get_all_questions_and_answers(search)
        )
    
    @staticmethod
    def get_question_and_answer_by_id(id:int):
        return QuestionsAndAnswers.get_question_and_answer_by_id(id)
    
    @staticmethod
    def delete_question_and_answer(id: int) -> bool:
        question_and_answer = QuestionsAndAnswers.get_question_and_answer_by_id(id)
        if question_and_answer:
            question_and_answer.delete()
            return True
        return False
    
    @staticmethod
    def delete_all_questions_and_answers():
        QuestionsAndAnswers.delete_all_questions_and_answers()

    @staticmethod
    def serialize_question_and_answer(question_and_answer):
        schema = QuestionsAndAnswersSchema()
        return schema.dump(question_and_answer)

    @staticmethod
    def serialize_questions_and_answers(questions_and_answers):
        questions_and_answers_schema = QuestionsAndAnswersSchema(many=True)
        questions_and_answers_json = questions_and_answers_schema.dump(questions_and_answers)
        return questions_and_answers_json