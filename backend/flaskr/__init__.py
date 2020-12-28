# Standard library imports
import json
from random import choice

# Third party imports
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

# Local application imports
from flaskr.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    '''
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        # response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories_query = Category.query.order_by(Category.type).all()

        if len(categories_query) == 0:
            return abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories_query}
        }), 200

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for
    three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        page_num = request.args.get('page', 1, type=int)
        start = (page_num-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions_query = Question.query.order_by(Question.id).all()
        total_questions = len(questions_query)
        questions = [question.format() for question in questions_query][start:end]
        categories_query = Category.query.order_by(Category.type).all()
        categories = {category.id: category.type for category in categories_query}

        if len(questions) == 0:
            return abort(404)

        return jsonify({
            'questions': questions,
            'total_questions': total_questions,
            'categories': categories,
            'current_category': None,
            'success': True
        }), 200

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get(id)
        if question:
            question.delete()
        else:
            return abort(404)

        return jsonify({
            'success': True,
            'deleted': id
        }), 200

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, the form will clear
    and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = json.loads(request.data)
        question = data.get('question')
        answer = data.get('answer')
        difficulty = data.get('difficulty')
        category = data.get('category')

        question_exist_query = Question.query.filter(Question.question.ilike(question)).first()
        if question_exist_query:
            return abort(422)

        question_obj = Question(
            question=question,
            answer=answer,
            category=category,
            difficulty=difficulty
        )
        question_obj.insert()

        return jsonify({
            'success': True,
            'created': question_obj.id
        }), 201

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = json.loads(request.data)
        search_term = data.get('searchTerm', '')
        questions_query = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        if len(questions_query) == 0:
            return abort(404)

        questions = [question.format() for question in questions_query]

        return jsonify({
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': None,
            'success': True
        }), 200

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        questions_query = Question.query.filter(Question.category == id).all()
        questions = [question.format() for question in questions_query]

        if len(questions) == 0:
            return abort(404)

        return jsonify({
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': id,
            'success': True
        }), 200

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
    def get_quiz_qustion():
        try:
            data = json.loads(request.data)
            previous_questions = data.get('previous_questions', [])
            category_id = data.get('quiz_category')['id']

            questions = None
            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.category == category_id).filter(Question.id.notin_(previous_questions)).all()

            question = None
            if len(questions) > 0:
                question = choice(questions)
                question = question.format()

            return jsonify({
                'question': question,
                'success': True
            }), 200
        except Exception as e:
            print(e)
            return abort(422)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(err):
        return jsonify({
            'success': False,
            'code': 400,
            'msg': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({
            'success': False,
            'code': 404,
            'msg': 'not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(err):
        return jsonify({
            'success': False,
            'code': 422,
            'msg': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_err(err):
        return jsonify({
            'success': False,
            'code': 500,
            'msg': 'internal server error'
        }), 500

    return app
