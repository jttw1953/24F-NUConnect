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
@employer.route('/employers/<int:user_id>', methods=['GET'])
def get_employer_by_id(user_id):
    query = f'''
        SELECT
            User.userID,
            User.email,
            User.phoneNum,
            User.firstName,
            User.lastName,
            Company.name AS companyName,
            Company.industry,
            Company.location
        FROM
            User
        INNER JOIN
            Employers ON User.userID = Employers.userID
        INNER JOIN
            Company ON Employers.companyID = Company.companyID
        WHERE
            User.userID = {user_id};
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    employer = cursor.fetchone()

    if employer:
        response = make_response(jsonify(employer))
        response.status_code = 200
    else:
        response = make_response({"error": f"Employer with User ID {user_id} not found"})
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

# 5 return a role
@employer.route('/role/<int:user_id>', methods=['GET'])
def get_role(user_id):
    query = f'''
        SELECT role FROM User WHERE User.UserID = {user_id}'''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#return all applicaction applied by students:

@employer.route('/applications/employer/<int:user_id>', methods=['GET'])
def get_employer_applications(user_id):
    query = f"""
            SELECT
                EmployerUser.userID AS employerUserID,
                Application.appID,
                Job.title AS jobTitle,
                Company.name AS companyName,
                CONCAT(StudentUser.firstName, ' ', StudentUser.lastName) AS studentName,
                Application.status,
                Application.dateSubmitted

            FROM
                Application
            INNER JOIN
                Job ON Application.jobID = Job.jobID
            INNER JOIN
                Company ON Job.companyID = Company.companyID
            INNER JOIN
                Student ON Application.studentID = Student.studentID
            INNER JOIN
                User AS StudentUser ON Student.userID = StudentUser.userID
            INNER JOIN
                Employers ON Job.employerID = Employers.employerID
            INNER JOIN
                User AS EmployerUser ON Employers.userID = EmployerUser.userID
            WHERE Employers.userID = {user_id};
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    return jsonify(results) if results else jsonify({"error": "No applications found"}), 404