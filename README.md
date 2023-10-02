# web-stuff
This repo holds the website and main codebase for the Skill Issue team, completing DECO3801 in S2 2023.

## Setup
This project uses `poetry` for python dependency management. Poetry is available for install from [their website](https://python-poetry.org/).

Once poetry is installed, you should have a shell tool available on your system, invoked as `poetry`. This can also be used interchangeably with `python -m poetry` or `py -m poetry` depending on your installation & setup.

## Running
All commands should be run from the root folder of the repository.

To start the webserver, run this command:
```bash
poetry install && poetry run python -O -m website [host]
```

For local use, `[host]` should be either `localhost` or `127.0.0.1`. The website will be available at port 9003 of the provided host.

A dockerfile is also provided. This can be built and run instead of manually installing poetry, if so desired. 

### Database
To connect to a production database, the URI should be provided in the `DATABASE_URI` environment variable.

## Development
For development use, omit the `-O` flag from the above command. This will change several behaviours of the website, including much faster calendar updates and pre-filling the database with some dummy users. It will also 'unlock' the calendar endpoint, that is otherwise usually locked and only accessible from the hardware (raspberry pi) component.

### Structure
The project is structured with the code all living inside `website/`. The root folder stores build/dependency information.

Within `website/` sits the python files that make up the backend of the webserver. Important files are `__init__.py` for the main function; `admin.py` for the user-facing settings interface, `cal.py` for the calendar-file parsing, and `calendar.py` for the user-facing calendar display (only accessible from the custom hardware).

The remainder of the files for the website live in `website/templates/`. The `.html` files in `website/templates/` are the actual html content of the website, `website/templates/css/` contains the stylesheets and fonts, `website/templates/graphics/` contains the static images for the site, and `website/templates/js` contains the frontend javascript code responsible for live updates.

### Adding Dependencies
Dependencies should be added exclusively using `poetry add [thing]`. This will automatically update the `pyproject.toml` file, `poetry.lock` file, and use `pip` to install the library itself.


## Team-Specific:
Eli's notes for their set up:
1. Swap folders (Eli applicable only but be sure to be in the correct folder when doing the following)
```
cd .\web-stuff\
```
2. install poetry deps if haven't already
```
python -m pip install poetry
```
3. Poetry shell
```
python -m poetry shell
```
4. To run
```
python -m poetry run python -m website localhost
```

-------------------------
Ali's setup:
start: crtl shift `
1. cd .\web-stuff\ (don't need if in vs terminal)
2. py -m pip install poetry
3. py -m poetry install
4. py -m poetry shell
5. py -m poetry run python -m website localhost
end: ctrl `
