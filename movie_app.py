from fuzzywuzzy import fuzz, process
import matplotlib.pyplot as plt
import random
from storage_json import StorageJson


class MovieApp:
    def __init__(self, storage=StorageJson(file_path='data_movies.json')):
        self._storage = storage

    def _command_list_movies(self):
        # Display list of movies from directory (choice 1)
        movies = self._storage.list_movies()  # call function form storage_json file
        for movie, details in movies.items():
            print(f"{movie}:")
            for key, value in details.items():
                print(f"{key}: {value}")
            print()

        print(f"{len(movies)} total movies.")

        input("Press Enter to continue")

    def _command_add_movie(self):
        # Add new movie to directory (choice 2)
        title = input("Enter a movie title: ")
        movies = self._storage.list_movies()
        if title in movies:
            print("The movie exist.")
        else:
            response = self._storage.add_movie(title)
            if response == "False":
                print(response)
            else:
                pass

        input("Press Enter to continue")

    def _command_delete_movie(self):
        # Delete movie from dictionary (choice 3)
        title = input("Enter a movie title to delete: ")
        if title in self._storage.data_movies:
            self._storage.delete_movie(title)
            print(f"The movie {title} was successfully deleted.")
        else:
            print("The movie doesn't exist.")

        input("Press Enter to continue")

    def _command_update_movie(self):
        # Update movie (choice 4)
        title = input("Enter a movie title: ")
        notes = input("Enter a note: ")
        self._storage.update_movie(title, notes)
        print("The note was successfully added.")
        input("Press Enter to continue")

    def _command_movie_stats(self):
        # Statistics (Average rating, Median rating, Best movie, Worst movie) (choice 5)
        data_movies = self._storage.load_movies()
        # Extract all movie ratings from load_data dictionary and stores them in a list movie_rating
        movie_ratings = [float(movie_data['rating']) for movie_data in data_movies.values()]
        # calculating total number of ratings
        len_of_movies_ratings = len(movie_ratings)

        # Average rating
        # calculating all ratings using sum() function
        sum_of_ratings = sum(movie_ratings)
        # calculating average rating - the sum of rating is divides by total number od movies
        average_rating = sum_of_ratings / len_of_movies_ratings
        print(f"Average rating: {average_rating:.2f}")

        # Median rating
        # Sorting of rating using sort() function
        movie_ratings.sort()
        # checking if length of the list is even or odd
        if len_of_movies_ratings % 2 == 0:
            median_rating = (movie_ratings[len_of_movies_ratings // 2] +
                             movie_ratings[len_of_movies_ratings // 2 - 1]) / 2
        else:
            median_rating = movie_ratings[len_of_movies_ratings // 2]
        print(f"Median rating: {median_rating:.2f}")

        # Best Movie
        # Finding the highest rating using max() function
        best_rating = max(movie_ratings)
        """
        Iterating over the load_data dictionary to find the movie(s) 
        with that rating and stores their names in the list best_movies.
        """
        best_movies = [movie_name for movie_name, movie_data in data_movies.items() if
                       float(movie_data['rating']) == best_rating]
        for movie_name in best_movies:
            print(f"Best movie: {movie_name}, Rating: {best_rating:.2f}")

        # Worst movie
        # Finding the lowest rating using min() function
        worst_rating = min(movie_ratings)
        """
        Iterating over the load_data dictionary to find the movie(s) with that 
        rating and stores their names in the list worst_movies.
        """
        worst_movies = [movie_name for movie_name, movie_data in data_movies.items() if
                        float(movie_data['rating']) == worst_rating]
        for movie_name in worst_movies:
            print(f"Worst movie: {movie_name}, Rating: {worst_rating:.2f}")

        input("Press Enter to continue")

    def _command_random_movie(self):
        # Random movie (choice 6)
        data_movies = self._storage.load_movies()

        movie, movie_data = random.choice(list(data_movies.items()))
        rating = movie_data['rating']
        print(f"Your movie for tonight: {movie}, it's rated {rating}.")

        input("Press Enter to continue")

    def _command_search_movie(self):
        # Search movie (choice 7)
        data_movies = self._storage.load_movies()

        searched_movie = input("Enter a movie name: ")
        """
        A Boolean variable found is initialized as False 
        to keep track of whether a matching movie is found or not
        """
        found = False

        """
        Iterating over each key-value pair in the 
        load_data dictionary using a for loop
        """
        for movie, movie_data in data_movies.items():
            """
            Calculating a similarity ratio between the user's input 
            and the current movie name using fuzz.token_set_ratio() 
            function from the fuzzywuzzy library
            """
            ratio = fuzz.token_set_ratio(searched_movie.lower(), movie.lower())
            if ratio >= 60:
                print(f"{movie}: {movie_data['rating']}")
                found = True

        if not found:
            print(f"The movie {searched_movie} does not exist. Did you mean:")
            suggestions = process.extract(searched_movie, data_movies.keys(), limit=2)
            for suggestion in suggestions:
                print(suggestion[0])

        input("Press Enter to continue")

    def _command_sorted_movies_by_rating(self):
        # Movies sorted by rating (choice 8)
        data_movies = self._storage.load_movies()

        """
        Sorting the data_movies dictionary by rating value, using the sorted() function 
        and passing in the data_movies.items(). The key parameter is set to a lambda 
        function that extracts the rating value from each item and float is used 
        to convert it to a numeric value. The reverse parameter is set to True to 
        sort the movies in descending order.
        """
        sorted_ratings = sorted(data_movies.items(), key=lambda x: float(x[1]['rating']), reverse=True)

        """
        Iterating over each item in the sorted_ratings list, 
        unpacking it into move and data values
        """
        for movie, data in sorted_ratings:
            rating = data['rating']
            print(f"{movie}, rating: {rating}")

        input("Press Enter to continue")

    def _command_create_histogram(self):
        # Create histogram (choice 9)
        data_movies = self._storage.load_movies()

        movie_ratings = [float(movie_data['rating']) for movie_data in data_movies.values()]

        plt.hist(movie_ratings, bins=10)

        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        plt.title('Movie Rating Histogram')

        try:
            file_name = input("Enter the name of the file to save (including extension): ")
            plt.savefig(file_name)
            plt.show()
            print("The histogram was created successfully.")

        except ValueError:
            print("Please enter supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, "
                  "svg, svgz, tif, tiff, webp")

        input("Press Enter to continue")

    def _generate_website(self):
        # Generate website (choice 10)
        data_movies = self._storage.load_movies()

        # Load the template file
        template_path = "_static/index_template.html"

        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        # Replace placeholder with actual template_content
        title_placeholder = "__TEMPLATE_TITLE__"
        movie_grid_placeholder = "__TEMPLATE_MOVIE_GRID__"
        storage_name = input("Enter the storage_name: ")

        movie_list_items = ""
        for movie, movie_data in data_movies.items():
            year = movie_data['year']
            poster_url = movie_data.get("poster_url", 'No Poster Available')
            movie_list_items += f"<li>\n"
            movie_list_items += f"<img src='{poster_url}' alt='{movie} Poster' width ='300'>\n "
            movie_list_items += f"<h2>{movie}</h2>\n"
            movie_list_items += f"<p>Year: {year}</p>\n"
            movie_list_items += f"</li>\n"

        # Replace placeholder with actual content in the template
        website_content = template_content.replace(title_placeholder, f"{storage_name} Movie App")
        website_content = website_content.replace(movie_grid_placeholder, movie_list_items)

        # Write the website content to index.html
        with open(f"{storage_name}.html", "w") as file:
            file.write(website_content)

        print("Website was generated successfully.")

        input("Press Enter to continue")

    def run(self):
        while True:
            print("Menu")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Updated movie")
            print("5. Movie stats")
            print("6. Get a random movie recommendation")
            print("7. Search for a movie")
            print("8. Sort movies by rating")
            print("9. Create a histogram of movie ratings")
            print("10. Generate website")
            print("0. Exit")

            choice = input("Enter your choice (0-10):")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_movie_stats()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_sorted_movies_by_rating()
            elif choice == "9":
                self._command_create_histogram()
            elif choice == "10":
                self._generate_website()
            elif choice == "0":
                print("Bye!")
                break
