from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create the Blueprint object for Employer routes
employer = Blueprint('employer', __name__)

# -------------------- ROUTES -------------------- #

# 1. GET all employers
@employer.route('/employers', methods=['GET'])
def get_employers():
    location = request.args.get('location')
    industry = request.args.get('company_industry')

    query = 'SELECT employer_id, name, location, company_industry FROM employer'
    filters = []
    if location:
        filters.append(f"location = '{location}'")
    if industry:
        filters.append(f"company_industry = '{industry}'")

    if filters:
        query += ' WHERE ' + ' AND '.join(filters)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    employers = cursor.fetchall()

    response = make_response(jsonify(employers))
    response.status_code = 200
    return response

# 2. GET employer details by ID
@employer.route('/employers/<int:employer_id>', methods=['GET'])
def get_employer_by_id(employer_id):
    query = f'''
        SELECT employer_id, name, location, company_industry
        FROM employer
        WHERE employer_id = {employer_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    employer = cursor.fetchone()

    if employer:
        response = make_response(jsonify(employer))
        response.status_code = 200
    else:
        response = make_response({"error": f"Employer with ID {employer_id} not found"})
        response.status_code = 404
    return response


# 3. POST a new employer
@employer.route('/employers', methods=['POST'])
def create_employer():
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    location = the_data['location']
    company_industry = the_data['company_industry']

    query = f'''
        INSERT INTO employer (name, location, company_industry)
        VALUES ('{name}', '{location}', '{company_industry}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response({"message": "Employer created successfully"})
    response.status_code = 201
    return response


# 4. PUT to update an employer's details
@employer.route('/employers/<int:employer_id>', methods=['PUT'])
def update_employer(employer_id):
    the_data = request.json
    current_app.logger.info(the_data)

    updates = []
    if 'name' in the_data:
        updates.append(f"name = '{the_data['name']}'")
    if 'location' in the_data:
        updates.append(f"location = '{the_data['location']}'")
    if 'company_industry' in the_data:
        updates.append(f"company_industry = '{the_data['company_industry']}'")

    if not updates:
        response = make_response({"error": "No valid fields provided for update"})
        response.status_code = 400
        return response

    query = f'''
        UPDATE employer
        SET {", ".join(updates)}
        WHERE employer_id = {employer_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response({"message": f"Employer {employer_id} updated successfully"})
    response.status_code = 200
    return response


# 5. DELETE an employer
@employer.route('/employers/<int:employer_id>', methods=['DELETE'])
def delete_employer(employer_id):
    query = f'''
        DELETE FROM employer
        WHERE employer_id = {employer_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response({"message": f"Employer {employer_id} deleted successfully"})
    response.status_code = 200
    return response
