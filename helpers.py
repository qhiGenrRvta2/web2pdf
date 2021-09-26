import os
import random
import re
import string
import zipfile


def generate_key(size):
    """
    Generates a random secret key.
    """
    return ''.join(random.choice(string.ascii_letters) for x in range(size))


def add_protocol(chunk):
    """
    Adds http:// to the start of a URL if missing.
    """
    if chunk.startswith("http"):
        return chunk
    else:
        return r"http://" + chunk


def get_dir_for_session(session_uuid):
    """
    Creates a directory with a random name based on a UUID.
    """
    name = f"session_{session_uuid.fields[0]}"
    
    if not os.path.isdir(name):
        os.mkdir(name)

    return name


def generate_url_list(raw_text):
    """
    Turns raw input into a list of urls.
    """
    # Regex from https://www.geeksforgeeks.org/python-check-url-string/
    url_regex = re.compile(
        r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
 
    chunks = raw_text.split()
    urls = [add_protocol(chunk) for chunk in chunks if re.match(url_regex, chunk)] 

    return urls


def make_zip(input_folder, output_folder=zips):
    """
    Creates a zipped version of folder
    https://docs.python.org/3/library/zipfile.html
    """
    # check that output_folder exists and create it if needed.
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    files = os.listdir(input_folder)
    
    name = f"bundle_{folder}.zip"
    destination_file = os.path.join(output_folder, name)

    with zipfile.ZipFile(destination_file, "a") as output:
        for entry in files:
            output.write(entry)

    return name
