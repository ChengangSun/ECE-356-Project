import cmd
import datetime
import mysql.connector



class Client(cmd.Cmd):
    intro = 'Welcome to our social Network app.   Type help or ? to list commands.\n'
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
        else:
            username = input("User name(can't be enpty): ")
            password = input("Password(can't be enpty): ")
            email = input("Email: ")
            gender = input("Gender: ")
            occupation = input("Occupation: ")
            date_entry = input('Enter a date in YYYY-MM-DD format: ')
            year, month, day = map(int, date_entry.split('-'))
            birthday = datetime.date(year, month, day)
            data = (username, email, gender, password, occupation)
            print(birthday)
            ##cursor.execute("""INSERT INTO Users VALUES(null,%s,%s,%s,%s,now(),now(),%s""", data)
            ##self.current_user_id = cursor.execute("""SELECT LAST_INSERT_ID();""")

    def do_login(self, arg):
        if (self.current_user_id != None):
            print("Please log out first")
        else:
            username = input("User name(can't be enpty): ")
            password = input("Password(can't be enpty): ")
            self.cursor.execute("SELECT hash FROM Users WHERE alias = %s", (username,))
            realpassword = self.cursor.fetchone()
            if password == realpassword[0] and realpassword[0] != None:
                print("Login Succeed. Welcome, {}!".format(username))
                self.cursor.execute("SELECT userID FROM Users WHERE alias = %s", (username,))
                self.current_user_id = self.cursor.fetchone()[0]
                print("userid: ", self.current_user_id)
            else:
                print("Login Failed. Incorrect User/Password pair!!!")

    def do_logout(self, arg):
        if (self.current_user_id != None):
            print("You have been logged out!")
            self.current_user_id = None
        else:
            print("No one is logged in!")

if __name__ == '__main__':

    Client().cmdloop()



