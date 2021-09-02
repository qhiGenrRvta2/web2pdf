import re
import requests
import pdfkit
from bs4 import BeautifulSoup as bs

# Useful references re. converting HTML to PDF
# https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
# https://pypi.org/project/pdfkit/
# https://wkhtmltopdf.org/usage/wkhtmltopdf.txt


class Page():
    """
    Takes a URL, retrieves its content, generates a PDF.
    """
    # CONSTANTS
    # Options for pdfkit
    options = {
        'quiet': '',                  # Silences pdfkit messages
        'print-media-type': '',       # Request printable version
        'header-left': '[webpage]',   # Put URL in header
        'header-right': '[isodate]',  # Put date of printing in header
        'header-spacing': 5,          # Spacing between header and content
        'footer-center': '[page]',    # Page number in footer
        'footer-spacing': 5,          # Spacing between footer and content in mm
        'margin-top': 15,             # Top margin in mm
        'margin-bottom': 15,          # Bottom margin in mm
    }
    
    def __init__(self, url):
        """
        Download data from URL
        Identify page title
        Generate PDF data
        """
        self.url = url
        self.raw_data = self.retrieve_data()
        self.page_title = self.get_title()
        self.pdf_data = pdfkit.from_url(self.url, False, options=Page.options)

    def retrieve_data(self):
        """
        Gets page text from a URL.
        https://docs.python-requests.org/en/master/user/quickstart/
        """
        # Get data.  Raises a requests.ConnectionError / requests.RequestException if something goes wrong. 
        data = requests.get(self.url)
        # Raise HTTPError if request not successful.
        data.raise_for_status()
     
        # Check that we got text.
        if not re.search(r'text', data.headers['content-type']):
            raise ValueError('Not an HTML file')

        return data.text

    def get_title(self):
        """
        Gets the title of the webpage.
        """
        soup = bs(self.raw_data, 'html.parser')
        return soup.find('title').get_text()


def main():

    test = Page('http://en.wikipedia.org/wiki/Sodium')
    print(type(test.pdf_data))


if __name__ == "__main__":
    main()
