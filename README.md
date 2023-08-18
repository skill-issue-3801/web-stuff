# web-stuff
To run the webserver, run:
```
poetry install
```

```
poetry shell
```

```
python -m website [host]
```

Note for local testing you should use `localhost` for `[host]`. The website should be available at port 9003 of the given host.

Not working? try adding python -m wherever poetry is in above. 

Eli's notes for their set up:
1. Swap folders (Eli applicable only but be sure to be in the correct folder when doing the following)
```
cd .\web-stuff\
```
2. install poetry if haven't already
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