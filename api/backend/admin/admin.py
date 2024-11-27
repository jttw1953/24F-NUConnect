from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create the Blueprint object for Admin routes
admin = Blueprint('admin', __name__)

# -------------------- ROUTES -------------------- #

# 1. GET all system alerts
@admin.route('/alerts', methods=['GET'])
def get_system_alerts():
    query = '''
        SELECT alert_id, description, timestamp, status
        FROM system_alerts
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# 2. POST a new system alert
@admin.route('/alerts', methods=['POST'])
def create_system_alert():
    the_data = request.json
    current_app.logger.info(the_data)

    description = the_data['description']
    status = the_data['status']

    query = f'''
        INSERT INTO system_alerts (description, status)
        VALUES ('{description}', '{status}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("System alert created successfully")
    response.status_code = 201
    return response

# 3. PUT to update a system alert
@admin.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_system_alert(alert_id):
    the_data = request.json
    current_app.logger.info(the_data)

    status = the_data.get('status', None)
    description = the_data.get('description', None)

    update_query = "UPDATE system_alerts SET "
    if status:
        update_query += f"status = '{status}'"
    if description:
        update_query += f", description = '{description}'"
    update_query += f" WHERE alert_id = {alert_id}"

    cursor = db.get_db().cursor()
    cursor.execute(update_query)
    db.get_db().commit()

    response = make_response(f"System alert {alert_id} updated successfully")
    response.status_code = 200
    return response

# 4. GET all maintenance schedules
@admin.route('/maintenance', methods=['GET'])
def get_maintenance_schedules():
    query = '''
        SELECT maintenance_id, description, start_time, end_time, scheduled_by
        FROM maintenance
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# 5. DELETE a maintenance schedule
@admin.route('/maintenance/<int:maintenance_id>', methods=['DELETE'])
def delete_maintenance_schedule(maintenance_id):
    query = f'''
        DELETE FROM maintenance
        WHERE maintenance_id = {maintenance_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response(f"Deleted maintenance schedule {maintenance_id}")
    response.status_code = 200
    return response
