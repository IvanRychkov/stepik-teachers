import random
import os

CSRF_PATH = 'csrf.token'


def generate_csrf():
    if os.path.exists(CSRF_PATH):
        print('using existing csrf token')
        with open(CSRF_PATH, 'r') as f:
            token = f.readline()
        return token
    else:
        with open(CSRF_PATH, 'w') as f:
            token = str(random.randbytes(256))
            f.write(token)
        print('csrf token generated')
        return token
