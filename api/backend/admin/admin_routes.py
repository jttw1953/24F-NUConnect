########################################################
# Admin blueprint of endpoints
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
admin = Blueprint('admin', __name__)

#------------------------------------------------------------
# Get all system alerts
@admin.route('/alerts', methods=['GET'])
def get_system_alerts():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT alertID, description, timestamp, status
        FROM SystemAlert
    ''')
    alerts = cursor.fetchall()
    the_response = make_response(jsonify(alerts))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Post a new system alert
@admin.route('/alerts', methods=['POST'])
def create_system_alert():
    alert_data = request.json
    description = alert_data['description']
    status = alert_data['status']

    query = '''
        INSERT INTO SystemAlert (description, status)
        VALUES (%s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (description, status))
    db.get_db().commit()

    return make_response("System alert created successfully", 201)

#------------------------------------------------------------
# Update a system alert by ID
@admin.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_system_alert(alert_id):
    alert_data = request.json
    status = alert_data.get('status')
    description = alert_data.get('description')

    updates = []
    if status:
        updates.append(f"status = %s")
    if description:
        updates.append(f"description = %s")
    
    if not updates:
        return make_response("No updates provided", 400)

    query = f'''
        UPDATE SystemAlert
        SET {', '.join(updates)}
        WHERE alertID = %s
    '''
    params = [value for value in (status, description) if value]
    params.append(alert_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()

    return make_response(f"System alert {alert_id} updated successfully", 200)

#------------------------------------------------------------
# GET all maintenance scheduless
@admin.route('/maintenance', methods=['GET'])
def get_maintenance_schedules():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT 
            m.maintenanceID, 
            m.description, 
            m.startTime, 
            m.endTime, 
            u.username AS performedBy
        FROM Maintenance m
        JOIN Admin a ON m.performedBy = a.adminID
        JOIN User u ON a.userID = u.userID
    ''')
    schedules = cursor.fetchall()
    the_response = make_response(jsonify(schedules))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# DELETE a maintenance schedule by ID
@admin.route('/maintenance/<int:maintenance_id>', methods=['DELETE'])
def delete_maintenance_schedule(maintenance_id):
    query = '''
        DELETE FROM Maintenance
        WHERE maintenanceID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (maintenance_id,))
    db.get_db().commit()

    return make_response(f"Deleted maintenance schedule {maintenance_id}", 200)

#------------------------------------------------------------
# Get all security logs
@admin.route('/securityLogs', methods=['GET'])
def get_security_logs():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT logID, actionType, timestamp, status
        FROM SecurityLog
    ''')
    logs = cursor.fetchall()
    the_response = make_response(jsonify(logs))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get performance metrics
@admin.route('/performanceMetric', methods=['GET'])
def get_performance_metrics():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT 
            pm.metricID, 
            pm.accessedBy, 
            u.username, 
            pm.serverTime, 
            pm.responseTime, 
            pm.memoryUsage, 
            pm.cpuUsage
        FROM PerformanceMetrics pm
        LEFT JOIN User u ON pm.accessedBy = u.userID
    ''')
    metrics = cursor.fetchall()
    the_response = make_response(jsonify(metrics))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# POST a new maintenance schedule
@admin.route('/maintenance', methods=['POST'])
def create_maintenance_schedule():
    maintenance_data = request.json
    current_app.logger.info(maintenance_data)

    description = maintenance_data['description']
    start_time = maintenance_data['startTime']
    end_time = maintenance_data['endTime']
    performed_by = maintenance_data['performedBy']

    query = '''
        INSERT INTO Maintenance (description, startTime, endTime, performedBy)
        VALUES (%s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (description, start_time, end_time, performed_by))
    db.get_db().commit()

    response = make_response("Maintenance schedule created successfully")
    response.status_code = 201
    return response

#------------------------------------------------------------
# POST flagged content
@admin.route('/contentFlag', methods=['POST'])
def create_flagged_content():
    flagged_data = request.json
    current_app.logger.info(flagged_data)

    reason = flagged_data['reason']
    status = flagged_data['status']

    query = '''
        INSERT INTO ContentFlag (reason, status)
        VALUES (%s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (reason, status))
    db.get_db().commit()

    response = make_response("Flagged content created successfully")
    response.status_code = 201
    return response

