import os
import random

env_var = 'SECRET_KEY'


def generate_secret_key():
    # Попробуем получить ключ из среды
    key = os.getenv(env_var)

    if key:
        print('secret key already exists')
        return key

    # Создадим ключ, если он не появился
    key = str(random.randbytes(256))
    os.environ[env_var] = key
    print('secret key generated')
    return key


if __name__ == '__main__':
    generate_secret_key()
