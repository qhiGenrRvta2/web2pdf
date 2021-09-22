import re

def add_protocol(chunk):
    if chunk.startswith("http"):
        return chunk
    else:
        return r"http://" + chunk

def generate_url_list(raw_text):
    """
    Turns raw input into a list of urls.
    """
    # Regex from https://www.geeksforgeeks.org/python-check-url-string/
    url_regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
 
    chunks = raw_text.split()
    urls = [add_protocol(chunk) for chunk in chunks if re.match(url_regex, chunk)] 

    return urls
