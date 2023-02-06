import getpass
import os
import re
import bcrypt
import psycopg2 as psycopg2
from User import User


class Authentication:
    EMAIL_VALIDATION = "^[\\w -.]+@([\\w-]+\\.)+[\\w-]{2,4}$"
    PASSWORD_VALIDATION = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!#%*?&]{6,20}$"
    NAME_VALIDATION = "^[A-z][a-z]+$"

    @staticmethod
    def __connect_to_db():
        conn = psycopg2.connect(host=os.environ['DATABASE_URL'], database=os.environ['PYTHON_PROJECT_USERNAME'],
                                password=os.environ['PASSWORD'],
                                user=os.environ['PYTHON_PROJECT_USERNAME'])
        return conn

    @staticmethod
    def create_tables():
        conn = psycopg2.connect(host=os.environ['DATABASE_URL'], database=os.environ['PYTHON_PROJECT_USERNAME'],
                                password=os.environ['PASSWORD'],
                                user=os.environ['PYTHON_PROJECT_USERNAME'])

        cursor = conn.cursor()
        cursor.execute("""DROP TABLE "user" CASCADE; """)
        cursor.execute("""DROP TABLE PROJECTION CASCADE; """)
        cursor.execute("""DROP TABLE PURCHASEHISTORY CASCADE; """)

        cursor.execute("""CREATE TABLE "user"(
                            EMAIL VARCHAR(35) NOT NULL PRIMARY KEY,
                            FIRSTNAME VARCHAR(30) NOT NULL,
                            LASTNAME VARCHAR(30) NOT NULL,
                            PASSWORD VARCHAR NOT NULL ,
                            ISADMIN BOOLEAN);
                        """)

        cursor.execute("""CREATE TABLE PROJECTION(
                       PROJECTIONID INT UNIQUE PRIMARY KEY,
                       DATE DATE,
                       TIME TIME,
                       MOVIE VARCHAR(50),
                       TOTALREVENUE DECIMAL(8,2));""")

        cursor.execute("""CREATE TABLE PURCHASEHISTORY(
                          PURCHASEDAT TIMESTAMP PRIMARY KEY,
                          PURCHASEDBY VARCHAR(50) REFERENCES "user"(EMAIL),
                          PROJECTION INT REFERENCES PROJECTION(PROJECTIONID),
                          PURCHASEDPLACES VARCHAR(200),
                          TOTAL DECIMAL(8,2));"""
                       )
        conn.commit()

    def __validate_registration_input(self):
        print("----------------REGISTER----------------")
        email = ""
        pwd = ""
        first_name = ""
        last_name = ""
        print("To cancel the operation, type 'quit'")
        while not re.match(self.EMAIL_VALIDATION, email):
            email = input("Enter email address: ")
            if email == "quit":
                return -1
            if not re.match(self.EMAIL_VALIDATION, email):
                print("Error: Invalid email. Try again...")
        conf_pwd = "2"
        while pwd != conf_pwd:
            print("Note: Password must contain:\nAt least 1 digit\nAt least one lowercase character\n"
                  "At least one uppercase character\nAt least one special character\nAt least 8 characters in length")
            while not re.match(self.PASSWORD_VALIDATION, pwd):
                pwd = getpass.getpass("Enter Password: ")
                if pwd == "quit":
                    return -1
                if not re.match(self.PASSWORD_VALIDATION, pwd):
                    print("Password doesn't satisfy requirements in Note. Try again...")
                    pwd = ""
            while not re.match(self.PASSWORD_VALIDATION, conf_pwd):
                conf_pwd = getpass.getpass("Confirm Password: ")
                if conf_pwd == "quit":
                    return -1
                if not re.match(self.PASSWORD_VALIDATION, conf_pwd):
                    print("Password doesn't satisfy requirements in Note. Try again...")
                    pwd = ""
                    conf_pwd = "2"
                    break
                if pwd != conf_pwd:
                    print("Passwords don't match. Try again...")
                    pwd = ""
                    conf_pwd = "2"
                    break
        while not re.match(self.NAME_VALIDATION, first_name):
            first_name = input("Enter First Name: ")
            if first_name == "quit":
                return -1
            if not re.match(self.NAME_VALIDATION, first_name):
                print("Error: Invalid First Name. Please enter only letters (2 minimum)...")
        while not re.match(self.NAME_VALIDATION, last_name):
            last_name = input("Enter Last Name: ")
            if last_name == "quit":
                return -1
            if not re.match(self.NAME_VALIDATION, last_name):
                print("Error: Invalid Last Name. Please enter only letters (2 minimum)...")
        return User(email, pwd, first_name, last_name, False)

    def register(self):
        user = self.__validate_registration_input()
        if user == -1:
            print("Registration process was canceled...")
        else:
            email = user.get_email()
            pwd = user.get_password()
            first_name = user.get_first_name()
            last_name = user.get_last_name()
            is_admin = user.get_isAdmin()

            conn = self.__connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""SELECT COUNT(1) FROM "user" WHERE EMAIL = %s""", [email])
            count = cursor.fetchone()[0]
            if count == 1:
                print("A registered user with this email exists...")
            else:
                pwd = bytes(pwd, "utf-8")
                hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
                hashed_pwd = str(hashed_pwd)
                cursor.execute("""
                INSERT INTO "user"(EMAIL, FIRSTNAME, LASTNAME, PASSWORD, ISADMIN)
                 VALUES (%s, %s, %s, %s, %s)
                """, [email, first_name, last_name, hashed_pwd, is_admin])
                conn.commit()
                print("Successfully registered...")
                return user

    def login(self):
        print("----------------LOGIN----------------")
        print("To cancel the operation, type 'quit'")
        email = ""
        while not re.match(self.EMAIL_VALIDATION, email):
            email = input("Enter email address: ")
            if email == "quit":
                return -1
            if not re.match(self.EMAIL_VALIDATION, email):
                print("Error: Invalid email. Try again...")
        pwd = getpass.getpass("Enter Password: ")
        if pwd == "quit":
            return -1
        pwd = bytes(pwd, "utf-8")

        conn = self.__connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(1), * FROM "user" WHERE EMAIL = %s GROUP BY EMAIL""", [email])
        result = cursor.fetchone()
        if result[0] == 0:
            print("There is no such user...")
        else:
            user_pwd = result[4]
            user_pwd = user_pwd[2:len(user_pwd) - 1]
            user_pwd = bytes(user_pwd, "utf-8")
            if bcrypt.checkpw(pwd, user_pwd):
                print("Logged in")
                return User(result[1], result[2], result[3], result[4], result[5])
            else:
                print("Incorrect password")


if __name__ == '__main__':
    test = Authentication()
    test.login()
