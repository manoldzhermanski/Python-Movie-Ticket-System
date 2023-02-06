import base64
import getpass
import os
import bcrypt
import re
import psycopg2 as psycopg2

EMAIL_VALIDATION = "^[\\w -.]+@([\\w-]+\\.)+[\\w-]{2,4}$"
PASSWORD_VALIDATION = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!#%*?&]{6,20}$"
NAME_VALIDATION = "^[A-z][a-z]+$"

def create_tables():
    conn = psycopg2.connect(host=os.environ['DATABASE_URL'], database=os.environ['PYTHON_PROJECT_USERNAME'],
                            password=os.environ['PASSWORD'],
                            user=os.environ['PYTHON_PROJECT_USERNAME'])

    cursor = conn.cursor()
    cursor.execute("""DROP TABLE "user" CASCADE """)
    cursor.execute("""DROP TABLE PROJECTION CASCADE """)
    cursor.execute("""DROP TABLE PURCHASEHISTORY CASCADE """)

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
    cursor.close()


def validate_registration_input():
    email = ""
    pwd = ""
    fstname = ""
    lstname = ""
    print("To cancel the operation, type 'quit'")
    while not re.match(EMAIL_VALIDATION, email):
        email = input("Enter email address: ")
        if email == "quit":
            return -1
        if not re.match(EMAIL_VALIDATION, email):
            print("Error: Invalid email. Try again...")
    conf_pwd = "2"
    while pwd != conf_pwd:
        print("Note: Password must contain:\nAt least 1 digit\nAt least one lowercase character\n"
              "At least one uppercase character\nAt least one special character\nAt least 8 characters in length")
        while not re.match(PASSWORD_VALIDATION, pwd):
            pwd = getpass.getpass("Enter Password: ")
            if pwd == "quit":
                return -1
            if not re.match(PASSWORD_VALIDATION, pwd):
                print("Password doesn't satisfy requirements in Note. Try again...")
                pwd = ""
        while not re.match(PASSWORD_VALIDATION, conf_pwd):
            conf_pwd = getpass.getpass("Confirm Password: ")
            if conf_pwd == "quit":
                return -1
            if not re.match(PASSWORD_VALIDATION, conf_pwd):
                print("Password doesn't satisfy requirements in Note. Try again...")
                pwd = ""
                conf_pwd = "2"
                break
            if pwd != conf_pwd:
                print("Passwords don't match. Try again...")
                pwd = ""
                conf_pwd = "2"
                break
    while not re.match(NAME_VALIDATION, fstname):
        fstname = input("Enter First Name: ")
        if fstname == "quit":
            return -1
        if not re.match(NAME_VALIDATION, fstname):
            print("Error: Invalid First Name. Please enter only letters...")
    while not re.match(NAME_VALIDATION, lstname):
        lstname = input("Enter Last Name: ")
        if lstname == "quit":
            return -1
        if not re.match(NAME_VALIDATION, lstname):
            print("Error: Invalid Last Name. Please enter only letters...")
    return email, pwd, fstname, lstname


def register():
    result = validate_registration_input()
    if result == -1:
        print("Registration process was canceled...")
    else:
        email = result[0]
        pwd = result[1]
        fstname = result[2]
        lstname = result[3]
        conn = psycopg2.connect(host=os.environ['DATABASE_URL'], database=os.environ['PYTHON_PROJECT_USERNAME'],
                                password=os.environ['PASSWORD'],
                                user=os.environ['PYTHON_PROJECT_USERNAME'])
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(1) FROM "user" WHERE email = %s""", [email])
        count = cursor.fetchone()[0]
        if count == 1:
            print("A registered user with this email exists...")
        else:
            print(pwd)
            pwd = bytes(pwd, "utf-8")
            print(pwd)
            hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
            print(hashed_pwd)
            print("{0}".format(hashed_pwd))
            hashed_pwd = str(hashed_pwd)
            cursor.execute("""
            INSERT INTO "user"(EMAIL, FIRSTNAME, LASTNAME, PASSWORD, ISADMIN)
             VALUES (%s, %s, %s, %s, FALSE)
            """, [email, fstname, lstname, hashed_pwd])
            conn.commit()
            cursor.close()
            print("Successfully registered...")


def login():
    print("To cancel the operation, type 'quit'")
    email = ""
    while not re.match(EMAIL_VALIDATION, email):
        email = input("Enter email address: ")
        if email == "quit":
            return -1
        if not re.match(EMAIL_VALIDATION, email):
            print("Error: Invalid email. Try again...")
    pwd = getpass.getpass("Enter Password: ")
    if pwd == "quit":
        return -1
    pwd = bytes(pwd, "utf-8")
    print(pwd)
    conn = psycopg2.connect(host=os.environ['DATABASE_URL'], database=os.environ['PYTHON_PROJECT_USERNAME'],
                            password=os.environ['PASSWORD'],
                            user=os.environ['PYTHON_PROJECT_USERNAME'])
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(1) FROM "user" WHERE EMAIL = %s""", [email])
    count = cursor.fetchone()[0]
    if count == 0:
        print("There is no such user...")
    else:
        cursor.execute("""SELECT PASSWORD FROM "user" WHERE EMAIL = %s""", [email])
        user_pwd = cursor.fetchone()[0]
        user_pwd = user_pwd[2:len(user_pwd)-1]
        print(user_pwd)
        user_pwd = bytes(user_pwd, "utf-8")
        if bcrypt.checkpw(pwd, user_pwd):
            cursor.execute("""SELECT * FROM "user" WHERE EMAIL = %s""", [email])
            result = cursor.fetchone()
            print("Logged in")
            return result
        else:
            print("Incorrect password")


"""
def signup():
    email = input("Enter email address: ")
    pwd = input("Enter password: ")
    conf_pwd = input("Confirm password: ")
    if conf_pwd == pwd:
        enc = conf_pwd.encode()
        hash1 = hashlib.md5(enc).hexdigest()
        with open("credentials.txt", "w") as f:
            f.write(email + "\n")
            f.write(hash1)
        f.close()
        print("You have registered successfully!")
    else:
        print("Password is not same as above! \n")

    def login():
        email = input("Enter email: ")
        pwd = input("Enter password: ")
        auth = pwd.encode()
        auth_hash = hashlib.md5(auth).hexdigest()
        with open("credentials.txt", "r") as f:
            stored_email, stored_pwd = f.read().split("\n")
        f.close()
        if email == stored_email and auth_hash == stored_pwd:
            print("Logged in Successfully!")
        else:
            print("Login failed! \n")

    while 1:
        print("********** Login System **********")
        print("1.Signup")
        print("2.Login")
        print("3.Exit")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            signup()
        elif ch == 2:
            login()
        elif ch == 3:
            break
        else:
            print("Wrong Choice!")
            """

if __name__ == '__main__':
    login()
