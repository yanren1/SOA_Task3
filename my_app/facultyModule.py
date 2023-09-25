from flask import request, jsonify, abort, url_for
from my_app import app, facultyData


# Get a list of all faculties
@app.route('/faculties', methods=['GET'])
def get_faculties():
    return jsonify({'faculties': facultyData})


# Get details of a specific student
@app.route('/faculties/<string:faculty>', methods=['GET'])
def get_faculty(faculty):
    if faculty not in facultyData:
        abort(404)
    return jsonify({'faculty': facultyData[faculty], 'links': url_for('get_faculty',
                                                                      faculty=faculty, _external=True)})


# Get details of a student's registered course
@app.route('/faculties/<string:faculty>/courses', methods=['GET'])
def get_faculty_courses(faculty):
    if faculty not in facultyData:
        abort(404)
    return jsonify({'courses': facultyData[faculty]['Courses'], 'links': url_for('get_faculty_courses',
                                                                                 faculty=faculty, _external=True)})


# Get students by faculty
@app.route('/faculties/<string:faculty>/students', methods=['GET'])
def get_faculty_students(faculty):
    return jsonify({'Students': facultyData[faculty]['Students'], 'links': url_for('get_faculty_students',
                                                                                   faculty=faculty, _external=True)})
