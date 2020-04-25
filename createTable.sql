DROP DATABASE IF EXISTS `social_network`;
CREATE DATABASE IF NOT EXISTS `social_network`;

USE social_network;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    userID INT NOT NULL AUTO_INCREMENT,
    alias VARCHAR (50),
    email VARCHAR (50),
    gender VARCHAR (50),
    hash VARCHAR (50),
    birthDate DATE,
    lastLoginDateTime DATETIME,
    occupation VARCHAR(50),
    PRIMARY KEY (userID)
);

DROP TABLE IF EXISTS Topics;
CREATE TABLE Topics (
    topicID INT NOT NULL AUTO_INCREMENT,
    topicName VARCHAR (50),
    parentID INT DEFAULT null,
    PRIMARY KEY (topicID)
);

DROP TABLE IF EXISTS UserGroups;
CREATE TABLE UserGroups(
    groupID INT NOT NULL AUTO_INCREMENT,
    groupName VARCHAR (50),
    creatorID INT,
    PRIMARY KEY (groupID),
    FOREIGN KEY (creatorID) REFERENCES Users(userID)
);

DROP TABLE IF EXISTS Members;
CREATE TABLE Members(
    groupID INT,
    userID INT,
    role VARCHAR(50) DEFAULT 'member',
    PRIMARY KEY (groupID, userID),
    FOREIGN KEY (groupID) REFERENCES UserGroups(groupID),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

DROP TABLE IF EXISTS FollowsUser;
CREATE TABLE FollowsUser (
    userID INT,
    targetUserID INT,
    PRIMARY KEY (userID, targetUserID),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

DROP TABLE IF EXISTS FollowsTopic;
CREATE TABLE FollowsTopic (
    userID INT,
    topicID INT,
    PRIMARY KEY (userID, topicID),
    FOREIGN KEY (topicID) REFERENCES Topics(topicID)
);


DROP TABLE IF EXISTS Posts;
CREATE TABLE Posts (
    postID INT NOT NULL AUTO_INCREMENT,
    post TEXT,
    postTime DATETIME DEFAULT now(),
    userID INT,
    topicID INT,
    parentID INT DEFAULT null,
    PRIMARY KEY (postID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (topicID) REFERENCES Topics(topicID)
);

DROP TABLE IF EXISTS Images;
CREATE TABLE Images (
    postID INT,
    location VARCHAR(100),
    PRIMARY KEY (postID, location),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);

DROP TABLE IF EXISTS Links;
CREATE TABLE Links (
    postID INT,
    link VARCHAR(100),
    PRIMARY KEY (postID, link),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);

DROP TABLE IF EXISTS Seens;
CREATE TABLE Seens (
    userID INT,
    postID INT,
    PRIMARY KEY (userID, postID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);

DROP TABLE IF EXISTS Thumb_up_downs;
CREATE TABLE Thumb_up_downs (
    userID INT,
    postID INT,
    isUp BOOL,
    PRIMARY KEY (userID, postID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);
