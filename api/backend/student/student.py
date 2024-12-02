from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

student = Blueprint('student', __name__)

# 1. GET all forum discussions filtered by tags
@student.route('/ForumDiscussion', methods=['GET'])
def get_forum_discussions():
    tags = request.args.get('tags')
    query = "SELECT * FROM ForumDiscussion"
    if tags:
        query += f" WHERE tags LIKE '%{tags}%'"
    query += " ORDER BY createdAt DESC"

    cursor = db.get_db().cursor()
    cursor.execute(query)
    discussions = cursor.fetchall()

    response = make_response(jsonify(discussions))
    response.status_code = 200
    return response

# 2. POST a new forum discussion
@student.route('/ForumDiscussion', methods=['POST'])
def post_forum_discussion():
    data = request.json
    query = f'''
        INSERT INTO ForumDiscussion (createdBy, content, title, tags)
        VALUES ('{data["createdBy"]}', '{data["content"]}', '{data["title"]}', '{data["tags"]}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response({"message": "Discussion created successfully"})
    response.status_code = 201
    return response

# 3. GET personalized job recommendations for a student
@student.route('/JobRecommendation/<int:student_id>', methods=['GET'])
def get_job_recommendations(student_id):
    query = f'''
        SELECT j.jobID, j.title, j.description
        FROM JobRecommendation jr
        JOIN Job j ON jr.jobID = j.jobID
        WHERE jr.studentID = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    jobs = cursor.fetchall()

    response = make_response(jsonify(jobs))
    response.status_code = 200
    return response

# 4. GET application statuses for a student
@student.route('/Application/<int:student_id>', methods=['GET'])
def get_application_status(student_id):
    query = f'''
        SELECT a.appID, a.jobID, a.status, j.title
        FROM Application a
        JOIN Job j ON a.jobID = j.jobID
        WHERE a.studentID = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    applications = cursor.fetchall()

    response = make_response(jsonify(applications))
    response.status_code = 200
    return response

# 5. GET jobs filtered by criteria
@student.route('/Job', methods=['GET'])
def get_jobs():
    major = request.args.get('major')
    skills = request.args.get('skills')  # Expected as comma-separated values
    company = request.args.get('company')

    # Base query
    query = """
        SELECT DISTINCT j.jobID, j.title, j.description 
        FROM Job j
    """
    joins = []
    filters = []
    params = []

    # Add joins and filters based on provided query parameters
    if skills:
        joins.append("JOIN JobSkill js ON j.jobID = js.jobID")
        joins.append("JOIN Skill sk ON js.skillID = sk.skillID")
        skill_list = skills.split(",")
        placeholders = ', '.join(['%s'] * len(skill_list))
        filters.append(f"sk.name IN ({placeholders})")
        params.extend(skill_list)

    if major:
        filters.append("j.major = %s")
        params.append(major)

    if company:
        filters.append("j.companyID = %s")
        params.append(company)

    # Add JOINs and WHERE clause if needed
    if joins:
        query += " " + " ".join(joins)
    if filters:
        query += " WHERE " + " AND ".join(filters)

    cursor = db.get_db().cursor()

    # Execute the query with parameters
    cursor.execute(query, params)
    jobs = cursor.fetchall()

    # Format response
    job_list = [
        {
            "jobID": job[0],
            "title": job[1],
            "description": job[2]
        }
        for job in jobs
    ]

    response = make_response(jsonify(job_list))
    response.status_code = 200
    return response

# 6. POST a message to an employer
@student.route('/Message', methods=['POST'])
def post_message():
    data = request.json
    query = f'''
        INSERT INTO Message (senderID, receiverID, content)
        VALUES ('{data["senderID"]}', '{data["receiverID"]}', '{data["content"]}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response({"message": "Message sent successfully"})
    response.status_code = 201
    return response