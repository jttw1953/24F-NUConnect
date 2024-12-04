from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import datetime, timedelta

# Create the Blueprint object for Analyst routes
analyst = Blueprint('analyst', __name__)

"""
GET METHODS
"""
# Get a count of new jobs, applications, discussions, and comments in the last day
@analyst.route('/DailySummary', methods=["GET"])
def get_summary():
    from datetime import datetime, timedelta
    end = datetime.utcnow()  
    start = end - timedelta(days=1)
    start_date = start.strftime('%Y-%m-%d %H:%M:%S')
    end_date = end.strftime('%Y-%m-%d %H:%M:%S')
    
    query = '''
        SELECT
            (SELECT COUNT(*) FROM Application WHERE dateSubmitted BETWEEN %s AND %s) AS apps_sent,
            (SELECT COUNT(*) FROM Job WHERE datePosted BETWEEN %s AND %s) AS jobs_posted,
            (SELECT COUNT(*) FROM ForumDiscussion WHERE createdAt BETWEEN %s AND %s) AS new_discussions,
            (SELECT COUNT(*) FROM Comment WHERE createdAt BETWEEN %s AND %s) AS new_comments;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query, (start_date, end_date, start_date, end_date, start_date, end_date, start_date, end_date))
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all forum discussion posts
@analyst.route('/ForumDiscussion', methods=["GET"])
def get_discussion():
    query = '''
        SELECT * 
        FROM ForumDiscussion
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all forum discussion with a certain tag
@analyst.route('/Tags', methods=["GET"])
def get_tags():
    tag = request.args.get('tag')

    query = 'SELECT * FROM ForumDiscussion'
    filters = []
    if tag:
        filters.append(f"tags = '{tag}'")

    if filters:
        query += ' WHERE ' + ' AND '.join(filters)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all comments
@analyst.route('/Comments', methods=["GET"])
def get_comments():
    query = '''
        SELECT * 
        FROM Comment
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@analyst.route('/Students', methods=["GET"])
def get_students():
    query = '''
        SELECT * 
        FROM Student
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all activity log of a certain type
@analyst.route('/ActivityLog', methods=["GET"])
def get_activity():
    activitytype  = request.args.get('type')
    query = 'SELECT * FROM ActivityLog'
    filters = []
    if activitytype:
        filters.append(f"activityType = '{activitytype}'")

    if filters:
        query += ' WHERE ' + ' AND '.join(filters)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all Jobs
@analyst.route('/Jobs', methods=["GET"])
def get_jobs():
    query = '''
        SELECT * 
        FROM Job
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all Applications
@analyst.route('/Apps', methods=["GET"])
def get_apps():
    query = '''
        SELECT * 
        FROM Application
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@analyst.route('/Employers', methods=["GET"])
def get_employers():
    query = '''
        SELECT * 
        FROM Company
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# return an analyst by userID
@analyst.route('/analysts/<int:user_id>', methods=['GET'])
def get_analyst_profile(user_id):
    query = """
        SELECT
            User.userID,
            User.firstName,
            User.lastName,
            User.email,
            User.phoneNum,
            User.registrationDate,
            'analyst' AS role
        FROM
            User
        WHERE
            User.role = 'analyst' AND User.userID = %s;
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    
    if result:
        return make_response(jsonify(result), 200)
    else:
        return make_response({"error": f"Analyst with User ID {user_id} not found."}, 404)
    

"""
POST and PUT routes
"""

# POST a new forum discussion
@analyst.route('/ForumDiscussion', methods=['POST'])
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

#Update a forum discussion
@analyst.route('/ForumDiscussion/<int:post_id>', methods=['PUT'])
def update_forum_post(post_id):
    data = request.json
    updates = []

    if 'content' in data:
        updates.append(f"content = '{data['content']}'")
    if 'tags' in data:
        updates.append(f"tags = '{data['tags']}'")

    if not updates:
        return make_response({"error": "No fields provided for update"}, 400)

    query = f'''
        UPDATE ForumDiscussion
        SET {', '.join(updates)}
        WHERE discussionID = {post_id};
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response({"message": f"Discussion {post_id} updated successfully"})
    response.status_code = 200
    return response