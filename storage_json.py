import json
import requests
from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_movies = {}
        self.load_movies()

    def load_movies(self):
        """
        Loads the movies data from JSON file and return it as a dictionary.
        If the file doesn't exist or is empty, return an empty dictionary.
        """
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        for title, movie_data in data.items():
            # Fetch the update information from the API for each movie in the data
            api_url = f"http://www.omdbapi.com/?apikey=770a6d70&t={title}"
            response = requests.get(api_url)
            update_data = response.json()

            # Check if response is successful
            if update_data.get("Response") == "True":
                updated_movie_data = {
                    "rating": update_data.get("imdbRating"),
                    "year": update_data.get("Year"),
                    "poster_url": update_data.get("Poster")
                }
                data[title] = updated_movie_data

        self.data_movies = data
        return data

    def list_movies(self):
        total_movies = len(self.data_movies)
        if total_movies == 0:
            print("No movies found.")
        else:
            movies_dict = {}
            for title, movie_data in self.data_movies.items():
                movie_info = movie_data.copy()
                if 'poster_url' not in movie_info:
                    movie_info['poster_url'] = f"http://www.omdbapi.com/?apikey=770a6d70&t={title}"
                movies_dict[title] = movie_info
            return movies_dict

    def add_movie(self, title):
        url = f"http://www.omdbapi.com/?apikey=770a6d70&t={title}"
        response = requests.get(url)
        movie_data = response.json()

        if movie_data.get("Response") == "True":
            title = movie_data.get("Title")
            year = movie_data.get("Year")
            rating = movie_data.get("imdbRating")
            poster_url = movie_data.get("Poster")

            self.data_movies[title] = {
                "rating": rating,
                "year": year,
                "poster_url": poster_url
            }
            self._save_movies()
            print(f"Movie {title} successfully added.")
        else:
            print("Movie not found.")

    def delete_movie(self, title):
        if title in self.data_movies:
            del self.data_movies[title]
            self._save_movies()
            return f"Movie {title} successfully deleted."
        else:
            return f"The movie {title} does not exist."

    def update_movie(self, title, notes):
        if title in self.data_movies:
            self.data_movies[title]['notes'] = notes
            self._save_movies()
            return f"Notes for movie {title} successfully added."
        else:
            return f"The movie {title} does not exist."

    def _save_movies(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data_movies, file, indent=4)
