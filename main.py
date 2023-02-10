from Authentication import Authentication
from Movie import Movie
from Projection import Projection

if __name__ == '__main__':
    authentication = Authentication()
    movies = Movie()
    projection = Projection()
    command = ""
    is_logged_in = False
    while command != "-e":
        print("------------------Welcome to the Movie Booking System------------------")
        print("Please choose from the following options:")
        print("1.Register (type '-r')\n2.Login (type '-li')\n3.View Current Projections (type '-cp')\n"
              "4 View Available Seats (type -as)\n5.Exit (type '-e')")
        command = input("Enter a command: ")
        if command == "-r":
            user = authentication.register()
            if user is None:
                command = ""
                continue
            else:
                command = '-li'
                is_logged_in = True
        if command == '-li':
            if not is_logged_in:
                user = authentication.login()
                if user is None:
                    command = ""
                    continue
                else:
                    is_logged_in = True
            if is_logged_in:
                while command != "-lo":
                    if user.get_isAdmin():
                        print("----------------ADMIN MENU----------------")
                        print("1. Add Projection (type -ap)\n2. Edit ticket price (type -et)\n"
                              "3. Delete projection (type -dp)\n4. Show total revenue (type - tr)\n"
                              "5. View Current Projections (type '-cp')\n6. Buy ticket (type -bt)\n"
                              "7. View Available Seats (type -as)\n8. Log out (type -lo)")
                        command = input("Enter a command: ")
                    else:
                        print("----------------MENU----------------")
                        print("1. View Current Projections (type '-cp')\n2. Buy ticket (type -bt)\n"
                              "3. Log out (type -lo)\n4. View Available Seats (type -as)")
                        command = input("Enter a command: ")
                    if user.get_isAdmin() and command == '-ap':
                        if not projection.create_projection():
                            command = ""
                    elif user.get_isAdmin() and command == '-et':
                        if not projection.edit_projection_ticket_price():
                            command = ""
                    elif user.get_isAdmin() and command == '-dp':
                        if not projection.delete_projection():
                            command = ""
                    elif user.get_isAdmin() and command == '-tr':
                        projection.show_total_revenue()
                    elif command == '-cp':
                        projection.view_movie_details()
                    elif command == '-bt':
                        if not projection.buy_ticket():
                            command = ""
                    elif command == '-as':
                        if not projection.view_available_seats():
                            command = ""
                    elif command == '-lo':
                        print("Logging out")
                    else:
                        print("Invalid command...")
                        command = ""
        elif command == '-cp':
            projection.view_movie_details()
        elif command == '-as':
            if not projection.view_available_seats():
                command = ""
        elif command == '-e':
            print("Goodbye :)")
        else:
            print("Error: Unknown command. Try again")
