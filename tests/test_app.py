import json
from http import HTTPStatus
from models.QuetionsAndAnswers import QuestionsAndAnswers
from unittest.mock import patch
from services.QuestionsAndAnswersService import QuestionsAndAnswersService


def test_ask_endpoint_valid_question(client,base_url):
    question = {"question": "What is the capital of France?"}
    response = client.post(f'{base_url}/ask', data=json.dumps(question), content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert 'answer' in data
    assert 'message' in data

def test_ask_endpoint_missing_question(client,base_url):
    question = {}
    response = client.post(f'{base_url}/ask', data=json.dumps(question), content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_ask_endpoint_invalid_data_type(client, base_url):
    question = {"question": 12345}
    response = client.post(f'{base_url}/ask', data=json.dumps(question), content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
  

def test_ask_endpoint_no_question_key(client, base_url):
    payload = {"not_a_question": "This is not a question"}
    response = client.post(f'{base_url}/ask', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_ask_endpoint_additional_fields(client, base_url):
    payload = {"question": "What is the capital of France?", "extra_field": "extra_value"}
    response = client.post(f'{base_url}/ask', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_database_schema(app):
    with app.app_context():
        columns = [column.name for column in QuestionsAndAnswers.__table__.columns]
        assert 'id' in columns
        assert 'question' in columns
        assert 'answer' in columns

@patch('database.db.session')
def test_missing_database_connection(mock_db_session,client, base_url):
    mock_db_session.add.side_effect = Exception("Database connection failed")
    question = {"question": "What is the capital of France?"}
    response = client.post(f'{base_url}/ask', data=json.dumps(question), content_type='application/json')
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

def test_save_question_and_answer(app):
    with app.app_context():
        qa = QuestionsAndAnswers(question="What is the capital of France?", answer="The capital of France is Paris.")
        qa.save()
        result = QuestionsAndAnswers.query.first()
        assert result.question == "What is the capital of France?"
        assert result.answer == "The capital of France is Paris."

def test_retrieve_questions_and_answers(app):
    with app.app_context():
        qa1 = QuestionsAndAnswers(question="What is the capital of France?", answer="The capital of France is Paris.")
        qa2 = QuestionsAndAnswers(question="What is 2+2?", answer="2 + 2 equals 4.")
        QuestionsAndAnswers.save_all([qa1, qa2])
        results = QuestionsAndAnswers.query.all()
        assert len(results) == 2
        assert results[0].question == "What is the capital of France?"
        assert results[1].question == "What is 2+2?"
        assert results[0].answer == "The capital of France is Paris."
        assert results[1].answer == "2 + 2 equals 4."

def test_save_question_and_answer(app):
    with app.app_context():
        qa = QuestionsAndAnswers(question="What is the capital of France?", answer="The capital of France is Paris.")
        qa.save()
        result = QuestionsAndAnswers.query.filter_by(question="What is the capital of France?").first()
        assert result is not None
        assert result.question == "What is the capital of France?"
        assert result.answer == "The capital of France is Paris."

def test_save_question_and_answer_2(app):
    with app.app_context():
        qa = QuestionsAndAnswers(question="What is 2+2?", answer="2 + 2 equals 4.")
        qa.save()
        result = QuestionsAndAnswers.query.filter_by(question="What is 2+2?").first()
        assert result is not None
        assert result.question == "What is 2+2?"
        assert result.answer == "2 + 2 equals 4."

def test_serialize_questions_and_answers(app):
    with app.app_context():
        qa1 = QuestionsAndAnswers(question="What is the capital of France?", answer="Paris")
        qa2 = QuestionsAndAnswers(question="What is 2+2?", answer="4")
        QuestionsAndAnswers.save_all([qa1, qa2])
    
    questions_and_answers = QuestionsAndAnswersService.get_all_questions_and_answers()
    questions_and_answers_json = QuestionsAndAnswersService.serialize_questions_and_answers(questions_and_answers)

    assert len(questions_and_answers_json) == 2
    assert questions_and_answers_json[0]['question'] == "What is the capital of France?"
    assert questions_and_answers_json[0]['answer'] == "Paris"
    assert questions_and_answers_json[1]['question'] == "What is 2+2?"
    assert questions_and_answers_json[1]['answer'] == "4"

def test_get_all_questions_and_answers(app, client):
    with app.app_context():
        qa1 = QuestionsAndAnswers(question="What is the capital of France?", answer="Paris")
        qa2 = QuestionsAndAnswers(question="What is 2+2?", answer="4")
        QuestionsAndAnswers.save_all([qa1, qa2])

    response = client.get("http://localhost:5000/api/question/")   
      
    response_data = response.json
    assert response.status_code == HTTPStatus.OK
    assert response_data is not None, "Response data is None"
    assert len(response_data) == 2
    assert response_data[0]['question'] == "What is the capital of France?"
    assert response_data[0]['answer'] == "Paris"
    assert response_data[1]['question'] == "What is 2+2?"
    assert response_data[1]['answer'] == "4"
   
def test_health_endpoint(client):
    response = client.get('http://localhost:5000/api/health/')
    assert response.status_code == HTTPStatus.OK, f"Expected status code 200, got {response.status_code}"
    assert response.json == {"ok": True}, f"Expected JSON response {{'ok': True}}, got {response.json}"