#------------------------------------------------------------
# PUT to update a maintenance schedule
@admin.route('/maintenance/<int:maintenance_id>', methods=['PUT'])
def update_maintenance_schedule(maintenance_id):
    maintenance_data = request.json
    current_app.logger.info(maintenance_data)

    description = maintenance_data.get('description')
    start_time = maintenance_data.get('startTime')
    end_time = maintenance_data.get('endTime')
    performed_by = maintenance_data.get('performedBy')

    updates = []
    if description:
        updates.append("description = %s")
    if start_time:
        updates.append("startTime = %s")
    if end_time:
        updates.append("endTime = %s")
    if performed_by:
        updates.append("performedBy = %s")

    if not updates:
        response = make_response("No fields provided for update")
        response.status_code = 400
        return response

    query = f'''
        UPDATE Maintenance
        SET {', '.join(updates)}
        WHERE maintenanceID = %s
    '''
    params = [value for value in (description, start_time, end_time, performed_by) if value]
    params.append(maintenance_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()

    response = make_response(f"Maintenance schedule {maintenance_id} updated successfully")
    response.status_code = 200
    return response

#------------------------------------------------------------
# GET all flags
@admin.route('/flags', methods=['GET'])
def get_all_content_flags():
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT
                cf.flagID,
                cf.contentID,
                cf.timestamp,
                cf.reason,
                cf.status,
                CASE
                    WHEN c.content IS NOT NULL THEN c.content
                    WHEN fd.title IS NOT NULL THEN fd.title
                    ELSE 'Unknown Content'
                END AS flaggedContent
            FROM ContentFlag cf
            LEFT JOIN Comment c ON cf.contentID = c.commentID
            LEFT JOIN ForumDiscussion fd ON cf.contentID = fd.discussionID
        '''
        cursor.execute(query)
        flags = cursor.fetchall()

        response = make_response(jsonify(flags))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error fetching content flags: {e}")
        return make_response("Failed to fetch content flags", 500)
#------------------------------------------------------------
# Post to add a flag 
@admin.route('/flags', methods=['POST'])
def create_content_flag():
    """
    POST route to create a new content flag.
    """
    try:
        # Get the JSON data from the request
        flag_data = request.json
        content_id = flag_data.get('contentID')
        reason = flag_data.get('reason')
        status = flag_data.get('status')

        # Validate the required fields
        if not content_id or not reason or not status:
            return make_response("Missing required fields: contentID, reason, or status", 400)

        # Query to insert the new content flag into the database
        query = '''
            INSERT INTO ContentFlag (contentID, timestamp, status, reason)
            VALUES (%s, NOW(), %s, %s)
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (content_id, reason, status))
        db.get_db().commit()

        return make_response(f"Content flag created successfully for content ID {content_id}", 201)

    except Exception as e:
        # Log and return the error message
        return make_response(f"Error creating content flag: {str(e)}", 500)

#------------------------------------------------------------
# PUT to update a flag status
@admin.route('/flags/<int:flag_id>', methods=['PUT'])
def update_flag_status(flag_id):
    flag_data = request.json
    new_status = flag_data.get('status')

    if not new_status:
        return make_response("Status is required", 400)

    # Query to update the flag's status
    query = '''
        UPDATE ContentFlag
        SET status = %s
        WHERE flagID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (new_status, flag_id))
    db.get_db().commit()

    return make_response(f"Flag {flag_id} status updated to {new_status}", 200)

#------------------------------------------------------------
# DELETE a flag
@admin.route('/flags/<int:content_id>', methods=['DELETE'])
def delete_flag_content(content_id):
    # Query to delete the flagged address content
    query = '''
        DELETE FROM ContentFlag
        WHERE flagID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (content_id,))
    db.get_db().commit()

    return make_response(f"Address content with ID {content_id} deleted successfully", 200)

#------------------------------------------------------------
# GET activity log
@admin.route('/activity-log', methods=['GET'])
def get_activity_log():
    # Get query parameters for filtering
    user_id = request.args.get('userID')
    activity_type = request.args.get('activityType')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    # Base query
    query = '''
        SELECT activityID, userID, activityType, logTime
        FROM ActivityLog
        WHERE 1=1
    '''
    params = []

    # Add filters if provided
    if user_id:
        query += ' AND userID = %s'
        params.append(user_id)
    if activity_type:
        query += ' AND activityType = %s'
        params.append(activity_type)
    if start_date and end_date:
        query += ' AND logTime BETWEEN %s AND %s'
        params.append(start_date)
        params.append(end_date)

    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    logs = cursor.fetchall()

    # Return the logs
    the_response = make_response(jsonify(logs))
    the_response.status_code = 200
    return the_response

@admin.route('/forumdiscussions', methods=['GET'])
def get_forum_discussions():
    query = """
        SELECT
            ForumDiscussion.discussionID,
            ForumDiscussion.title,
            ForumDiscussion.content,
            ForumDiscussion.tags,
            ForumDiscussion.createdAt,
            CONCAT(User.firstName, ' ', User.lastName) AS createdBy,
            COUNT(Comment.commentID) AS commentCount
        FROM
            ForumDiscussion
        INNER JOIN
            User ON ForumDiscussion.createdBy = User.userID
        LEFT JOIN
            Comment ON ForumDiscussion.discussionID = Comment.forumID
        GROUP BY
            ForumDiscussion.discussionID,
            ForumDiscussion.title,
            ForumDiscussion.content,
            ForumDiscussion.tags,
            ForumDiscussion.createdAt,
            User.firstName,
            User.lastName
        ORDER BY
            ForumDiscussion.createdAt DESC;
            """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    discussions = cursor.fetchall()
    response = jsonify(discussions)
    response.status_code = 200
    return response

@admin.route('/admins/<int:user_id>', methods=['GET'])
def get_admin_profile(user_id):
    query = """
        SELECT
            User.userID,
            User.firstName,
            User.lastName,
            User.email,
            User.phoneNum,
            User.registrationDate,
            'admin' AS role
        FROM
            User
        INNER JOIN
            Admin ON User.userID = Admin.userID
        WHERE
            User.role = 'admin' AND User.userID = %s;
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    
    if result:
        return make_response(jsonify(result), 200)
    else:
        return make_response({"error": f"Admin with User ID {user_id} not found."}, 404)