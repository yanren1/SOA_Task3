from flask import request, jsonify, abort, url_for
from my_app import app, studentData, coursesData, facultyData


# Get a list of all students
@app.route('/students', methods=['GET'])
def get_students():
    for student_id in studentData:
        if 'Link' not in studentData[student_id]:
            studentData[student_id]['Link'] = url_for('get_student', student_id=student_id, _external=True)

    return jsonify({'students': studentData})


# Get details of a specific student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    if student_id not in studentData:
        abort(404)
    if 'Link' not in studentData[student_id]:
        studentData[student_id]['Link'] = url_for('get_student', student_id=student_id, _external=True)

    return jsonify(
        {'student': studentData[student_id], 'links': url_for('get_student', student_id=student_id, _external=True)})


@app.route('/students/<int:student_id>/faculty', methods=['GET'])
def get_students_faculty(student_id):
    faculty = studentData[student_id]['Faculty']
    if student_id not in studentData:
        abort(404)

    return jsonify({'faculty': studentData[student_id]['Faculty'],
                    'links': url_for('get_faculty', faculty=faculty, _external=True)})


# Get details of a student's registered course
@app.route('/students/<int:student_id>/courses', methods=['GET'])
def get_students_courses(student_id):
    if student_id not in studentData:
        abort(404)
    return jsonify({'courses': studentData[student_id]["Course Registered"],
                    'links': url_for('get_students_courses', student_id=student_id, _external=True)})


# Add a new student
@app.route('/students', methods=['POST'])
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
def delete_student(student_id):
    if student_id not in studentData:
        abort(404)
    del studentData[student_id]
    return jsonify({'message': 'Student deleted'})
