from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import datetime, timedelta

# Create the Blueprint object for Analyst routes
analyst = Blueprint('analyst', __name__)

# Get a count of new jobs, applications, discussions, and comments in the last day
@analyst.route('/DailySummary/count', methods=["GET"])
def get_summary():
    end = datetime.utcnow()  
    start = end - timedelta(days=1)
    start_date = start.strftime('%Y-%m-%d %H:%M:%S')
    end_date = end.strftime('%Y-%m-%d %H:%M:%S')
    query = '''
        SELECT
        (SELECT COUNT(*) FROM Application WHERE datePosted BETWEEN '{start_date}' AND '{end_date}') AS apps_sent,
        (SELECT COUNT(*) FROM Job WHERE dateSubmitted BETWEEN '{start_date}' AND '{end_date}') AS jobs_posted,
        (SELECT COUNT(*) FROM ForumDiscussion WHERE createdAt BETWEEN '{start_date}' AND '{end_date}') AS new_discussions,
        (SELECT COUNT(*) FROM Comment WHERE createdAt BETWEEN '{start_date}' AND '{end_date}') AS new_comments);
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all forum discussion posts
@analyst.route('/ForumDiscussion', methods=["GET"])
def get_summary():
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
@analyst.route('/ForumDiscussion/{tags}', methods=["GET"])
def get_summary(tag):
    query = '''
        SELECT * 
        FROM ForumDiscussion
        WHERE tags = {tag}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all comments
@analyst.route('/Comments', methods=["GET"])
def get_summary():
    query = '''
        SELECT * 
        FROM Comments
        GROUP BY forumID
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all activity log of a certain type
@analyst.route('/ActivityLog/{activityType}', methods=["GET"])
def get_summary(activityType):
    query = '''
        SELECT * 
        FROM ActivityLog
        WHERE activityType = {activityType}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all Jobs
@analyst.route('/Jobs', methods=["GET"])
def get_summary():
    query = '''
        SELECT * 
        FROM Job
        GROUP BY companyID
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# Get all Applications
@analyst.route('/Apps', methods=["GET"])
def get_summary():
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
