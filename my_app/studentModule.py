from flask import request, jsonify, abort, url_for
from my_app import app, studentData, coursesData, facultyData
from main import auth


# Get a list of all students with optional filtering
@app.route('/students', methods=['GET'])
#Authentication for student list
@auth.login_required
def get_students():
    filtered_students = {}
    faculty_filter = request.args.get('faculty')

    for student_id, student_info in studentData.items():
        if faculty_filter and student_info['Faculty'] != faculty_filter:
            continue

        if 'Link' not in student_info:
            student_info['Link'] = url_for('get_student', student_id=student_id, _external=True)

        filtered_students[student_id] = student_info
    return jsonify({'students': filtered_students})


# Get details of a specific student

@app.route('/students/<int:student_id>', methods=['GET'])
#Authentication for student details
@auth.login_required
def get_student(student_id):
    if student_id not in studentData:
        abort(404)
    if 'Link' not in studentData[student_id]:
        studentData[student_id]['Link'] = url_for('get_student', student_id=student_id, _external=True)

    return jsonify(
        {'student': studentData[student_id], 'links': url_for('get_student', student_id=student_id, _external=True)})


@app.route('/students/<int:student_id>/faculty', methods=['GET'])
#Authentication for student faculty
@auth.login_required
def get_students_faculty(student_id):
    faculty = studentData[student_id]['Faculty']
    if student_id not in studentData:
        abort(404)

    return jsonify({'faculty': studentData[student_id]['Faculty'],
                    'links': url_for('get_faculty', faculty=faculty, _external=True)})


# Get details of a student's registered course
@app.route('/students/<int:student_id>/courses', methods=['GET'])
#Authentication for student course registered
@auth.login_required
def get_students_courses(student_id):
    if student_id not in studentData:
        abort(404)
    return jsonify({'courses': studentData[student_id]["Course Registered"],
                    'links': url_for('get_students_courses', student_id=student_id, _external=True)})


# Add a new student
@app.route('/students', methods=['POST'])
#Admins can add student
@auth.login_required(role='admin')
def add_student():
    checkList0 = ['Name', 'Faculty', ]
    checkList1 = ['Age', 'Country', ]
    data = request.get_json()

    # necessary data
    for e in checkList0:
        if e not in data:
            abort(400)

    # additional data
    for e in checkList1:
        if e not in data:
            data[e] = 'Unknown'

    new_id = max(studentData.keys()) + 1
    studentData[new_id] = data
    return jsonify({'message': 'Student added', 'student_id': new_id}), 201


# Update a student's information
@app.route('/students/<int:student_id>', methods=['PUT'])
#Admins can update a student
@auth.login_required(role='admin')
def update_student(student_id):
    if student_id not in studentData:
        abort(404)
    data = request.get_json()
    if 'Name' in data:
        studentData[student_id]['Name'] = data['Name']
    if 'Age' in data:
        studentData[student_id]['Age'] = data['Age']
    if 'Faculty' in data:
        if data['Faculty'] in facultyData.keys():
            studentData[student_id]['Faculty'] = data['Faculty']
    if 'Country' in data:
        studentData[student_id]['Country'] = data['Country']
    if 'Course Registered' in data:
        for c in list(data['Course Registered'].keys()):
            if c in studentData['Course Registered']:
                continue
            if c in coursesData:
                studentData[student_id]['Course Registered'][c] = {'Course Name': coursesData[c]['Course Name']}

    return jsonify({'message': 'Student updated', 'student_id': student_id})


# Delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
#Admins can delete student
@auth.login_required(role='admin')
def delete_student(student_id):
    if student_id not in studentData:
        abort(404)
    del studentData[student_id]
    return jsonify({'message': 'Student deleted'})
