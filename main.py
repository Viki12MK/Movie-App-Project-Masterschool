from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


def main():
    storage_type = input("Enter a choice of storage type ('json' or 'csv'): ")
    storage_name = input("Enter a name of storage: ")

    if storage_type == "json":
        storage = StorageJson(f'{storage_name}.json')
    elif storage_type == "csv":
        storage = StorageCsv(f'{storage_name}.csv')
    else:
        print("Invalid storage type.")
        return

    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
