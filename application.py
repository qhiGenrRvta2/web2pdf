import uuid
import flask
import helpers
import Page_archiver


# https://cs50.harvard.edu/college/2020/fall/notes/9/

app = flask.Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Sessions.
# https://www.code-learner.com/how-to-use-session-and-cookie-in-python-flask-framework/
app.config['SECRET_KEY'] = helpers.generate_key(8)

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
    
    # Create a unique session ID.  Store it in flask.session (which works like a dict).
    # https://pythonbasics.org/flask-sessions/
    flask.session['uuid'] = uuid.uuid4()
    
    return flask.render_template('archiver.html') 


@app.route("/results", methods=["GET", "POST"])
def results():
    """
    Generate and deliver the results.
    """
    # If no form received: go back to start page.
    if flask.request.method == "GET":
        return flask.redirect("/archiver")

    if flask.request.method == "POST":
        
        # Get the raw data from the HTML form.
        raw_prefix = flask.request.form.get("prefix")
        raw_url_list = flask.request.form.get("url_box")
       
        # Get list of usable URLs.
        urls = helpers.generate_url_list(raw_url_list)

        if urls:
            destination = helpers.create_dir_for_session(flask.session['uuid'])
            # TODO: generate a PDF of each, and offer for download.
            print(urls)
            print(destination)
            print(f"At line 58: {flask.session['uuid']=}")
        
        raise NotImplementedError
