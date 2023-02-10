import os
import psycopg2


class MovieHall:
    __hall = []
    __rows = -1
    __seats = -1

    __conn = psycopg2.connect(host=os.environ['DATABASE_URL'], database=os.environ['PYTHON_PROJECT_USERNAME'],
                              password=os.environ['PASSWORD'],
                              user=os.environ['PYTHON_PROJECT_USERNAME'])

    __cursor = __conn.cursor()

    def string_to_hall(self, string_hall) -> list:
        temp = [string_hall[idx: idx + 20] for idx in range(0, len(string_hall), 20)]
        res = list(map(lambda ele: list(map(int, ele)), temp))
        self.__rows = len(res)
        self.__seats = 20
        self.__hall = res
        return res

    def __validate_hall_input(self):
        row = ""
        seat = ""
        while row == "":
            row = input(f"Enter a row number (between 1 and {self.__rows}): ")
            if row == "quit":
                return False, False
            elif row.isnumeric() is False:
                print("Error: Non-numeric input. Try again...")
                row = ""
            elif int(row) < 0 or int(row) > self.__rows:
                print("Error: Invalid row. Try again...")
                row = ""
        while seat == "":
            seat = input(f"Enter a seat number (between 1 and {self.__seats}): ")
            if seat == "quit":
                return False, False
            elif seat.isnumeric() is False:
                print("Error: Non-numeric input. Try again...")
                seat = ""
            elif int(seat) < 0 or int(seat) > self.__seats:
                print("Error: Invalid seat. Try again...")
                seat = ""
        return int(row), int(seat)

    def hall_to_string(self) -> str:
        string_hall = [[str(ele) for ele in sub] for sub in self.__hall]
        flat_list = [item for sublist in string_hall for item in sublist]
        flat_list = "".join(flat_list)
        return flat_list

    def print_hall(self) -> None:
        print("FREE SEATS - 0\n TAKEN SEATS - 1\n")
        for row in self.__hall:
            print(*row)

    def buy_ticket(self) -> bool:
        print("----------------CHOOSE SEAT----------------")
        print("To cancel the operation, type 'quit'")
        self.print_hall()
        row, seat = self.__validate_hall_input()
        if row is False or seat is False:
            print("Process has been canceled...")
            return False
        if self.__hall[row - 1][seat - 1] == 1:
            print("This seat is already booked.")
        else:
            print("This seat is empty.")
            print("Buying seat...")
            self.__hall[row - 1][seat - 1] = 1
            print("We have now bought this seat for you.")

    def count_free_seats(self) -> None:
        free_seats = 0
        for row in self.__hall:
            free_seats += row.count(0)
        if free_seats > 0:
            print(f"There are {free_seats} free seats available")
        else:
            print("There are no free seats available")
