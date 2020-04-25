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
        if not self.current_user_id:
            print("Please log in first")
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
        print("Signup successful! Congrats = %s", username)

    def do_login(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        username = input("Username (can't be empty): ")
        password = input("Password (can't be empty): ")
        self.cursor.execute("SELECT password FROM Users WHERE alias = %s", (username,))
        realpassword = self.cursor.fetchone()
        if realpassword and password == realpassword[0]:
            print("Login Succeed. Welcome, {}!".format(username))
            self.cursor.execute("SELECT userID FROM Users WHERE alias = %s", (username,))
            self.current_user_id = self.cursor.fetchone()[0]
            print("userid: ", self.current_user_id)
        else:
            print("Login Failed. Incorrect User/Password pair!!!")

    def do_logout(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        print("You have been logged out!")
        self.current_user_id = None

    def do_create_post(self, arg):
        if not self.current_user_id:
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
            print("Post successful! PostID = %s", postid)
        except mysql.connector.Error as error:
            print("Create post failed with error: {}".format(error))
            self.cnx.rollback()

    def do_create_reply(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        postid = input("ID of the post you want to reply to: ")
        self.cursor.execute("SELECT topicID FROM Posts WHERE postID = %s;", (postid,))
        result = self.cursor.fetchone()
        if not result:
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
        print("Reply successful! Reply PostID = %s", postid)

    def do_thumb_up(self, arg):
        if not self.current_user_id:
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
        print("Thumb up successful! PostID = %s", postid)


    def do_thumb_down(self, arg):
        if not self.current_user_id:
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
        print("Thumb down successful! PostID = %s", postid)

    def do_follow(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        temp = input("Follow user or Follow topic? \n")
        if temp == 'user':
            username = input("Input the user name: ")
            self.cursor.execute("SELECT userID FROM Users WHERE alias = %s;", (username,))
            result = self.cursor.fetchone()
            if not result:
                print("User not found")
                return
            self.cursor.execute("INSERT IGNORE INTO FollowsUser (userID, targetUserID) VALUES (%s, %s);",
                                (self.current_user_id, result[0]))
            self.cnx.commit()
            print("Following {}".format(username))
        elif temp == 'topic':
            topicname = input("Input the topic name: ")
            self.cursor.execute("SELECT topicID FROM Topics WHERE topicName = %s;", (topicname,))
            result = self.cursor.fetchone()
            if not result:
                print("Topic not found")
                return
            self.cursor.execute("INSERT IGNORE INTO FollowsTopic (userID, topicID) VALUES (%s, %s);",
                                (self.current_user_id, result[0]))
            self.cnx.commit()
            print("Following {}".format(topicname))
        else:
            print("Wrong answer pick user or topic!!!")

    def do_create_group(self, arg):
        if not self.current_user_id:
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
        print("Create successful! Group name = %s", groupname)


    def do_join_group(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        groupname = input("Please enter the group name: ")
        role = input("Please enter role: ")
        self.cursor.execute("SELECT groupID FROM UserGroups WHERE groupName = %s;", (groupname,))
        result = self.cursor.fetchone()
        if not result:
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
        print("Join successful! Group name = %s", groupname)


    def do_delete_group(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        groupname = input("Please enter the group name to be deleted: ")
        self.cursor.execute("SELECT creatorID, groupID FROM UserGroups WHERE groupName = %s;", (groupname,))
        result = self.cursor.fetchone()
        if not result:
            print("Sorry, group not found")
            return
        # check if the user created/owns the group
        if result[0] != self.current_user_id:
            print("Sorry, you don't own this group!")
            return
        # delete row in usergroup table
        self.cursor.execute("DELETE FROM UserGroups WHERE groupName = %s;", (groupname,))
        # delete rows in member table
        self.cursor.execute("DELETE FROM Members WHERE groupID = %s;", (result[1],))
        self.cnx.commit()
        print("Delete successful! Group name = %s", groupname)


    def do_quit_group(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        groupname = input("Please enter the group name (quit): ")
        self.cursor.execute("SELECT creatorID, groupID FROM UserGroups WHERE groupName = %s;", (groupname,))
        result = self.cursor.fetchone()
        if not result:
            print("Sorry, group not found")
            return
        # check if the user created/owns the group
        if result[0] == self.current_user_id:
            print("Sorry, you created/own this group. You can't quit but delete the group.")
            return
        # check if the user is in the group
        self.cursor.execute("SELECT userID FROM UserGroups WHERE groupID = %s and userID = %s;",
                            (result[1], self.current_user_id))
        result1 = self.cursor.fetchone()
        if not result1:
            print("Sorry, you are not in this group!")
            return
        # delete row in member table
        self.cursor.execute("DELETE FROM Members WHERE groupID = %s and userID = %s;",
                            (result[1], self.current_user_id))
        self.cnx.commit()
        print("Quit successful! Group name = %s", groupname)


if __name__ == '__main__':
    Client().cmdloop()



