import csv
import pandas as pd
from csv import writer
from istorage import IStorage


class StorageCsv(IStorage):

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def list_movies(self):
        """
                Returns a dictionary of dictionaries that
                contains the movies information in the database.

                The function loads the information from the CSV
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

        with open(self.file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            data_list = []
            for row in csv_reader:
                data_list.append(row)
            movies = {}
            for data in data_list:
                movies.update({data['title']: [data['rating'], data['year'], data['poster']]})
        return movies

    def add_movie(self, title, year, rating, poster):
        """
                Adds a movie to the movie database.
                Loads the information from the API database, add the movie to the CSV file,
                and saves it. The function doesn't need to validate the input.
                """

        movie_attribute = [title, rating, year, poster]
        with open(self.file_path, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(movie_attribute)
            print(f"""Movie "{title}" successfully deleted""")
            f_object.close()

    def delete_movie(self, title):
        """
                Deletes a movie from the movie database.
                Loads the information from the JSON file, deletes the movie,
                and saves it. The function doesn't need to validate the input.
                """

        movies = self.list_movies()
        f_object = pd.read_csv(self.file_path, index_col='title')
        f_object = f_object.drop(title)
        f_object.to_csv(self.file_path, index=True)
        print(f"""Movie "{title}" doesn't exit""")

    def update_movie(self, title, rating):
        """
                Updates a movie from the movie database.
                Loads the information from the JSON file, updates the movie,
                and saves it. The function doesn't need to validate the input.
                """

        f_object = pd.read_csv(self.file_path, index_col="title")
        f_object.at[title, 'rating'] = rating
        f_object = f_object.reset_index()
        f_object.to_csv(self.file_path, index=False)
        print(f"""Movie "{title}" successfully updated""")
