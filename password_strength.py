import re


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
        r'(?:[1-9]|0[1-9]|[1-2]\d|3[01])[\.\/-]?(?:[1-9]|0[1-9]|1[0-2])[\.\/-]?(?:[1-2]\d{3})',
        # phone numbers
        r'[78]?[?:(-]?9\d{2}[?:)-]?\d{3}-?\d{2}-?\d{2}',
        # license plate numbers
        # r''
    ]
    return any(re.match(pattern, password) for pattern in patterns)


def get_passwords_blacklist():
    return None


def get_password_strength(password):
    if not password:
        return 'Пароль не указан'

    # max_score = 10
    check_list = [1,
                  # has_normal_length(password),
                  # has_perfect_length(password),
                  # contains_numbers(password),
                  # contains_lowercase_letters(password),
                  # contains_uppercase_letters(password),
                  # contains_special_chars(password),
                  not mached_by_banned_patterns(password),
                  0,
                  0
                  ]
    # strength = round(sum(check_list) / len(check_list) * max_score)
    return sum(check_list)


if __name__ == '__main__':
    print('Введите пароль для проверки его силы:')
    password = input()
    print('Сила Вашего пароля по шкале от 1 до 10:')
    # print(get_password_strength(password))
    print(mached_by_banned_patterns(password))
