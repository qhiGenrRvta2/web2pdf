import os
import uuid

import flask

import helpers
import Page_archiver as p


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
    if 'uuid' not in flask.session:
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

        # Stop if nothing to do.
        if not urls:
            return flask.render_template('no_results.html')
            
        # Create session folder, and a list for storing results.
        session_folder = helpers.get_dir_for_session(flask.session['uuid'])
        
        # Generate an archive of each URL in the folder.
        # Identify any URLs which can't be archived. 
        bad_urls = []
        
        for url in urls:
            try:
                archive = p.Page_archiver(url)
                archive.create_file(session_folder, raw_prefix)
            except Exception as e:
                bad_urls.append(url)
                print(repr(e))

        # Identify outputs
        outputs = os.listdir(session_folder)

        if not outputs and not bad_urls:
            return flask.render_template('no_results.html')
       
        # Provide links to the archived files
        return flask.render_template('results.html', file_list=outputs, failures=bad_urls)


@app.route("/download/<filename>")
def download(filename):
    """
    Offer archived pages for download.
    """
    # https://tedboy.github.io/flask/generated/flask.send_from_directory.html
    session_folder = helpers.get_dir_for_session(flask.session['uuid'])
    try:
        return flask.send_from_directory(session_folder, filename, as_attachment=True)
    except FileNotFoundError:
        flask.abort(404)


@app.route("/make_zip")
def make_zip():
    """
    Create and send zip file containing all archived pages.
    """
    zip_folder = 'zips' 
    session_folder = helpers.get_dir_for_session(flask.session['uuid'])
    
    zip_file = helpers.make_zip(session_folder, zip_folder)
    
    return flask.send_from_directory(zip_folder, zip_file, as_attachment=True)
