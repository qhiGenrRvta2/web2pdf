import flask

app = flask.Flask(__name__)

# https://cs50.harvard.edu/college/2020/fall/notes/9/


@app.route("/")
def index():
    """
    Index page not implemented, redirect to the archiver.
    """
    return flask.redirect("/archiver", 303)


@app.route("/archiver")
def archiver():
    """
    Render a page for getting user input.
    """
    raise NotImplementedError


@app.route("/results")
def results():
    """
    Deliver the results.
    """
    raise NotImplementedError
