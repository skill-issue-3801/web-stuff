import json
from flask import Flask


# In theory what static_folder="templates" does is whenever app
# looks for a static folder it looks under templates
app = Flask(__name__, static_folder="templates")


@app.route("/is_prod", methods=["POST"])
def foo():
    return json.dumps(not __debug__)
