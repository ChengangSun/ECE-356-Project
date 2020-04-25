import cmd
import datetime
import mysql.connector


class Client(cmd.Cmd):
    intro = 'Welcome to our social Network app. Type help or ? to list commands.\n'
    prompt = '(social network client): '

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
        if self.current_user_id:
            print("Please log out first")
            return
        # check if user name already exist
        namecheck = 0
        while namecheck == 0:
            username = input("Username (can't be empty): ")
            self.cursor.execute("SELECT userID FROM Users WHERE alias = %s", (username,))
            if not self.cursor.fetchone():
                namecheck = 1
            else:
                print("User name already exist. Please pick a new one")
        password = input("Password (can't be empty): ")
        email = input("Email: ")
        # check gender requirement
        gendercheck = 0
        while gendercheck == 0:
            gender = input("Gender(MALE/FEMALE/OTHER OR empty): ")
            if gender == "MALE" or gender == "FEMALE" or gender == "other" or (not gender):
                gendercheck = 1
            else:
                print("Gender unclear. Please re-enter.")
        occupation = input("Occupation: ")
        # check if birth date is empty or wrong format
        datecheck = 0
        year = month = day = 0
        birthday = datetime.date.today()
        while datecheck == 0:
            date_entry = input('Enter a date in YYYY-MM-DD format: ')
            if date_entry:
                try:
                    year, month, day = map(int, date_entry.split('-'))
                except ValueError:
                    year = month = day = 0
            if 1900 < year and 0 < month < 13 and 0 < day < 32:
                birthday = datetime.date(year, month, day)
            if birthday < datetime.date.today():
                datecheck = 1
            if datecheck == 0:
                print("Format wrong. Please input correct date!")
        data = (username, email, gender, password, birthday, occupation)
        print(birthday)
        self.cursor.execute("INSERT INTO Users VALUES(null,%s,%s,%s,%s,%s,now(),%s)", data)
        self.cnx.commit()
        print("Signup successful! Congrats = %s" % username)

    def do_login(self, arg):
        if self.current_user_id:
            print("Please log out first")
            return
        username = input("Username (can't be empty): ")
        password = input("Password (can't be empty): ")
        self.cursor.execute("SELECT password FROM Users WHERE alias = %s", (username,))
        realpassword = self.cursor.fetchone()
        if realpassword and password == realpassword[0]:
            print("Login Succeed. Welcome, {}!".format(username))
            self.cursor.execute("SELECT userID FROM Users WHERE alias = %s", (username,))
            self.current_user_id = self.cursor.fetchone()[0]
            print("userid: %s" % self.current_user_id)
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
            # find topic
            topicid = None
            self.cursor.execute("SELECT topicID FROM Topics WHERE topicName = %s;", (topic,))
            result = self.cursor.fetchone()
            if result:
                topicid = result[0]
                print("topicid: %s" % topicid)
            else:
                # Insert the topic if topic does not exist
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
            print("Post successful! PostID = %s" % postid)
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
        print("Reply successful! Reply PostID = %s" % postid)

    def do_get_single_post(self, args):
        if not self.current_user_id:
            print("Please log in first")
            return
        postid = input("ID of the post you want to see: ")
        #postID, post, postTime, alias, topicName, parentID, points
        self.cursor.execute("SELECT * FROM view_post WHERE postID = %s", (postid,))
        result = self.cursor.fetchone()
        if not result:
            print("Post does not exist")
            return
        print("PostID: %s" % result[0])
        print("Topic: %s" % result[4])
        print("Author: %s" % result[3])
        print("Post Time: %s" % result[2])
        if (result[5]): 
            print("Reply to: %s" % result[5])
        print("Content: %s" % result[1])
        print("Points: %s" % result[6])
        self.cursor.execute("INSERT IGNORE INTO Seens (userID, postID) VALUES (%s, %s)",
                            (self.current_user_id, result[0]))
        self.cnx.commit()

    def do_get_user_posts(self, args):
        if not self.current_user_id:
            print("Please log in first")
            return
        username = input("username of the user you want to see: ")
        self.cursor.execute("SELECT * FROM Users WHERE alias = %s", (username,))
        if not self.cursor.fetchone():
            print("User does not exist")
            return
        self.cursor.execute("SELECT * FROM view_post WHERE alias = %s", (username,))
        posts = self.cursor.fetchall()
        if not posts:
            print("User has no posts")
        for post in posts:
            print("PostID: %s" % post[0])
            print("Topic: %s" % post[4])
            print("Author: %s" % post[3])
            print("Post Time: %s" % post[2])
            if (post[5]): 
                print("Reply to: %s" % post[5])
            print("Content: %s" % post[1])
            print("Points: %s" % post[6])
            print("------------------------------")
            self.cursor.execute("INSERT IGNORE INTO Seens (userID, postID) VALUES (%s, %s)",
                            (self.current_user_id, post[0]))
        self.cnx.commit()

    def do_get_topic_posts(self, args):
        if not self.current_user_id:
            print("Please log in first")
            return
        topicname = input("Topic you want to see: ")
        self.cursor.execute("SELECT topicID FROM Topics WHERE topicName = %s", (topicname,))
        topicID = self.cursor.fetchone()
        if not topicID:
            print("Topic does not exist")
            return
        allTopics = []
        toSearch = [topicID[0]]
        #get all subtopics
        while toSearch:
            nextToSearch = []
            for topicID in toSearch:
                self.cursor.execute("SELECT topicID FROM Topics WHERE parentID = %s", (topicID,))
                results = self.cursor.fetchall()
                for result in results:
                    nextToSearch.append(result[0])
            allTopics.extend(toSearch)
            toSearch = nextToSearch
        serialize = "(" + str(allTopics[0])
        for i in range(1, len(allTopics)):
            serialize += (", " + str(allTopics[i]))
        serialize += ")"
        self.cursor.execute("SELECT * FROM view_post WHERE topicID IN " + serialize)
        posts = self.cursor.fetchall()
        if not posts:
            print("No new posts! Follow for more!")
        for post in posts:
            print("PostID: %s" % post[0])
            print("Topic: %s" % post[4])
            print("Author: %s" % post[3])
            print("Post Time: %s" % post[2])
            if (post[5]): 
                print("Reply to: %s" % post[5])
            print("Content: %s" % post[1])
            print("Points: %s" % post[6])
            print("------------------------------")
            self.cursor.execute("INSERT IGNORE INTO Seens (userID, postID) VALUES (%s, %s)",
                            (self.current_user_id, post[0]))
        self.cnx.commit()

    def do_get_new_posts(self, args):
        if not self.current_user_id:
            print("Please log in first")
            return
        self.cursor.execute("SELECT topicID FROM FollowsTopic WHERE userID = %s", (self.current_user_id,))
        results = self.cursor.fetchall()
        allTopics = []
        toSearch = []
        for result in results:
            toSearch.append(result[0])
        #get all subtopics
        while toSearch:
            nextToSearch = []
            for topicID in toSearch:
                self.cursor.execute("SELECT topicID FROM Topics WHERE parentID = %s", (topicID,))
                results = self.cursor.fetchall()
                for result in results:
                    nextToSearch.append(result[0])
            allTopics.extend(toSearch)
            toSearch = nextToSearch
        serialize = "(" + str(allTopics[0])
        for i in range(1, len(allTopics)):
            serialize += (", " + str(allTopics[i]))
        serialize += ")"
        self.cursor.execute("SELECT * FROM view_post "
                            "WHERE (userID IN (SELECT targetUserID FROM FollowsUser WHERE userID = %s) OR topicID IN " + serialize + ") "
                            "AND postID NOT IN (SELECT postID FROM Seens WHERE userID = %s)",
                            (self.current_user_id, self.current_user_id))
        posts = self.cursor.fetchall()
        if not posts:
            print("Topic has no posts")
        for post in posts:
            print("PostID: %s" % post[0])
            print("Topic: %s" % post[4])
            print("Author: %s" % post[3])
            print("Post Time: %s" % post[2])
            if (post[5]): 
                print("Reply to: %s" % post[5])
            print("Content: %s" % post[1])
            print("Points: %s" % post[6])
            print("------------------------------")
            self.cursor.execute("INSERT IGNORE INTO Seens (userID, postID) VALUES (%s, %s)",
                            (self.current_user_id, post[0]))
        self.cnx.commit()

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
        print("Thumb up successful! PostID = %s" % postid)

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
        print("Thumb down successful! PostID = %s" % postid)

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

    def do_get_follows(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        self.cursor.execute("SELECT alias FROM FollowsUser fu "
                            "INNER JOIN Users u ON fu.targetUserID = u.userID "
                            "WHERE fu.userID = %s", (self.current_user_id,))
        users = self.cursor.fetchall()
        print("Users you are following:")
        for user in users:
            print(user[0])
        self.cursor.execute("SELECT topicName FROM FollowsTopic ft "
                            "INNER JOIN Topics t ON ft.topicId = t.topicID "
                            "WHERE ft.userID = %s", (self.current_user_id,))
        topics = self.cursor.fetchall()
        print("Topics you are following:")
        for topic in topics:
            print(topic[0])

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

    def do_unfollow(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        temp = input("Unfollow user or unfollow topic? \n")
        if temp == 'user':
            username = input("Input the user name: ")
            self.cursor.execute("SELECT userID FROM Users WHERE alias = %s;", (username,))
            result = self.cursor.fetchone()
            if not result:
                print("User not found")
                return
            self.cursor.execute("SELECT userID FROM FollowsUser WHERE userID = %s and targetUserID = %s;",
                                (self.current_user_id, result[0]))
            result1 = self.cursor.fetchone()
            if not result1:
                print("User not followed yet")
                return
            self.cursor.execute("DELETE FROM FollowsUser WHERE userID = %s and targetUserID = %s;",
                                (self.current_user_id, result[0]))
            self.cnx.commit()
            print("User %s unfollowed." % username)
        elif temp == 'topic':
            topicname = input("Input the topic name: ")
            self.cursor.execute("SELECT topicID FROM Topics WHERE topicName = %s;", (topicname,))
            result = self.cursor.fetchone()
            if not result:
                print("Topic not found")
                return
            self.cursor.execute("SELECT userID FROM FollowsTopic WHERE userID = %s and topicID = %s;",
                                (self.current_user_id, result[0]))
            result1 = self.cursor.fetchone()
            if not result1:
                print("Topic not followed yet")
                return
            self.cursor.execute("DELETE FROM FollowsTopic WHERE userID = %s and topicID = %s;",
                                (self.current_user_id, result[0]))
            self.cnx.commit()
            print("Topic %s unfollowed." % topicname)
        else:
            print("Wrong answer pick user or topic!!!")
            return

    def do_get_my_groups(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        self.cursor.execute("SELECT groupName, role FROM UserGroups ug INNER JOIN Members m ON ug.groupID = m.groupID "
                            "WHERE userID = %s", (self.current_user_id,))
        results = self.cursor.fetchall()
        if not results:
            print("You are not in any groups.")
            return
        print("Your groups:")
        for result in results:
            print("You are a(n) %s in %s" % (result[1], result[0]))

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
        print("Create successful! Group name = %s" % groupname)


    def do_join_group(self, arg):
        if not self.current_user_id:
            print("Please log in first")
            return
        groupname = input("Please enter the group name: ")
        # check if the user is creator of the group, it he is, block this action
        self.cursor.execute("SELECT creatorID FROM UserGroups WHERE groupName = %s and creatorID = %s;",
                            (groupname, self.current_user_id))
        temp = self.cursor.fetchone()
        if temp:
            print("You are the creator. Illegal action blocked!")
            return
        # check role. It mustn't be creator
        rolecheck = 0
        while rolecheck == 0:
            role = input("Please enter role: ")
            if rolecheck != "Creator":
                rolecheck = 1
            else:
                print("Your role can't be creator. Please change.")
        self.cursor.execute("SELECT groupID FROM UserGroups WHERE groupName = %s;", (groupname,))
        result = self.cursor.fetchone()
        if not result:
            print("Sorry, group not found")
            return
        if role:
            self.cursor.execute("INSERT IGNORE INTO Members (groupID, userID, role) VALUES (%s, %s, %s);",
                                (result[0], self.current_user_id, role))
        else:
            self.cursor.execute("INSERT IGNORE INTO Members (groupID, userID) VALUES (%s, %s);",
                                (result[0], self.current_user_id))
        self.cnx.commit()
        print("Join successful! Group name = %s" % groupname)


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
        # delete rows in member table
        self.cursor.execute("DELETE FROM Members WHERE groupID = %s;", (result[1],))
        # delete row in usergroup table
        self.cursor.execute("DELETE FROM UserGroups WHERE groupID = %s;", (result[1],))

        self.cnx.commit()
        print("Delete successful! Group name = %s" % groupname)


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
        self.cursor.execute("SELECT userID FROM Members WHERE groupID = %s and userID = %s;",
                            (result[1], self.current_user_id))
        result1 = self.cursor.fetchone()
        if not result1:
            print("Sorry, you are not in this group!")
            return
        # delete row in member table
        self.cursor.execute("DELETE FROM Members WHERE groupID = %s and userID = %s;",
                            (result[1], self.current_user_id))
        self.cnx.commit()
        print("Quit successful! Group name = %s" % groupname)


if __name__ == '__main__':
    Client().cmdloop()



