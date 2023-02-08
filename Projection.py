import os
import re
import psycopg2
from Movie import Movie
from tabulate import tabulate


class Projection:
    DATE_VALIDATION = "^(\\d{4})-(0[1-9]|1[0-2]|[1-9])-([1-9]|0[1-9]|[1-2]\\d|3[0-1])$"
    TIME_VALIDATION = "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
    PRICE_VALIDATION = "^\\d+(\\.\\d{1,2})?$"

    __conn = psycopg2.connect(host=os.environ['DATABASE_URL'], database=os.environ['PYTHON_PROJECT_USERNAME'],
                              password=os.environ['PASSWORD'],
                              user=os.environ['PYTHON_PROJECT_USERNAME'])

    __cursor = __conn.cursor()

    def __validate_projection_input(self):
        print("----------------MOVIE----------------")
        chosen_movie = 0
        hall_number = 0
        desired_date = ""
        desired_time = ""
        hall_representation = ""
        ticket_price = 0.00

        movie = Movie()
        movie.get_now_playing()

        while int(chosen_movie) < 1 or int(chosen_movie) > 20:
            chosen_movie = input("Enter the corresponding number of the movie: ")
            if chosen_movie == "quit":
                print("Process has been canceled...")
                return -1
            elif int(chosen_movie) < 1 or int(chosen_movie) > 20:
                print("Error: Chosen number is out of range. Try again...")
            elif chosen_movie.isnumeric() is False and chosen_movie != "quit":
                print("Error: Non-numeric input. Try again...")
        chosen_movie = movie.now_playing_list()[int(chosen_movie) - 1]

        print("----------------DATE AND TIME----------------")

        while desired_date == "":
            desired_date = input(""""Enter the desired date in format YYYY-MM-DD: """)
            if desired_date == "quit":
                print("Process has been canceled...")
                return -1
            if not re.match(self.DATE_VALIDATION, desired_date):
                print("Invalid date. Try again...")
                desired_date = ""

        while desired_time == "":
            desired_time = input("Enter the desired time in the format HH:MM: ")
            if desired_time == "quit":
                return -1
            if not re.match(self.TIME_VALIDATION, desired_time):
                print("Error: Invalid time")
                desired_time = ""

        print("----------------MOVIE HALL----------------")
        print("Note:\n1) Hall 1 (80 places)\n2) Hall 2 (100 places)\n3) Hall 3 (120 places)\n4) Hall 4 (200 places)")
        self.__cursor.execute("""SELECT HALL_ID FROM PROJECTION WHERE PROJECTION_DATE = %s 
                                        AND PROJECTION_TIME = %s""", [desired_date, desired_time])
        taken_halls = self.__cursor.fetchall()
        all_halls = {1, 2, 3, 4}
        if taken_halls:
            for hall in taken_halls:
                all_halls.remove(hall[0])
        if len(all_halls) == 0:
            print("All halls are occupied...")
            return -1
        else:
            print("Available halls for this date and time:")
            for hall in all_halls:
                print(f"Hall {hall}")

        while hall_number == 0:
            hall_number = input("Enter the corresponding number of the hall: ")
            if hall_number == "quit":
                print("Process has been canceled...")
                return -1
            elif int(hall_number) not in all_halls:
                print("Error: Chosen number is out of range. Try again...")
                hall_number = 0
            elif hall_number.isdigit() is False and hall_number != "quit":
                print("Error: Wrong input. Try again...")
                hall_number = 0
        hall_number = int(hall_number)

        # Hall representation as string
        row = "00000000000000000000"
        if hall_number == 1:
            for i in range(0, 4):
                hall_representation += row
        elif hall_number == 2:
            for i in range(0, 5):
                hall_representation += row
        elif hall_number == 3:
            for i in range(0, 6):
                hall_representation += row
        else:
            for i in range(0, 10):
                hall_representation += row

        print("----------------TICKET PRICE----------------")
        while ticket_price == 0.00:
            ticket_price = input("Enter the ticket price: ")
            if ticket_price == "quit":
                print("Process has been canceled...")
                return -1
            if not re.match(self.PRICE_VALIDATION, ticket_price):
                print("Error: Invalid price format. Try again...")
                ticket_price = 0.00
        ticket_price = float(ticket_price)
        return desired_date, desired_time, hall_number, chosen_movie, hall_representation, ticket_price

    def create_projection(self):
        print("----------------ADD PROJECTION----------------")
        print("To terminate the process, type 'quit'")
        projection = self.__validate_projection_input()
        if projection == -1:
            return
        else:
            self.__cursor.execute("""INSERT INTO PROJECTION(PROJECTION_DATE, PROJECTION_TIME, HALL_ID, MOVIE,
            HALL_REPRESENTATION, TAKEN_SEATS, TICKET_PRICE, TOTAL_REVENUE) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)""", [projection[0], projection[1], projection[2], projection[3],
                                                  projection[4], 0, projection[5], 0.00])
            self.__conn.commit()
            print("Successfully added projection...")

    def edit_projection_time(self):
        pass

    def edit_projection_ticket_price(self):
        pass

    def projection_ids_to_list(self):
        self.__cursor.execute("""SELECT PROJECTION_ID FROM PROJECTION""")
        result = self.__cursor.fetchall()
        projection_ids = []
        for ids in result:
            projection_ids.append(ids[0])
        return projection_ids

    def __projections_to_list(self):
        self.__cursor.execute("""SELECT * FROM PROJECTION""")
        result = self.__cursor.fetchall()
        projections = []
        for _projection in result:
            projections.append(map(str, _projection))
        return projections

    def __view_projections_admin(self):
        projections = self.__projections_to_list()
        print(tabulate(projections, headers=["ID", "DATE", "TIME", "HALL ID", "MOVIE", "HALL",
                                             "TAKEN SEATS", "TICKET PRICE", "TOTAL"]))

    def delete_projection(self):
        print("----------------DELETE PROJECTION----------------")
        self.__view_projections_admin()
        ids = self.projection_ids_to_list()
        projection_id = ""
        while projection_id == "":
            projection_id = input("Enter the projection id of the desired movie: ")
            if projection_id == "quit":
                print("Process was cancelled...")
                return
            if projection_id.isnumeric() is False:
                print("Error:Non-numeric input. Try again...")
            if int(projection_id) not in ids:
                print("Invalid input. Try again...")
                projection_id = ""
        self.__cursor.execute("""DELETE FROM PROJECTION WHERE PROJECTION_ID = %s""", projection_id)
        self.__conn.commit()
        print("Successfully deleted projection")


if __name__ == '__main__':
    projection = Projection()
    projection.delete_projection()