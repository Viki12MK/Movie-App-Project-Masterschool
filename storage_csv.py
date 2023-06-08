import csv
import requests
from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_movies = {}
        self.load_movies()

    def load_movies(self):
        """
        Loads the movies data from CSV file and return it as a dictionary.
        If the file doesn't exist or is empty, return an empty dictionary.
        """
        try:
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
        except (FileNotFoundError, csv.Error):
            data = []

        for movie_data in data:
            title = movie_data['title']
            rating = movie_data['rating']
            year = movie_data['year']
            poster_url = movie_data['poster_url']
            notes = movie_data['notes'] if 'notes' in movie_data else ''

            self.data_movies[title] = {
                'rating': rating,
                'year': year,
                'poster_url': poster_url,
                'notes': notes
            }

        return self.data_movies

    def list_movies(self):
        total_movies = len(self.data_movies)
        if total_movies == 0:
            return {}
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
                "poster_url": poster_url,
                "notes": ""
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
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'rating', 'year', 'poster_url', 'notes'])
            writer.writeheader()
            for title, movie_data in self.data_movies.items():
                writer.writerow({
                    'title': title,
                    'rating': movie_data['rating'],
                    'year': movie_data['year'],
                    'poster_url': movie_data['poster_url'],
                    'notes': movie_data['notes']
                })
