import requests
import pdfkit
from bs4 import BeautifulSoup as bs

# Useful references
# https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
# https://pypi.org/project/pdfkit/
# https://wkhtmltopdf.org/usage/wkhtmltopdf.txt

class Page():
    """
    """
    
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
    
    def __init__(self, url):
        """
        """
        self.url = url
        self.raw_data = self.retrieve_data()
        self.page_title = self.get_title()
        self.pdf_data = pdfkit.from_url(url, False, options=Page.options)

    def retrieve_data(self):
        """
        Get page text from a URL, and returns it (or "None" if something goes wrong).
        """
        try:
            data = requests.get(self.url)
        except requests.RequestException as e:
            print(f"retrieve_data(): there was a connection problem when trying to access {from_url}: {e}")
            return None

        if not data.ok:
            print(f"retrieve_data(): got an unexpected response from {from_url}")
            return None
        
        return data.text

    def get_title(self):
        """
        Gets the title of the webpage.
        """
        soup = bs(self.raw_data, 'html.parser')
        return soup.find('title').get_text()


def main():

    test = Page('https://en.wikipedia.org/wiki/Sodium')
    print(type(test.pdf_file))


if __name__ == "__main__":
    main()
