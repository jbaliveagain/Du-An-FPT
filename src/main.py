from movie_app import MovieApp
from storage_jason import StorageJson
from storage_csv import StorageCsv


def main():
    storage = StorageCsv("../data/data.csv")
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
