import statistics
import requests
import random
import operator
from requests.exceptions import ConnectionError


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self) -> None:
        movies = self._storage.list_movies()
        print(f"\nTHERE ARE {len(movies)} MOVIES FOR YOU TO CHOOSE")
        for name, attribute in movies.items():
            print(f"{name} ({attribute[1]}): {attribute[0]}")

    def _command_add_movies(self) -> None:
        movies = self._storage.list_movies()
        title = input("Enter new movie name: ")
        if title in movies:
            print(f"Movie {title} already exist!")
            return
        api_url = 'http://www.omdbapi.com/?apikey=b49eb448&t={}'.format(title)
        try:
            response = requests.get(api_url)
            if response.status_code == requests.codes.ok:
                title = response.json()["Title"]
                year = response.json()["Year"]
                rate = float(response.json()["imdbRating"])
                poster = response.json()["Poster"]
                self._storage.add_movie(title, year, rate, poster)
            else:
                print("Error:", response.status_code, response.text)
        except ConnectionError as e:
            print("No internet connection!")
        except KeyError:
            print(f"Movie {title} doesn't exit!")

    def _command_delete_movie(self) -> None:
        title = input("Enter movie name that you want to delete from your collection: ")
        self._storage.delete_movie(title)

    def _command_update_movie(self) -> None:
        movies = self._storage.list_movies()
        title = input("Enter movie name to update: ")
        if title in movies:
            rating = float(input("Enter new movie rating (0-10): "))
            self._storage.update_movie(title, rating)

    def _command_movie_stats(self):
        """
                Calculate the average, median, min, max of the movie rates. Prompt the result
                with the message.
                """
        movies = self._storage.list_movies()
        rate_list = []
        for movie in movies:
            rate_list.append(float(movies[movie][0]))
        print(f"Average rating: {statistics.mean(rate_list)}")
        print(f"Median rating: {statistics.median(rate_list)}")
        for movie, stat in movies.items():
            if stat[0] == max(rate_list):
                print(f"Best movie: {movie}, {stat[0]}")
            if stat[0] == min(rate_list):
                print(f"Worst movie: {movie}, {stat[0]}")

    def _command_random_movie(self):
        """
            Display a random movie from the json file to the user
            """
        movies = self._storage.list_movies()
        movie, stat = random.choice(list(movies.items()))
        print(f"Your movie for tonight: {movie}, it's rated {stat[0]}")

    def _command_search_movie(self):
        """
            Search movie base on user input. It will find the text that in the json file
            and display it.
            Example:
                - User: The
                - Result:
        The Shawshank Redemption (1994): 9.5
        The Godfather (1972): 9.2
        The Godfather: Part II (1974): 9.0
        The Dark Knight (2008): 9.0
        The Room (2003): 3.6
        """
        movies = self._storage.list_movies()
        user_search = input("Enter part of movie name: ")
        for movie, stat in movies.items():
            if user_search.lower() in movie.lower():
                print(f"{movie} ({stat[1]}): {stat[0]}")

    def _command_sorted_by_rating(self):
        """Sort all the movie from highest to lowest base on the rate value"""
        movies = self._storage.list_movies()
        sort = dict(sorted(movies.items(), key=operator.itemgetter(1), reverse=True)[:len(movies)])
        for movie, stat in sort.items():
            print(f"{movie} ({stat[1]}): {stat[0]}")

    def _command_generate_website(self):
        """
            This function will use the json file data to insert into html file with tag to create content
            for the website. Including movie title, year of production, rating and URL link to the poster of the movie
            """

        movies = self._storage.list_movies()
        print(movies)
        output = ""
        for movie, stat in movies.items():
            output += "<li>"
            output += "<div class='movie'>\n"
            output += f"<img class='movie-poster' src='{stat[2]}'\n>"
            output += f"<div class='movie-title'>{movie}</div>\n"
            output += f"<div class='movie-year'>{stat[1]}</dive>\n"
            output += "</div>\n"
            output += "</li>"
        with open("../res/index_template.html", "r") as html_file:
            html = html_file.read()
        with open("../res/index_template.html", "w") as html_file:
            html_file.write(html.replace("__TEMPLATE_MOVIE_GRID__", output))
            print("Website was generated successfully.")

    def run(self):
        while True:
            print("""
        ********** My Movies Database **********

        Menu:
        1. List movies
        2. Add movies
        3. Delete movie
        4. Update movie rate
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Generate website
        0. Exit program
        """)
            choice = int(input("Enter choice (0-9): "))
            if choice == 1:
                self._command_list_movies()
            if choice == 2:
                self._command_add_movies()
            if choice == 3:
                self._command_delete_movie()
            if choice == 4:
                self._command_update_movie()
            if choice == 5:
                self._command_movie_stats()
            if choice == 6:
                self._command_random_movie()
            if choice == 7:
                self._command_search_movie()
            if choice == 8:
                self._command_sorted_by_rating()
            if choice == 9:
                self._command_generate_website()
            elif choice == 0:
                print("Thanks for using! Bye!")
                exit()
