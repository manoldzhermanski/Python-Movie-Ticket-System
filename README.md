Python Movie Ticket System
---
#### by Manol Dzhermanski

## Idea of the project
The idea of the project is to create a simple yet sophisticated console application
that simulates the purchase of tickets for movies. The integrated API allows for
creating projections with relevant movies and have information about them. With the
integrated PostgreSQL, changes are easily created and stored. There are 2 types of
profiles - admin and ordinary user. Each of them can perform a number of commands.
To perform a command, the user types it in the console.


## Used technologies
* APIs: [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction)
* Database: PostgreSQL

## Database tables
![](../../Pictures/Screenpresso/2023-02-10_15h08_16.png)
## Used libraries
* os
* re
* bcrypt
* getpass
* psycopg2
* tabulate

## Environment variables
* DATABASE_URL = hattie.db.elephantsql.com
* PASSWORD = QY1pLBecE6SeG3ExmWkSA5S9q6NkhxHJ
* PYTHON_PROJECT_USERNAME = nskgzyhp
* ADMIN_PASSWORD = Moncho12!

## Functionalities
### Admin functionalities
|   Functionality    | Description                                                                                                                                                                                                                                                                                                            |
|:------------------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   Add Projection   | The admin can choose one of the 20-th movie titles given by the API, choose date and time of the projection. With the given information it is checked in the database if there is an available hall from which the admin can choose. A ticket price is set and finally the created projection is added to the database |
| Edit ticket price  | The admin can choose a projection from the database and alter the price of the ticket (simulate a promotion)                                                                                                                                                                                                           |
| Delete projection  | The admin can delete a projection from the database                                                                                                                                                                                                                                                                    |
| Show total revenue | The admin can see the total earnings from all projections                                                                                                                                                                                                                                                              |

### User functionalities
|      Functionality       | Description                                                                                                                                                                                                                                                                                                 |
|:------------------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         Register         | A new user can be created and added to the database                                                                                                                                                                                                                                                         |
|          Log in          | A user can log in his profile, so he can perform some of the available commands                                                                                                                                                                                                                             |
| View Current Projections | The user can see all projections that are stored in the database. In addition, the user can choose if he wants to view  infromation about a movie [Y/N]. If the user wishes to see the details, with the help of the API, a plot summary, cast, duration, genres and language of the film will be displayed |
|       Buy ticket*        | The user can choose from the available projections. After that the seats will be displayed and he can choose a place. After the purchase is completed, the information in the database is updated                                                                                                           |
|   View Available Seats   | The user can see the available seats for a projection - 0 are for 'FREE' and 1 'TAKEN'                                                                                                                                                                                                                      |
|         Log out          | The user exits their profile                                                                                                                                                                                                                                                                                |

Note:

*Currently there is only one admin user in the database. His credentials are:
* email - moncho1@abv.bg
* password - Moncho12!
* 
** When running **main.py**, it's best to do it from a terminal rather than the play button.
**Pycharm has difficulties with the getpass library**

## How to run
1. Add the environment variables to your machine or IDE
2. Install the needed libraries
3. Run main.py