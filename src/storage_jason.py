import json
from istorage import IStorage


class StorageJson(IStorage):

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def list_movies(self):
        """
                Returns a dictionary of dictionaries that
                contains the movies information in the database.

                The function loads the information from the JSON
                file and returns the data.

                For example, the function may return:
                {
                  "Titanic": [
                    9,
                    1999
                  ],
                  "..." [
                    ...
                  ],
                ]
                """

        with open(self.file_path, "r") as handle:
            movies = json.load(handle)
        return movies

    def add_movie(self, title, year, rating, poster):
        """
                Adds a movie to the movie database.
                Loads the information from the API database, add the movie to the JSON file,
                and saves it. The function doesn't need to validate the input.
                """

        movies = self.list_movies()
        movies.update({title: [rating, year, poster]})
        with open("../data/data.json", "w") as file_obj:
            json.dump(movies, file_obj, indent=4)
        print(f"Movie {title} successfully added")

    def delete_movie(self, title):
        """
                Deletes a movie from the movie database.
                Loads the information from the JSON file, deletes the movie,
                and saves it. The function doesn't need to validate the input.
                """

        movies = self.list_movies()
        if title in movies:
            del movies[title]
            with open("../data/data.json", "w") as file_obj:
                json.dump(movies, file_obj, indent=4)
                print(f"""Movie "{title}" successfully deleted""")
        else:
            print(f"""Movie "{title}" doesn't exit""")

    def update_movie(self, title, rating):
        """
                Updates a movie from the movie database.
                Loads the information from the JSON file, updates the movie,
                and saves it. The function doesn't need to validate the input.
                """

        movies = self.list_movies()
        movies[title][0] = rating
        with open("../data/data.json", "w") as file_obj:
            json.dump(movies, file_obj, indent=4)
            print(f"""Movie "{title}" successfully updated""")
