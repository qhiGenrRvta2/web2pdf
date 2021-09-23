import os
import random
import re
import string

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

def create_dir_for_session(session_uuid):
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
    url_regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
 
    chunks = raw_text.split()
    urls = [add_protocol(chunk) for chunk in chunks if re.match(url_regex, chunk)] 

    return urls
