""" Тут просто можно сгенерировать хэш пароля, чтобы скопировать и добавить в базу данных вручную. """

import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == '__main__':
    print(hash_password('1234'))