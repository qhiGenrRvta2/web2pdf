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
    return flask.render_template('archiver.html') 


@app.route("/results", methods=["POST"])
def results():
    """
    Generate and deliver the results.
    """
    raise NotImplementedError
