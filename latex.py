from help_modules import generate_random_name
import os


def render(latex_code):
    filename = 'TEMP/' + generate_random_name()
    tex_file = filename + '.tex'
    pdf_file = filename + '.pdf'

    with open(tex_file, 'w') as f:
        f.write(latex_code)

    try:
        command = f'pdflatex -output-directory=TEMP {tex_file} > /dev/null'
        os.system(command)
    except:
        return None

    return pdf_file
