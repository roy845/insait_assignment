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
    def get_all_questions_and_answers():
        return QuestionsAndAnswers.get_all_questions_and_answers()

    @staticmethod
    def serialize_questions_and_answers(questions_and_answers):
        questions_and_answers_schema = QuestionsAndAnswersSchema(many=True)
        questions_and_answers_json = questions_and_answers_schema.dump(questions_and_answers)
        return questions_and_answers_json