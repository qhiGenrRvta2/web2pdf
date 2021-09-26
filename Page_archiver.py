import os
import re

import pdfkit
import requests

from bs4 import BeautifulSoup as bs

# Useful references re. converting HTML to PDF
# https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
# https://pypi.org/project/pdfkit/
# https://wkhtmltopdf.org/usage/wkhtmltopdf.txt


class Page_archiver():
    """
    Takes a URL, retrieves its content, generates a PDF archive if appropriate.
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
        if self.is_binary:
            self.archive = self.raw_data
        else:
            self.archive = pdfkit.from_url(self.url, False, options=Page_archiver.options)

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
            self.is_binary = True
            return data.content

        self.is_binary = False
        return data.text

    def get_title(self):
        """
        Gets the title of the webpage.
        """
        if not self.is_binary:
            soup = bs(self.raw_data, 'html.parser')
            return soup.find('title').get_text()
        
        return os.path.basename(self.url)

    def create_file(self, tmp_directory=None, name_prefix=''):
        
        if not self.is_binary:
            name = name_prefix+self.page_title+'.pdf'
        else:
            name = self.page_title

        if tmp_directory:
            output_name = os.path.join(tmp_directory, name)
        else:
            output_name = name

        with open(output_name, "wb") as archive_file:
            archive_file.write(self.archive)
        
        return output_name


def main():

    test = Page_archiver('http://en.wikipedia.org/wiki/Sodium')
    test.create_file('tmp', 'Example - ')
    print(type(test.archive))


if __name__ == "__main__":
    main()
