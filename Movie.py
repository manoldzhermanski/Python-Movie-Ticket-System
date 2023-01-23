import requests


class Movie:
    __base_url = "https://api.themoviedb.org/3/movie/"
    __api_key = "d8e12eff606e3ce0127689cb127f5641"

    def get_now_playing(self):
        print("Now Playing: ")
        response = requests.get(self.__base_url + "now_playing?api_key=" + self.__api_key)
        response = response.json()
        for i in range(len(response['results'])):
            print(f"{i + 1}) {response['results'][i]['title']}")

    @staticmethod
    def search_by_title(title):
        print("Search Results: ")
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie?api_key=d8e12eff606e3ce0127689cb127f5641&query=" + title)
        response = response.json()
        response = sorted(response['results'], key=lambda x: x['vote_count'], reverse=True)
        for i in range(len(response)):
            print(f"{i + 1}) {response[i]['title']}")

    @staticmethod
    def movie_titles_to_list(title):
        movie_titles = []
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie?api_key=d8e12eff606e3ce0127689cb127f5641&query=" + title)
        response = response.json()
        for i in range(len(response['results'])):
            movie_titles.append(response['results'][i]['title'])
        return movie_titles

    @staticmethod
    def __get_movie_id(title):
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie?api_key=d8e12eff606e3ce0127689cb127f5641&query=" + title)
        response = response.json()
        return response['results'][0]['id']

    def get_movie_details(self, title):
        movie_id = self.__get_movie_id(title)
        movie_info = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + self.__api_key)
        movie_cast = requests.get(" https://api.themoviedb.org/3/movie/" +
                                  str(id) + "/credits?api_key=" + self.__api_key)
        movie_info = movie_info.json()
        movie_cast = movie_cast.json()
        movie_cast = sorted(movie_cast['cast'], key=lambda x: x['popularity'], reverse=True)
        print()
        print(movie_info['title'])
        if movie_info['overview'] != "":
            print(movie_info["overview"])
        if movie_info['runtime'] != 0:
            print(movie_info['runtime'])
        cast = []
        for i in range(0, 5):
            cast.append(movie_cast[i]['name'])
        cast_string = ', '.join(cast)
        print(f"Cast: {cast_string}")
        genres = []
        for i in range(len(movie_info['genres'])):
            genres.append((movie_info['genres'][i]['name']))
        genres_string = ', '.join(genres)
        print(f"Genres: {genres_string}")
        print(f"Original language: {movie_info['original_language']}")


movie = Movie()
# movie.get_now_playing()
movie.search_by_title("Avatar")
movie.get_movie_details("Avatar 5")
