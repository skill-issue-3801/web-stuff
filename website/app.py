from flask import Flask, render_template

# In theory what static_folder="templates" does is whenever app
# looks for a static folder it looks under templates
app = Flask(__name__, static_folder="templates")


@app.route("/")
def home():
    return render_template("index.html")
