from Authentication import Authentication
from Movie import Movie

if __name__ == '__main__':
    authentication = Authentication()
    authentication.add_admin()
    movies = Movie()
    print("------------------Welcome to the Movie Booking System------------------")
    print("Please choose from the following options:")
    print("1.Register (type '-r')\n2.Login (type '-li')\n3.View Currently Played Movies (type '-c')\n"
          "4.Exit (type '-e')")
    command = ""
    while command != "-e":
        command = input("Enter a command: ")
        if command == "-r":
            user = authentication.register()
            if user == -1:
                pass
            else:
                pass
        elif command == '-li':
            user = authentication.login()
            if user == -1:
                pass
            else:
                if user.get_isAdmin():
                    print("1. Add Projection (type - ap)")
                else:
                    pass
        elif command == '-c':
            movies.get_now_playing()
        elif command == '-e':
            print("Goodbye :)")
        else:
            print("Error: Unknown command. Try again")
