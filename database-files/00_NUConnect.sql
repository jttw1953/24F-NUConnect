DROP SCHEMA IF EXISTS `nuconnect` ;
CREATE SCHEMA IF NOT EXISTS `nuconnect` DEFAULT CHARACTER SET latin1 ;
USE `nuconnect` ;

CREATE TABLE `User` (
    userID INT AUTO_INCREMENT,
    registrationDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(75),
    phoneNum VARCHAR(30),
    role VARCHAR(20),
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

CREATE TABLE `UserDiscussions` (
    userID INT NOT NULL,
    discussionID INT NOT NULL,
    PRIMARY KEY (userID, discussionID),
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (discussionID) REFERENCES ForumDiscussion(discussionID)
);

CREATE TABLE `UserComments` (
    userID INT NOT NULL,
    commentID INT NOT NULL,
    PRIMARY KEY (userID, commentID),
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (commentID) REFERENCES Comment(commentID)
);

CREATE TABLE `DiscussionFlags` (
    discussionID INT NOT NULL,
    flagID INT NOT NULL,
    PRIMARY KEY (discussionID, flagID),
    FOREIGN KEY (discussionID) REFERENCES ForumDiscussion(discussionID),
    FOREIGN KEY (flagID) REFERENCES ContentFlag(flagID)
);

CREATE TABLE `CommentFlags` (
    commentID INT NOT NULL,
    flagID INT NOT NULL,
    PRIMARY KEY (commentID, flagID),
    FOREIGN KEY (commentID) REFERENCES Comment(commentID),
    FOREIGN KEY (flagID) REFERENCES ContentFlag(flagID)
);