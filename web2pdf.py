import pdfkit

# https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python
# https://pypi.org/project/pdfkit/
# https://wkhtmltopdf.org/usage/wkhtmltopdf.txt

# Options for pdfkit
options = {
    'quiet': '', # Silences pdfkit messages
    'print-media-type': '', # Request printable version
    'no-background': '', # Don't print background
    'header-left': '[webpage]', # Put URL in header
    'header-right': '[isodate]', # Put date of printing in header
    'header-spacing': 5,    # Spacing between header and content
    'footer-center': '[page]',  # Page number in footer
    'footer-spacing': 5,    # Spacing between footer and content in mm
    'margin-top': 15,   # Top margin in mm
    'margin-bottom': 15 # Bottom margin in mm
}

# Can replace output filename with 'False' to assign to a variable.
pdfkit.from_url('https://en.wikipedia.org/wiki/Bajadasaurus', 'out.pdf', options=options)
