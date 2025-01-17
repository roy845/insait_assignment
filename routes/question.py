from flask_restx import Namespace, Resource,fields
from flask import request
from pydantic import ValidationError
from schemas.QuestionSchema import QuestionSchema
from http import HTTPStatus
from services.QuestionsAndAnswersService import QuestionsAndAnswersService


question_api = Namespace('question', description='Question')

ask_model = question_api.model('Ask', {
    'question': fields.String(required=True, description='The question to ask')
})



@question_api.route('/')
class GetAllQuestionsAndAnswers(Resource):
    @question_api.doc(
               params={
            'search': {
                'description': 'Search query for filtering questions and answers',
                'in': 'query',
                'type': 'string',
                'required': False
            }
        },
        responses={HTTPStatus.OK: 'List of all questions and answers',HTTPStatus.INTERNAL_SERVER_ERROR:"Internal Server Error"})
    def get(self):
        
           search = request.args.get('search')
           questions_and_answers = QuestionsAndAnswersService.get_all_questions_and_answers(search)
           return questions_and_answers, HTTPStatus.OK
    
        
    @question_api.doc(
        responses={
            HTTPStatus.NO_CONTENT: 'All questions and answers deleted successfully',
            HTTPStatus.INTERNAL_SERVER_ERROR: "Internal Server Error"
        }
    )
    def delete(self):
     
            QuestionsAndAnswersService.delete_all_questions_and_answers()
            return '', HTTPStatus.NO_CONTENT
       


@question_api.route('/<int:id>')
class GetQuestionAndAnswerById(Resource):
    @question_api.doc(
        params={'id': 'The ID of the question and answer'},
        responses={HTTPStatus.OK: 'The specific question and answer', 
                   HTTPStatus.NOT_FOUND: 'Question and answer not found', 
                   HTTPStatus.INTERNAL_SERVER_ERROR: "Internal Server Error"})
    def get(self, id):
       
            question_and_answer = QuestionsAndAnswersService.get_question_and_answer_by_id(id)
            if question_and_answer is None:
                return {'message': 'Question and answer not found'}, HTTPStatus.NOT_FOUND

            question_and_answer_json = QuestionsAndAnswersService.serialize_question_and_answer(question_and_answer)
            return question_and_answer_json, HTTPStatus.OK
      
        
    @question_api.doc(
    params={'id': 'The ID of the question and answer'},
        responses={HTTPStatus.NO_CONTENT: 'Question and answer deleted', 
                   HTTPStatus.NOT_FOUND: 'Question and answer not found', 
                   HTTPStatus.INTERNAL_SERVER_ERROR: "Internal Server Error"})
    def delete(self, id):
        
        deleted = QuestionsAndAnswersService.delete_question_and_answer(id)
        if not deleted:
            return {'message': 'Question and answer not found'}, HTTPStatus.NOT_FOUND

        return '', HTTPStatus.NO_CONTENT
       

@question_api.route('/ask')
class Ask(Resource):
    @question_api.expect(ask_model)
    @question_api.doc(
        responses={HTTPStatus.CREATED: 'The answer to the question received as JSON payload and a message indicate that the Question and Answer created successfully',
                   HTTPStatus.BAD_REQUEST:"Error message about JSON payload validation",
                   HTTPStatus.INTERNAL_SERVER_ERROR:"Internal Server Error"})
    def post(self):
        data = request.get_json()

        validated_data = QuestionSchema(**data) 

        created_text,answer,status = QuestionsAndAnswersService.save_question_and_answer(validated_data)
        
        return {"answer":answer,"message":created_text},status
    
      


