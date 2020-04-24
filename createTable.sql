DROP DATABASE IF EXISTS `social_network`;
CREATE DATABASE IF NOT EXISTS `social_network`;

USE social_network;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    userID VARCHAR (50),
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
    topicID VARCHAR (50),
    topicName VARCHAR (50),
    parentID VARCHAR (50),
    PRIMARY KEY (topicID)
);

DROP TABLE IF EXISTS UserGroups;
CREATE TABLE UserGroups(
    groupID VARCHAR (50),
    groupName VARCHAR (50),
    creatorID VARCHAR (50),
    PRIMARY KEY (groupID),
    FOREIGN KEY (creatorID) REFERENCES Users(userID)
);

DROP TABLE IF EXISTS Members;
CREATE TABLE Members(
    groupID VARCHAR(50),
    userID VARCHAR(50),
    role VARCHAR(50),
    PRIMARY KEY (groupID, userID),
    FOREIGN KEY (groupID) REFERENCES UserGroups(groupID),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

DROP TABLE IF EXISTS Follows;
CREATE TABLE Follows (
    userID VARCHAR (50),
    targetUserID VARCHAR (50),
    topicID VARCHAR (50),
    PRIMARY KEY (userID, targetUserID, topicID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (topicID) REFERENCES Topics(topicID)
);

DROP TABLE IF EXISTS Posts;
CREATE TABLE Posts (
    postID VARCHAR (50),
    post TEXT,
    postTime DATETIME,
    userID VARCHAR (50),
    topicID VARCHAR (50),
    parentID VARCHAR(50),
    PRIMARY KEY (postID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (topicID) REFERENCES Topics(topicID)
);

DROP TABLE IF EXISTS Images;
CREATE TABLE Images (
    postID VARCHAR(50),
    location VARCHAR(100),
    PRIMARY KEY (postID, location),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);

DROP TABLE IF EXISTS Links;
CREATE TABLE Links (
    postID VARCHAR(50),
    link VARCHAR(100),
    PRIMARY KEY (postID, link),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);

DROP TABLE IF EXISTS ReadPost;
CREATE TABLE ReadPost (
    userID VARCHAR(50),
    postID VARCHAR(50),
    PRIMARY KEY (userID, postID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);
DROP TABLE IF EXISTS Seens;
CREATE TABLE Seens (
    userID VARCHAR (50),
    postID VARCHAR (50),
    PRIMARY KEY (userID, postID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);

DROP TABLE IF EXISTS Thumb_up_downs;
CREATE TABLE Thumb_up_downs (
    userID VARCHAR (50),
    postID VARCHAR (50),
    isUp BOOL,
    PRIMARY KEY (userID, postID),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (postID) REFERENCES Posts(postID)
);
