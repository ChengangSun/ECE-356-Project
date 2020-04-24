import cmd
import datetime
import mysql.connector

cnx = mysql.connector.connect(
            host="18.234.70.125",
            database="social_network",
            user="SCG",
            password="scg199821")
cursor = cnx.cursor()

class Client(cmd.Cmd):
    intro = 'Welcome to our social Network app.   Type help or ? to list commands.\n'
    prompt = '(social network client)'

    def __init__(self):
        super(Client, self).__init__()
        self.current_user_id = None

    def do_signUp(self, arg):
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
            birthday = datetime.datetime.now()
            data = (username, email, gender, password, birthday, occupation)
            print(birthday)
            cursor.execute("""INSERT INTO Users VALUES(null,%s,%s,%s,%s,%s,now(),%s""", data)
            self.current_user_id = cursor.execute("""SELECT LAST_INSERT_ID();""")

if __name__ == '__main__':
    Client().cmdloop()



