"""This module contains functions for converting LaTeX and Markdown files"""

import string
import random
import os
import multiprocessing
import time
from markdown import markdown
import pdfkit


MAX_WAIT_TIME = 3
POLLING_RATE = 10


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


def __run_pdflatex(code, send_end):
    """Sets path to generated PDF or None"""
    filename = 'TEMP/' + generate_random_name()
    tex_file_path = filename + '.tex'

    try_create_tempdir()

    with open(tex_file_path, 'w') as tex_file:
        tex_file.write(code)

    try:
        command = f'pdflatex -output-directory=TEMP {tex_file_path} > /dev/null'
        os.system(command)
        send_end.send(filename + '.pdf')
    except Exception:
        send_end.send(None)


def render_latex(code):
    """Returns path to generated PDF or None"""
    pdf_file_path = None
    recv_end, send_end = multiprocessing.Pipe(False)
    proc = multiprocessing.Process(
        target=__run_pdflatex, args=(code, send_end))
    proc.start()

    for _ in range(POLLING_RATE * MAX_WAIT_TIME):
        if proc.is_alive():
            time.sleep(1 / POLLING_RATE)
        else:
            pdf_file_path = recv_end.recv()
            break

    if proc.is_alive():
        print('proc was killed')
        proc.terminate()
        proc.join()

    return pdf_file_path
