"""This module contains functions for converting LaTeX and Markdown files"""

import string
import random
import os
from markdown import markdown
import pdfkit


def try_create_tempdir():
    os.makedirs(os.getcwd() + "/TEMP", exist_ok=True)


def generate_random_name(size=120, alphabet=string.ascii_letters):
    """This fuction generates a random name from file. The length and alphabet can be changed"""
    return ''.join(random.choice(alphabet) for _ in range(size))


def render_markdown(code):
    """Returns path to generated PDF or None"""
    filename = 'TEMP/' + generate_random_name() + '.pdf'

    try:
        try_create_tempdir()
        html_text = markdown(code, output_format='html4')
        pdfkit.from_string(html_text, filename)
    except Exception:
        return None

    return filename


def render_latex(code):
    """Returns path to generated PDF or None"""
    filename = 'TEMP/' + generate_random_name()
    tex_file_path = filename + '.tex'
    pdf_file_path = filename + '.pdf'

    try_create_tempdir()

    with open(tex_file_path, 'w') as tex_file:
        tex_file.write(code)

    try:
        command = f'pdflatex -output-directory=TEMP {tex_file_path} > /dev/null'
        os.system(command)
    except Exception:
        return None

    return pdf_file_path
