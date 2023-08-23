from website import main
import sys
import os

if (database_uri := os.environ.get("DATABASE_URI")) is None:
    database_uri = "sqlite:///"

if __name__ == "__main__":
    main(database_uri, sys.argv)
