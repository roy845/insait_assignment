from flask_restx import Namespace, Resource,fields
from flask import jsonify, request
from pydantic import ValidationError
from models.QuetionsAndAnswers import QuestionsAndAnswersSchema
from schemas.QuestionSchema import QuestionSchema
from http import HTTPStatus
from services.QuestionsAndAnswersService import QuestionsAndAnswersService


question_api = Namespace('question', description='Question')

ask_model = question_api.model('Ask', {
    'question': fields.String(required=True, description='The question to ask')
})


@question_api.route('/ask')
class Ask(Resource):
    @question_api.expect(ask_model)
    @question_api.doc(
        responses={HTTPStatus.CREATED: 'The answer to the question received as JSON payload and a message indicate that the Question and Answer created successfully',
                   HTTPStatus.BAD_REQUEST:"Error message about JSON payload validation",
                   HTTPStatus.INTERNAL_SERVER_ERROR:"Internal Server Error"})
    def post(self):
        try:
            data = request.get_json()
            try:  
                validated_data = QuestionSchema(**data)
            except ValidationError as e:
                return {'errors': e.errors()}, HTTPStatus.BAD_REQUEST
            
            created_text,answer,status = QuestionsAndAnswersService.save_question_and_answer(validated_data)

            return {"answer":answer,"message":created_text},status
    
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

@question_api.route('/')
class GetAllQuestionsAndAnswers(Resource):
    @question_api.doc(
        responses={HTTPStatus.OK: 'List of all questions and answers',HTTPStatus.INTERNAL_SERVER_ERROR:"Internal Server Error"})
    def get(self):
        try:
           questions_and_answers = QuestionsAndAnswersService.get_all_questions_and_answers()
           questions_and_answers_json = QuestionsAndAnswersService.serialize_questions_and_answers(questions_and_answers)
           return questions_and_answers_json, HTTPStatus.OK
    
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR