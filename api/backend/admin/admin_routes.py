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
        SELECT alert_id, description, timestamp, status
        FROM system_alerts
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
        INSERT INTO system_alerts (description, status)
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
        updates.append(f"status = '{status}'")
    if description:
        updates.append(f"description = '{description}'")
    
    if not updates:
        return make_response("No updates provided", 400)

    query = f'''
        UPDATE system_alerts
        SET {', '.join(updates)}
        WHERE alert_id = {alert_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response(f"System alert {alert_id} updated successfully", 200)

#------------------------------------------------------------
# Get all maintenance schedules
@admin.route('/maintenance', methods=['GET'])
def get_maintenance_schedules():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT maintenance_id, description, start_time, end_time, scheduled_by
        FROM maintenance
    ''')
    schedules = cursor.fetchall()
    the_response = make_response(jsonify(schedules))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete a maintenance schedule by ID
@admin.route('/maintenance/<int:maintenance_id>', methods=['DELETE'])
def delete_maintenance_schedule(maintenance_id):
    query = '''
        DELETE FROM maintenance
        WHERE maintenance_id = %s
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
        SELECT log_id, action_type, ip_address, timestamp FROM security_log
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
        SELECT metric_id, server_name, response_time, memory_usage, cpu_usage
        FROM performance_metric
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
    start_time = maintenance_data['start_time']
    end_time = maintenance_data['end_time']
    scheduled_by = maintenance_data['scheduled_by']

    query = '''
        INSERT INTO maintenance (description, start_time, end_time, scheduled_by)
        VALUES (%s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (description, start_time, end_time, scheduled_by))
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
        INSERT INTO content_flag (reason, status)
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
    start_time = maintenance_data.get('start_time')
    end_time = maintenance_data.get('end_time')
    scheduled_by = maintenance_data.get('scheduled_by')

    updates = []
    if description:
        updates.append("description = %s")
    if start_time:
        updates.append("start_time = %s")
    if end_time:
        updates.append("end_time = %s")
    if scheduled_by:
        updates.append("scheduled_by = %s")

    if not updates:
        response = make_response("No fields provided for update")
        response.status_code = 400
        return response

    query = f'''
        UPDATE maintenance
        SET {', '.join(updates)}
        WHERE maintenance_id = %s
    '''
    cursor = db.get_db().cursor()
    params = [value for value in (description, start_time, end_time, scheduled_by) if value]
    params.append(maintenance_id)
    cursor.execute(query, params)
    db.get_db().commit()

    response = make_response(f"Maintenance schedule {maintenance_id} updated successfully")
