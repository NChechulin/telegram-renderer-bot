import string
import random


def generate_random_name():
    alph = string.ascii_letters + string.digits
    size = 120
    return ''.join(random.choice(alph) for _ in range(size))
