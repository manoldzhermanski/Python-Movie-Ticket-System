from MovieHall import MovieHall

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        movie_hall = MovieHall(2, 5, 3)
    except ValueError:
        pass
    movie_hall.buy_ticket()
    movie_hall.buy_ticket()
    movie_hall.export_hall_info("C:\\Users\\PC\\PycharmProjects\\Movie Booking System\\output.txt")
    movie_hall.count_free_seats()
    movie_hall.reset_hall()
    movie_hall.count_free_seats()
    movie_hall.print_hall()
    movie_hall.export_hall_info("C:\\Users\\PC\\PycharmProjects\\Movie Booking System\\output.txt")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
