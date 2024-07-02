# Home Assignment for Backend Developer

### Live Deploy (Frontend app in React):

https://chatgpt-5tqi.onrender.com/

### Swagger Docs (Server Documentation):

https://chatgpt-5tqi.onrender.com//api/docs

# Task Overview

This is a simple Flask server that exposes some endpoints with the ability to ask a question, get history of the asked questions and their answers, get specific question and answer that is stored in the database, delete specific question and answer that is stored in the database, delete ALL the questions and answers that are stored in the database.

## How it works

The server sends the question to an OpenAI API, receives the answer, and saves both the question and the answer in a PostgreSQL database.

## Docker and docker-compose

The server and the database is dockerized and run with Docker Compose.

## Testing

There are also testing using pytest.

## Database migrations

Alembic is used for database migrations.

## Technology stack

- **Docker**
  <img src="https://icon-icons.com/icons2/2699/PNG/512/docker_official_logo_icon_169250.png" width="124px" height="124px">
- **Docker**
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7swv72e-AJAfT3hZdULsmYXetYSldgE78ag&s" width="124px" height="124px">

- **React**
  <img src="https://upload.wikimedia.org/wikipedia/he/a/a7/React-icon.svg" width="124px" height="124px">

  - **Tailwindcss**
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_BuIzY141a5nIZoGEQkFYPN_f3bQddC4uu5ctRPO1Ftp6BNy_iV5foebwEIYesnZLA6c&usqp=CAU" width="60px" height="60px">

  - **Typescript**
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuiTDrB4jE3RaO72W0feOQP1XcZhjTrOBuYcqcXNSIQKeOx4iaA75cEZVN5BDrkQcLYK0&usqp=CAU" width="60px" height="60px">

  - **FastAPI**
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRubRv-E-PFnEuyYITdMYPqMXrBLOIKUTW8ug&s">

  - **React hook form**
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStBSZr9XstT3_uX0Mi4nBL88vUxZ2LTLu_6ikhMhZywt41ETXdZepvU12op0L33xJTrEM&usqp=CAU" width="220px" height="220px">

- **Zod**
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXt1ITFzxsJzjyjX9RnBco2jKyBcNv1UUnf8HojJSqcDchgcAL1x7DuSqdUje0oH7nLsA&usqp=CAU" width="220px" height="220px">

## Installation and Setup

<b>Clone the repository git clone https://github.com/roy845/insait_assignment.git</b>

Prepare .env file in the root folder directory with the following details:

DATABASE_PROD_URL=postgresql://postgres:admin@localhost:5432/prod_db
DATABASE_TEST_URL=postgresql://postgres:admin@localhost:5432/test_db
OPENAI_API_KEY= // your openai api-key
POSTGRES_PASSWORD=admin
POSTGRES_DB=QuestionsAndAnswers

<b>Install python virtual environment and dependencies and start the server</b>

1. Open a new terminal in VSCODE.
2. Create the virtual environment: python -m venv venv.
3. Activate the virtual environment: .\venv\Scripts\activate.
4. Install dependencies: pip install -r requirements.txt.
5. Run the server: python app.py.

<b>OR</b>

<b>Run in docker environment</b>

1. for the .env file put

   DATABASE_PROD_URL=postgresql://postgres:admin@db:5432/prod_db
   DATABASE_TEST_URL=DATABASE_TEST_URL=postgresql://postgres:admin@db:5432/test_db
   OPENAI_API_KEY= // your openai api-key
   POSTGRES_PASSWORD=admin
   POSTGRES_DB=QuestionsAndAnswers

2. run the command docker-compose up in the terminal console in VSCODE when you are in the project directory.

<b>OR</b>

<b>Pull the docker image iv'e created from docker hub</b>

1. Open a new terminal in VSCODE.
2. docker login -> type the username and password in the terminal.
3. docker pull royatali/chatgpt:latest.
4. run the image from docker desktop or using the command:

   docker run --name chatgpt_c -p 5000:5000 -d chatgpt using the terminal in VSCODE.

## Features

### Ask Question

The user can send his question to the api in the form of JSON payload and it will receive an answer using chatgpt open ai api
![alt text](image-1.png)

![alt text](image-2.png)

### Get all questions and answers

There is an option to get all the questions and answers the users asks
![alt text](image-3.png)

### Get specific question and answer

The user needs to provide specific question and answer id in order to retreive the required resource. providing id of question and answer that is not found will result in 404 - NOT_FOUND response as a result and a JSON that says:
{
"message": "Question and answer not found"
}

![alt text](image-4.png)

### Delete specific question and answer

The user needs to provide specific question and answer id in order to delete the required resource. providing id of question and answer that is not found will result in 404 - NOT_FOUND response as a result and a JSON that says:

![alt text](image-5.png)

### Delete ALL question and answer

There is an option to delete ALL the questions and answers the users asks
![alt text](image-6.png)
