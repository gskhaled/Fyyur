# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions?page=<page number>'
GET '/categories/<category id>/questions'
POST '/questions'
POST '/quizzes'
DELETE '/questions'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a JSON of questions which are in the database
- Request Arguments: Page
- Returns: A JSON object with 4 keys: total_questions: the number of resulting questions from the query, questions: a list of question objects with question text, answer, id, category and difficulty, current_category: set to '' for now, categories: the available categories (same as GET /categories). 
{
    'total_questions': 1,
    'questions': [{ 'question':'Test question?', 'answer': 'Test answer', 'category': 1, 'difficulty': 1, 'id': 1}],
    'current_category': '',
    'categories': {'1' : "Science",
                    '2' : "Art",
                    '3' : "Geography",
                    '4' : "History",
                    '5' : "Entertainment",
                    '6' : "Sports"
    }
}

GET '/categories/<category id>/questions'
- Fetches a JSON of questions which are in the database with the given Category ID
- Request Arguments: Category ID
- Returns: A JSON object with 3 keys: total_questions  (the number of resulting questions from the query), questions (a list of question objects with question text, answer, id, category and difficulty), current_category (set to the category type).
{
    'total_questions': 1,
    'questions': [{ 'question':'Test question?', 'answer': 'Test answer', 'category': 1, 'difficulty': 1, 'id': 1}],
    'current_category': 'Science'
}


POST '/questions'
- Could search for a question or add a new question
- Request Arguments: None
- Returns: Could either return a JSON object of 2 keys (in case of adding a new question): success (if the new question was added successfully) and question (id of the question added) or a JSON object of 3 keys (in case of searching for a question): total_questions (the number of resulting questions from the query), questions (a list of question objects with question text, answer, id, category and difficulty), current_category (set to '' for now).
REQUEST BODY: 
{
    'searchTerm': 'term'
}
OR
{
    'question':'Test question?', 
    'answer': 'Test answer', 
    'category': 1, 
    'difficulty': 1
}
RESPONSE:
{
    'total_questions': 1,
    'questions': [{ 'question':'Test question?', 'answer': 'Test answer', 'category': 1, 'difficulty': 1, 'id': 1}],
    'current_category': ''
}
OR
{
    'success': True,
    'question': 1
}

POST '/quizzes'
- Searches for a question to ask in the quiz
- Request Arguments: None
- Returns:  a JSON object of a question (question text, answer, id, category and difficulty).
REQUEST BODY: 
{
    'quiz_category': { 'id':1, 'type':'Science'},
    'previous_questions': []
}
RESPONSE:
{
    'question':'Test question?', 
    'answer': 'Test answer', 
    'category': 1, 
    'difficulty': 1, 
    'id': 1
}

DELETE '/questions'
- Fetches a JSON of questions which are in the database
- Request Arguments: Question ID
- Returns: A JSON object with 2 keys: success and deleted (which is the ID of the deleted question).
{
    'success': True
    'deleted': 1
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```