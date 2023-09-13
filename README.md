# web-stuff
To run the webserver, run:
```
poetry install
```

```
poetry run python -m website [host]
```

Note for local testing you should use `localhost` for `[host]`. The website should be available at port 9003 of the given host.

Not working? Alternative flavours include using `python -m poetry` or `py -m poetry` instead of `poetry`, or spawning `poetry shell` and running `python -m website [host]` inside that shell. You may also need to run `poetry install` again, if there are any new dependencies.

For installing dependencies, use `poetry add <thing>`, which will pip install it into poetry, but also update poetry's internal knowledge of "what do I have installed".

If anything breaks or starts acting funny, ping andrew about it, it's his problem.



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