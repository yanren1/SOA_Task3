from flask import request, jsonify, abort, url_for
from my_app import app, facultyData
from main import auth

# Get a list of all faculties
# Only admin users can view the list of all faculties.
@app.route('/faculties', methods=['GET'])
@auth.login_required(role='admin')
def get_faculties():
    return jsonify({'faculties': facultyData})

# Get details of a specific faculty
# Both admin and regular users can access, but admin users will see more details.
@app.route('/faculties/<string:faculty>', methods=['GET'])
@auth.login_required
def get_faculty(faculty):
    if faculty not in facultyData:
        abort(404)
    faculty_details = facultyData[faculty]
    if auth.current_user() in ["admin"]:
        # Add additional details for admin users
        faculty_details["extra_info"] = "Random Additional data for admin"
    return jsonify({'faculty': faculty_details, 'links': url_for('get_faculty', faculty=faculty, _external=True)})

# Get details of a faculty's courses
# Both admin and regular users can access, but admin users will see more details.
@app.route('/faculties/<string:faculty>/courses', methods=['GET'])
@auth.login_required
def get_faculty_courses(faculty):
    if faculty not in facultyData:
        abort(404)
    course_details = facultyData[faculty]['Courses']
    if auth.current_user() in ["admin"]:
        # Add additional details for admin users
        course_details["extra_info"] = "More Random Additional course data for admin"
    return jsonify({'courses': course_details, 'links': url_for('get_faculty_courses', faculty=faculty, _external=True)})

# Get students by faculty
# Only admin users can view the list of students by faculty.
@app.route('/faculties/<string:faculty>/students', methods=['GET'])
@auth.login_required(role='admin')
def get_faculty_students(faculty):
    for student_id in facultyData[faculty]['Students']:
        if 'Link' not in facultyData[faculty]['Students'][student_id]:
            facultyData[faculty]['Students'][student_id]['Link'] = url_for('get_student', student_id=student_id, _external=True)
    return jsonify({'Students': facultyData[faculty]['Students'], 'links': url_for('get_faculty_students', faculty=faculty, _external=True)})
