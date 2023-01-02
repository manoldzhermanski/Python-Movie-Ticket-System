class MovieHall:
    __hall = []
    __rows = -1
    __seats = -1
    __hall_number = -1

    def __set_rows(self, rows):
        if rows <= 0:
            raise ValueError
        else:
            self.__rows = rows

    def get_rows(self):
        return self.__rows

    def del_rows(self):
        del self.__rows

    def __set_seats(self, seats):
        if seats <= 0:
            raise ValueError
        else:
            self.__seats = seats

    def get_seats(self):
        return self.__seats

    def del_seats(self):
        del self.__seats

    def __set_hall(self):
        for i in range(self.__rows):
            self.__hall.append([0] * self.__seats)

    def get_hall(self):
        return self.__hall

    def del_hall(self):
        for row in range(len(self.__hall)):
            self.__hall.pop()

    def __set_hall_number(self, hall_number):
        self.__hall_number = hall_number

    def get_hall_number(self):
        return self.__hall_number

    def __init__(self, rows, seats, hall_number):
        try:
            self.__set_rows(rows)
        except ValueError:
            print("Invalid row. Please enter a positive number")
            raise ValueError
        try:
            self.__set_seats(seats)
        except ValueError:
            print("Invalid seat. Please enter a positive number")
            raise ValueError
        self.__set_hall_number(hall_number)
        self.__set_hall()

    def __repr__(self):
        return f"Hall[{self.get_rows()}][{self.get_seats()}]"

    def print_hall(self):
        for row in self.__hall:
            print(*row)

    def buy_ticket(self):
        self.print_hall()
        booked = False
        while not booked:
            row = int(input(f"Enter a row number (between 1 and {self.__rows})"))
            if row < 0 or row > self.__rows:
                print("Error: Invalid row\n")
                continue
            seat = int(input(f"Enter a column number (between 1 and {self.__seats})"))
            if seat < 0 or seat > self.__seats:
                print("Invalid seat\n")
                continue
            if self.__hall[row - 1][seat - 1] == 1:
                print("This seat is already booked.")
            else:
                print("This seat is empty.")
                print("Booking seat...")
                self.__hall[row - 1][seat - 1] = 1
                print("We have now booked this seat for you.")
                booked = True

    def export_hall_info(self, file_path):
        print("Exporting hall information...")
        file = open(file_path, 'a')
        for row in self.__hall:
            for seat in row:
                file.write(str(seat) + ",")
            file.write("\n")
        print(f"Successfully exported information to {file_path}")

    def reset_hall(self):
        print("Resetting hall...")
        self.del_hall()
        self.__set_hall()
        print("All seats are available")

    def count_free_seats(self):
        free_seats = 0
        for row in self.__hall:
            free_seats += row.count(0)
        if free_seats > 0:
            print(f"There are {free_seats} free seats available")
        else:
            print("There are no free seats available")
