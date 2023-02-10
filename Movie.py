import requests


class Movie:
    __base_url = "https://api.themoviedb.org/3/movie/"
    __api_key = "d8e12eff606e3ce0127689cb127f5641"

    def get_now_playing(self) -> None:
        print("Now Playing: ")
        response = requests.get(f"{self.__base_url}now_playing?api_key={self.__api_key}")
        response = response.json()
        for i in range(len(response['results'])):
            print(f"{i + 1}) {response['results'][i]['title']}")

    def now_playing_list(self) -> list:
        now_playing_movie_titles = []
        response = requests.get(f"{self.__base_url}now_playing?api_key={self.__api_key}")
        response = response.json()
        for i in range(len(response['results'])):
            now_playing_movie_titles.append(response['results'][i]['title'])
        return now_playing_movie_titles

    @staticmethod
    def __get_movie_id(title) -> int:
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key=d8e12eff606e3ce0127689cb127f5641&query={title}")
        response = response.json()
        return response['results'][0]['id']

    def get_movie_details(self, title) -> None:
        movie_id = self.__get_movie_id(title)
        movie_info = requests.get(f"https://api.themoviedb.org/3/movie/{str(movie_id)}?api_key={self.__api_key}")
        movie_cast = requests.get(f"https://api.themoviedb.org/3/movie/"
                                  f"{str(movie_id)}/credits?api_key={self.__api_key}")
        movie_info = movie_info.json()
        movie_cast = movie_cast.json()
        movie_cast = sorted(movie_cast['cast'], key=lambda x: x['popularity'], reverse=True)
        print()
        print(movie_info['title'])
        if movie_info['overview'] != "":
            print(movie_info["overview"])
        if movie_info['runtime'] != 0:
            print(f"Runtime: {movie_info['runtime']}")
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
