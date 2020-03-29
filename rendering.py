import string
import random
import os
from markdown import markdown
import pdfkit


def generate_random_name(size=120, alphabet=string.ascii_letters):
    return ''.join(random.choice(alphabet) for _ in range(size))


def render_markdown(code):
    filename = 'TEMP/' + generate_random_name() + '.pdf'

    try:
        html_text = markdown(code, output_format='html4')
        pdfkit.from_string(html_text, filename)
    except:
        return None

    return filename


def render_latex(code):
    filename = 'TEMP/' + generate_random_name()
    tex_file = filename + '.tex'
    pdf_file = filename + '.pdf'

    with open(tex_file, 'w') as f:
        f.write(code)

    try:
        command = f'pdflatex -output-directory=TEMP {tex_file} > /dev/null'
        os.system(command)
    except:
        return None

    return pdf_file
