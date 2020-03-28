from help_modules import generate_random_name
from markdown import markdown
import pdfkit


def render(md_code):
    filename = 'TEMP/' + generate_random_name() + '.pdf'

    try:
        html_text = markdown(md_code, output_format='html4')
        pdfkit.from_string(html_text, filename)
    except:
        return None

    return filename
