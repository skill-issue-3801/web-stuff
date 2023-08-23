from flask import Flask


class DecoWebsite(Flask):
    def set_db_engine(self, db_engine):
        self.db = db_engine

app = DecoWebsite(__name__, static_folder=None)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
