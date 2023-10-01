from flask import jsonify, make_response
from my_app import app

# Custom Exception Handler
@app.errorhandler(404)
@app.errorhandler(400)
@app.errorhandler(500)
@app.errorhandler(401)
@app.errorhandler(403)
def handle_error(error):
    status_code = error.code
    response = {'error': str(status_code) + ' ' + error.name}
    if status_code == 404:
        response['message'] = '404 Not Found'
    elif status_code == 400:
        response['message'] = 'Bad Request'
    elif status_code == 500:
        response['message'] = 'Internal Server Error'
    elif status_code == 401:
        response['message'] = 'Unauthorized!'
    elif status_code == 403:
        response['message'] = 'Forbidden >:('

    return make_response(jsonify(response), status_code)