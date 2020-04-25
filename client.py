import cmd
import datetime
import mysql.connector



class Client(cmd.Cmd):
    intro = 'Welcome to our social Network app. Type help or ? to list commands.\n'
    prompt = '(social network client)'

    cnx = mysql.connector.connect(
        host="18.234.70.125",
        database="social_network",
        user="SCG",
        password="scg199821")
    cursor = cnx.cursor()

    def __init__(self):
        super(Client, self).__init__()
        self.current_user_id = None

    def do_signup(self, arg):
        if(self.current_user_id != None):
            print("Please log out first" )
            return
        username = input("Username (can't be empty): ")
        password = input("Password (can't be empty): ")
        email = input("Email: ")
        gender = input("Gender: ")
        occupation = input("Occupation: ")
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        year, month, day = map(int, date_entry.split('-'))
        birthday = datetime.date(year, month, day)
        data = (username, email, gender, password, birthday, occupation)
        print(birthday)
        self.cursor.execute("INSERT INTO Users VALUES(null,%s,%s,%s,%s,%s,now(),%s)", data)
        self.cnx.commit()

    def do_login(self, arg):
        if (self.current_user_id != None):
            print("Please log out first")
            return
        username = input("Username (can't be empty): ")
        password = input("Password (can't be empty): ")
        self.cursor.execute("SELECT hash FROM Users WHERE alias = %s", (username,))
        realpassword = self.cursor.fetchone()
        if realpassword != None and password == realpassword[0]:
            print("Login Succeed. Welcome, {}!".format(username))
            self.cursor.execute("SELECT userID FROM Users WHERE alias = %s", (username,))
            self.current_user_id = self.cursor.fetchone()[0]
            print("userid: ", self.current_user_id)
        else:
            print("Login Failed. Incorrect User/Password pair!!!")

    def do_logout(self, arg):
        if (self.current_user_id == None):
            print("No one is logged in!")
            return
        print("You have been logged out!")
        self.current_user_id = None

    def do_createpost(self, arg):
        if (self.current_user_id == None):
            print("Please log in first")
            return
        topic = input("Input your post topic: ")
        content = input("Input your post content: ")
        image = input("Image location: ")
        link = input("Link adress: ")
        if not topic or not content:
            print("topic and content mandatory")
            return
        try:
            ## find topic
            topicid = None
            self.cursor.execute("SELECT topicID FROM Topics WHERE topicName = %s;", (topic,))
            result = self.cursor.fetchone()
            if result:
                topicid = result[0]
                print("topicid: ", topicid)
            else:
                # Insert the topic is topic does not exist
                self.cursor.execute("INSERT INTO Topics (topicID, topicName) VALUES (%s, %s);", (topicid, topic))
                topicid = self.cursor.lastrowid
                print("New topic created: ", topicid, topic)
            # Insert the post with the topic
            self.cursor.execute("INSERT INTO Posts (userID, post, topicID) VALUES (%s, %s, %s);", (self.current_user_id, content,topicid))
            postid = self.cursor.lastrowid
            if image:
                self.cursor.execute("INSERT INTO Images VALUES (%s, %s);", (postid, image))
            if link:
                self.cursor.execute("INSERT INTO Links VALUES (%s, %s);", (postid, link))
            self.cnx.commit()
        except mysql.connector.Error as error:
            print("Create post failed with error: {}".format(error))
            self.cnx.rollback()

    def do_createreply(self, arg):
        if (self.current_user_id == None):
            print("Please log in first")
            return
        postid = input("ID of the post you want to reply to: ")
        self.cursor.execute("SELECT topicID FROM Posts WHERE postID = %s;", (postid,))
        result = self.cursor.fetchone()
        if (not result):
            print("Sorry post doesn't exit!")
            return
        content = input("Input your post content: ")
        image = input("Image location: ")
        link = input("Link adress: ")
        if not content:
            print("Sorry, empty content")
            return
        self.cursor.execute("INSERT INTO Posts (userID, post, topicID, parentID) VALUES (%s, %s, %s, %s);",
                            (self.current_user_id, content, result[0], postid))
        postid = self.cursor.lastrowid
        if image:
            self.cursor.execute("INSERT INTO Images VALUES (%s, %s);", (postid, image))
        if link:
            self.cursor.execute("INSERT INTO Links VALUES (%s, %s);", (postid, link))
        self.cnx.commit()

    def do_thumbup(self, arg):
        if (self.current_user_id == None):
            print("Please log in first")
            return
        postid = input("ID of the post you want to thumb up: ")
        self.cursor.execute("SELECT 1 FROM Posts WHERE postID = %s;", (postid,))
        result = self.cursor.fetchone()
        if not result: #check exist of post
            print("Sorry post doesn't exit!")
            return
        self.cursor.execute("INSERT INTO Thumb_up_downs VALUES (%s, %s, 1)"
                            "ON DUPLICATE KEY UPDATE isUp = 1;",
                            (self.current_user_id, postid))
        self.cnx.commit()

    def do_thumbdown(self, arg):
        if (self.current_user_id == None):
            print("Please log in first")
            return
        postid = input("ID of the post you want to thumb down: ")
        self.cursor.execute("SELECT 1 FROM Posts WHERE postID = %s;", (postid,))
        result = self.cursor.fetchone()
        if not result: #check exist of post
            print("Sorry post doesn't exit!")
            return
        self.cursor.execute("INSERT INTO Thumb_up_downs VALUES (%s, %s, 0)"
                            "ON DUPLICATE KEY UPDATE isUp = 0;",
                            (self.current_user_id, postid))
        self.cnx.commit()

    def do_topics(self, arg):
        if (self.current_user_id == None):
            print("Please log in first")
            return
        print("Navigate all Topics")
        self.cursor.execute("SELECT topicID, topicName FROM Topics WHERE parentID IS null")
        topics = self.cursor.fetchall()
        while(topics):
            for topic in topics:
                print(topic[1])
            selection = input("Choose a topic to navigate to: ")
            selectionID = None
            for topic in topics:
                if (selection == topic[1]):
                    selectionID = topic[0]
                    break
            if not selectionID:
                print("invalid choice")
                return
            self.cursor.execute("SELECT topicID, topicName FROM Topics WHERE parentID = %s", (selectionID,))
            topics = self.cursor.fetchall()
            print ("Subtopics of {}:".format(selection))
        print("No subtopics!")

    def do_follow(self, arg):
        if (self.current_user_id == None):
            print("Please log in first")
            return
        temp = input("Follow user or Follow topic? \n")
        if temp == 'user':
            username = input("Input the user name: ")
            self.cursor.execute("SELECT userID FROM Users WHERE alias = %s;", (username,))
            result = self.cursor.fetchone()
            if result == None:
                print("User not found")
                return
            self.cursor.execute("INSERT IGNORE INTO FollowsUser (userID, targetUserID) VALUES (%s, %s);",
                                (self.current_user_id, result[0]))
            print("Following {}".format(username))
            self.cnx.commit()
        elif temp == 'topic':
            topicname = input("Input the topic name: ")
            self.cursor.execute("SELECT topicID FROM Topics WHERE topicName = %s;", (topicname,))
            result = self.cursor.fetchone()
            if result == None:
                print("Topic not found")
                return
            self.cursor.execute("INSERT IGNORE INTO FollowsTopic (userID, topicID) VALUES (%s, %s);",
                                (self.current_user_id, result[0]))
            print("Following {}".format(topicname))
            self.cnx.commit()
        else:
            print("Wrong answer pick user or topic!!!")

    def do_creategroup(self, arg):
        if (self.current_user_id == None):
            print("Please log in first")
            return
        groupname = input("Please enter the group name: ")
        self.cursor.execute("SELECT groupID FROM UserGroups WHERE groupName = %s;", (groupname,))
        result = self.cursor.fetchone()
        if (result):
            print("Group name already taken. Please use change.")
            return
        self.cursor.execute("INSERT INTO UserGroups (groupName, creatorID) VALUES (%s, %s);",
                            (groupname, self.current_user_id))
        self.cursor.execute("INSERT INTO Members (groupID, userID, role) VALUES (%s, %s, %s);",
                            (self.cursor.lastrowid, self.current_user_id, 'creator'))
        self.cnx.commit()

    def do_joingroup(self, arg):
        if (self.current_user_id == None):
            print("Please log in first")
            return
        groupname = input("Please enter the group name: ")
        role = input("Please enter role: ")
        self.cursor.execute("SELECT groupID FROM UserGroups WHERE groupName = %s;", (groupname,))
        result = self.cursor.fetchone()
        if (not result):
            print("Sorry, group not found")
            return
        # self.cursor.execute("SELECT groupID FROM Members WHERE userID = %s and groupID = %s;", (self.current_user_id, result[0]))
        # result1 = self.cursor.fetchone()
        # if result1:
        #     print("You are already in the group")
        #     return
        if role:
            self.cursor.execute("INSERT IGNORE INTO Members (groupID, userID, role) VALUES (%s, %s, %s);",
                                (result[0], self.current_user_id, role))
        else:
            self.cursor.execute("INSERT IGNORE INTO Members (groupID, userID) VALUES (%s, %s);",
                                (result[0], self.current_user_id))
        self.cnx.commit()

if __name__ == '__main__':
    Client().cmdloop()



