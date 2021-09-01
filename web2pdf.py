import requests

import pdfkit

from bs4 import BeautifulSoup as bs

def retrieve_data(from_url):
    """Get page text from a URL, and returns it (or "None" if something goes wrong)."""
    
    try:
        data = requests.get(from_url)
    except requests.RequestException as e:
        print(f"retrieve_data(): there was a connection problem when trying to access {from_url}: {e}")
        return None

    if data.ok:
        return data.text
    else:
        print(f"retrieve_data(): got an unexpected response from {from_url}")
        return None

# https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
# https://pypi.org/project/pdfkit/
# https://wkhtmltopdf.org/usage/wkhtmltopdf.txt

# Options for pdfkit
options = {
    'quiet': '', # Silences pdfkit messages
    'print-media-type': '', # Request printable version
    'header-left': '[webpage]', # Put URL in header
    'header-right': '[isodate]', # Put date of printing in header
    'header-spacing': 5,    # Spacing between header and content
    'footer-center': '[page]',  # Page number in footer
    'footer-spacing': 5,    # Spacing between footer and content in mm
    'margin-top': 15,   # Top margin in mm
    'margin-bottom': 15, # Bottom margin in mm
}

test_url = 'https://en.wikipedia.org/wiki/Sodium'
data = retrieve_data(test_url)
soup = bs(data, 'html.parser')

page_title = soup.find('title').get_text()
print(page_title)

# Can replace output filename with 'False' to assign to a variable.
pdfkit.from_url(test_url, f'{page_title}.pdf', options=options)
