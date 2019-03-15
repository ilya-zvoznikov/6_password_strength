import getpass
import hashlib
import re
import requests
import sys


def has_normal_length(password):
    return len(password) > 8


def has_perfect_length(password):
    return len(password) > 15


def contains_numbers(password):
    return bool(re.search(r'\d', password))


def contains_lowercase_letters(password):
    return bool(re.search(r'[a-zа-я]', password))


def contains_uppercase_letters(password):
    return bool(re.search(r'[A-ZА-Я]', password))


def contains_special_chars(password):
    return bool(re.search(r'[\W]', password))


def mached_by_banned_patterns(password):
    patterns = [
        # dates
        r'(?:[1-9]|0[1-9]|[1-2]\d|3[01])[./-]?'
        r'(?:[1-9]|0[1-9]|1[0-2])[./-]?'
        r'(?:[1-2]\d{3})',
        # phone numbers
        r'[78]?[?:(-]?9\d{2}[?:)-]?\d{3}-?\d{2}-?\d{2}',
        # license plate numbers
        r'[AaBbCcEeHhKkMmOoPpTtXxАаВвЕеКкМмНнОоРрСсТтХх]\d{3}'
        r'[AaBbCcEeHhKkMmOoPpTtXxАаВвЕеКкМмНнОоРрСсТтХх]{2}(?:\d{2,3})?'
    ]
    return any(re.match(pattern, password) for pattern in patterns)


def is_diverse(password):
    return len(set(password)) > 6


def has_been_pwned_online(password):
    url = r'https://api.pwnedpasswords.com/range/{}'
    hash_obj = hashlib.sha1(password.encode('utf-8'))
    hash_str = hash_obj.hexdigest().upper()
    try:
        response = requests.get(url.format(hash_str[:5]))
        password_range = response.text
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout):
        return True

    return hash_str[5:] in password_range


def get_password_strength(password):
    if not password:
        return None

    # max_score = 10
    check_list = [
        1,
        has_normal_length(password),
        has_perfect_length(password),
        contains_numbers(password),
        contains_lowercase_letters(password),
        contains_uppercase_letters(password),
        contains_special_chars(password),
        not mached_by_banned_patterns(password),
        is_diverse(password),
        not has_been_pwned_online(password),
    ]

    return sum(check_list)


if __name__ == '__main__':
    print('Введите пароль для проверки его силы:')
    password = getpass.getpass()
    if not password:
        sys.exit('Пароль не указан')
    print('Сила Вашего пароля по шкале от 1 до 10:')
    print(get_password_strength(password))
