import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample
    route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, PATCH')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def categories():
        categories = Category.query.all()
        dictionary = {c.id: c.type for c in categories}
        return jsonify({
            'categories': dictionary
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = Question.query.all()
            categories = Category.query.all()
            formattedCategories = [c.type for c in categories]
            formattedQuestions = [question.format() for question in questions]
            return jsonify({
                'total_questions': len(questions),
                'questions': formattedQuestions[start:end],
                'current_category': '',
                'categories': formattedCategories
            })
        except Exception:
            abort(404)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        questionToDelete = Question.query.get(question_id)
        try:
            questionToDelete.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            abort(404)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.
    '''
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions', methods=['POST'])
    def questions():
        body = request.get_json()
        searchTerm = body.get('searchTerm', None)
        if(searchTerm is not None):
            searchResults = Question.query.filter(func.lower(
                Question.question).contains(func.lower(searchTerm))).all()
            formattedQuestions = [question.format()
                                  for question in searchResults]
            return jsonify({
                'questions': formattedQuestions,
                'total_questions': len(formattedQuestions),
                'current_category': ''
            })
        questionText = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        if(questionText is None or answer is None):
            abort(400)
        try:
            question = Question(
                question=questionText, answer=answer, category=category,
                difficulty=difficulty)
            question.insert()
            return jsonify({
                'success': True,
                'question': question.id
            })
        except Exception:
            abort(422)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_by_category(category_id):
        category_id = str(int(category_id) + 1)
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            currentCategory = Category.query.filter(
                Category.id == category_id).one_or_none()
            formattedQuestions = [question.format() for question in questions]
            return jsonify({
                'total_questions': len(questions),
                'questions': formattedQuestions[start:end],
                'current_category': currentCategory.type
            })
        except Exception:
            abort(400)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()
        previousQuestions = body.get('previous_questions', None)
        quizCategory = body.get('quiz_category', None)
        if(quizCategory is None):
            abort(400)

        if(int(quizCategory['id']) == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == quizCategory['id']).all()

        formattedQuestions = [question.format() for question in questions]
        if(len(formattedQuestions) <= len(previousQuestions)):
            return jsonify({
                'question': None
            })

        randomIndex = random.randint(0, len(formattedQuestions) - 1)
        while(formattedQuestions[randomIndex]['question']
              in previousQuestions):
            randomIndex = random.randint(0, len(formattedQuestions) - 1)
        return jsonify({
            'question': formattedQuestions[randomIndex]
        })

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'error': 400,
            'message': 'bad request'
        }), 400

    return app
