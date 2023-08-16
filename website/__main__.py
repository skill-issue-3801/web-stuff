import sys
import os

if (database_uri := os.environ.get("DATABASE_URI")) is None:
    database_uri = "sqlite:///"

def run(args):
    while True:
        pass

if __name__ == "__main__":
    run(sys.argv)
