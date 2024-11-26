DROP DATABASE IF EXISTS NUConnect;

CREATE DATABASE IF NOT EXISTS NUConnect;

USE NUConnect;

CREATE TABLE `User` (
    userID INT AUTO_INCREMENT,
    registrationDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(75),
    phoneNum VARCHAR(15),
    role VARCHAR(10),
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    username VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL,
    securityLevel VARCHAR(15),
    PRIMARY KEY(userID)
);

CREATE TABLE `Admin` (
    adminID INT NOT NULL AUTO_INCREMENT,
    userID INT NOT NULL,
    PRIMARY KEY(adminID),
    CONSTRAINT fk_admin_user FOREIGN KEY (userID) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Student` (
    userID INT,
    studentID INT NOT NULL,
    major VARCHAR(30),
    admitYear INT NOT NULL,
    tags TEXT,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(studentID),
    CONSTRAINT fk_student_user FOREIGN KEY (userID) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Skill` (
    skillID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(30),
    description VARCHAR(1000),
    studentID INT NOT NULL,
    PRIMARY KEY(skillID),
    CONSTRAINT fk_skill_student FOREIGN KEY (studentID) REFERENCES Student (studentID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE `Company` (
    companyID INT NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    industry VARCHAR(50),
    location TEXT,
    PRIMARY KEY(companyID)
);

CREATE TABLE `Employers` (
    userID INT,
    employerID INT AUTO_INCREMENT,
    companyID INT,
    PRIMARY KEY(employerID),
    CONSTRAINT fk_employer_user FOREIGN KEY (userID) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_employer_company FOREIGN KEY (companyID) REFERENCES Company (companyID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `ForumDiscussion` (
    discussionID INT NOT NULL AUTO_INCREMENT,
    createdBy INT NOT NULL,
    content TEXT NOT NULL,
    title TEXT NOT NULL,
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
    tags VARCHAR(75),
    PRIMARY KEY(discussionID),
    CONSTRAINT fk_discussion_user FOREIGN KEY (createdBy) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Job` (
    jobID INT NOT NULL AUTO_INCREMENT,
    companyID INT NOT NULL,
    employerID INT,
    title TINYTEXT NOT NULL,
    datePosted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    PRIMARY KEY(jobID),
    CONSTRAINT fk_job_company FOREIGN KEY (companyID) REFERENCES Company (companyID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_job_employer FOREIGN KEY (employerID) REFERENCES Employers (employerID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Application` (
    appID INT NOT NULL AUTO_INCREMENT,
    studentID INT NOT NULL,
    jobID INT NOT NULL,
    dateSubmitted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(15),
    PRIMARY KEY(appID),
    CONSTRAINT fk_application_student FOREIGN KEY (studentID) REFERENCES Student (studentID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_application_job FOREIGN KEY (jobID) REFERENCES Job (jobID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Comment` (
    commentID INT NOT NULL AUTO_INCREMENT,
    createdBy INT NOT NULL,
    forumID INT NOT NULL,
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(commentID),
    CONSTRAINT fk_comment_user FOREIGN KEY (createdBy) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_comment_forum FOREIGN KEY (forumID) REFERENCES ForumDiscussion (discussionID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `DailySummary` (
    summaryID INT NOT NULL AUTO_INCREMENT,
    jobID INT,
    applicationID INT,
    discussionID INT,
    notify INT,
    PRIMARY KEY(summaryID),
    CONSTRAINT fk_dailysummary_jobs FOREIGN KEY (jobID) REFERENCES Job (jobID) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_dailysummary_applications FOREIGN KEY (applicationID) REFERENCES Application (appID) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_dailysummary_discussions FOREIGN KEY (discussionID) REFERENCES ForumDiscussion (discussionID) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_dailysummary_notify FOREIGN KEY (notify) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE `ActivityLog` (
    activityID INT NOT NULL AUTO_INCREMENT,
    logTime DATETIME,
    userID INT NOT NULL,
    activityType VARCHAR(30),
    PRIMARY KEY(activityID),
    CONSTRAINT fk_activitylog_user FOREIGN KEY (userID) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `ContentFlag` (
    flagID INT NOT NULL AUTO_INCREMENT,
    contentID INT,
    timestamp DATETIME,
    reason TEXT,
    status VARCHAR(15),
    PRIMARY KEY(flagID),
    CONSTRAINT fk_contentflag_discussion FOREIGN KEY (contentID) REFERENCES ForumDiscussion (discussionID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `SecurityLog` (
    logID INT NOT NULL AUTO_INCREMENT,
    actionType VARCHAR(30),
    userID INT,
    timestamp DATETIME,
    status VARCHAR(15),
    PRIMARY KEY(logID),
    CONSTRAINT fk_securitylog_user FOREIGN KEY (userID) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `SystemAlert` (
    alertID INT NOT NULL AUTO_INCREMENT,
    alertType VARCHAR(30),
    typeID INT,
    description TEXT,
    timestamp DATETIME,
    status VARCHAR(15),
    notifyAdmin INT,
    triggeredBy INT,
    PRIMARY KEY(alertID),
    CONSTRAINT fk_systemalert_admin FOREIGN KEY (notifyAdmin) REFERENCES Admin (adminID) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_systemalert_user FOREIGN KEY (triggeredBy) REFERENCES User (userID) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE `PerformanceMetrics` (
    metricID INT NOT NULL AUTO_INCREMENT,
    accessedBy INT,
    serverTime INT,
    responseTime INT,
    timestamp DATETIME,
    memoryUsage INT,
    cpuUsage INT,
    PRIMARY KEY(metricID),
    CONSTRAINT fk_performancemetrics_user FOREIGN KEY (accessedBy) REFERENCES Admin (adminID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `Maintenance` (
    maintenanceID INT NOT NULL AUTO_INCREMENT,
    performedBy INT,
    status VARCHAR(30),
    startTime DATETIME,
    endTime DATETIME,
    description TEXT,
    PRIMARY KEY(maintenanceID),
    CONSTRAINT fk_maintenance_user FOREIGN KEY (performedBy) REFERENCES Admin (adminID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE `AuditLog` (
    auditLogID INT NOT NULL AUTO_INCREMENT,
    performedBy INT,
    actionType VARCHAR(30),
    timestamp DATETIME,
    changes TEXT,
    PRIMARY KEY(auditLogID),
    CONSTRAINT fk_auditlog_user FOREIGN KEY (performedBy) REFERENCES Admin (adminID) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Insert into User
INSERT INTO User (registrationDate, email, phoneNum, role, firstName, lastName, username, password, securityLevel)
VALUES
    (NOW(), 'jdoe@example.com', '1234567890', 'Student', 'John', 'Doe', 'jdoe', 'password123', 'Medium'),
    (NOW(), 'asmith@example.com', '0987654321', 'Employer', 'Alice', 'Smith', 'asmith', 'securePass', 'High'),
    (NOW(), 'admin@example.com', '1122334455', 'Admin', 'Bob', 'Admin', 'admin1', 'adminPass', 'High');

-- Insert into Admin
INSERT INTO Admin (userID)
VALUES
    (3),
    (2);

-- Insert into Student
INSERT INTO Student (userID, studentID, major, admitYear, tags, updatedAt)
VALUES
    (1, 101, 'Computer Science', 2022, 'co-op, software engineer', NOW()),
    (1, 102, 'Data Science', 2023, 'co-op, data analysis', NOW());

-- Insert into Skill
INSERT INTO Skill (name, description, studentID)
VALUES
    ('Python', 'Proficient in Python programming.', 101),
    ('Data Analysis', 'Skilled in data cleaning and visualization.', 102),
    ('Machine Learning', 'Knowledge of basic ML algorithms.', 101);

-- Insert into Company
INSERT INTO Company (name, industry, location)
VALUES
    ('TechCorp', 'Technology', 'Boston, MA'),
    ('DataWorks', 'Data Analytics', 'San Francisco, CA'),
    ('HealthTech', 'Healthcare Technology', 'Seattle, WA');

-- Insert into Employers
INSERT INTO Employers (userID, companyID)
VALUES
    (2, 1),
    (2, 2);

-- Insert into ForumDiscussion
INSERT INTO ForumDiscussion (createdBy, content, title, tags, createdAt, updatedAt)
VALUES
    (1, 'What are some tips for acing technical interviews?', 'Technical Interview Tips', 'interview, tips', NOW(), NOW()),
    (2, 'Join our webinar on data engineering!', 'Data Engineering Webinar', 'webinar, data', NOW(), NOW());

-- Insert into Job
INSERT INTO Job (companyID, employerID, title, description, datePosted)
VALUES
    (1, 1, 'Software Engineer Co-op', 'We are seeking a motivated co-op student to join our team.', NOW()),
    (2, 2, 'Data Analyst Co-op', 'Looking for students passionate about data analysis and visualization.', NOW());

-- Insert into Application
INSERT INTO Application (studentID, jobID, dateSubmitted, status)
VALUES
    (101, 1, NOW(), 'Pending'),
    (102, 2, NOW(), 'Reviewed');

-- Insert into Comment
INSERT INTO Comment (createdBy, forumID, createdAt)
VALUES
    (1, 1, NOW()),
    (2, 2, NOW());

-- Insert into DailySummary
INSERT INTO DailySummary (jobID, applicationID, discussionID, notify)
VALUES
    (1, 1, 1, 1),
    (2, 2, 2, 2);

-- Insert into ActivityLog
INSERT INTO ActivityLog (logTime, userID, activityType)
VALUES
    (NOW(), 1, 'Login'),
    (NOW(), 2, 'Posted on Forum');

-- Insert into ContentFlag
INSERT INTO ContentFlag (contentID, timestamp, reason, status)
VALUES
    (1, NOW(), 'Spam content', 'Resolved'),
    (2, NOW(), 'Inappropriate content', 'Unresolved');

-- Insert into SecurityLog
INSERT INTO SecurityLog (actionType, userID, timestamp, status)
VALUES
    ('Failed Login', 1, NOW(), 'Unresolved'),
    ('Password Change', 2, NOW(), 'Resolved');

-- Insert into SystemAlert
INSERT INTO SystemAlert (alertType, typeID, description, timestamp, status, notifyAdmin, triggeredBy)
VALUES
    ('Unauthorized Access', 101, 'Multiple failed login attempts.', NOW(), 'Unresolved', 1, 1),
    ('Server Downtime', 102, 'Scheduled maintenance.', NOW(), 'Resolved', 1, NULL);

-- Insert into PerformanceMetrics
INSERT INTO PerformanceMetrics (accessedBy, serverTime, responseTime, timestamp, memoryUsage, cpuUsage)
VALUES
    (1, 120, 15, NOW(), 75, 30),
    (2, 150, 20, NOW(), 80, 35);

-- Insert into Maintenance
INSERT INTO Maintenance (performedBy, status, startTime, endTime, description)
VALUES
    (1, 'Scheduled', '2024-11-20 22:00:00', '2024-11-21 02:00:00', 'Routine maintenance'),
    (1, 'Completed', '2024-11-18 01:00:00', '2024-11-18 03:00:00', 'Database optimization');

-- Insert into AuditLog
INSERT INTO AuditLog (performedBy, actionType, timestamp, changes)
VALUES
    (1, 'Role Update', NOW(), 'Updated user role to Admin'),
    (2, 'Password Reset', NOW(), 'Reset password for user ID 1');