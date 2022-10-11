def get_min_and_max_value():
    string = input('>> ')
    if not all([st.isdigit() for st in string.split()]):
        print('Ошибка: Неверный тип значений.\n(Ожидаются цифры).')
        return get_min_and_max_value()
    try:
        min_p, max_p = string.split()
    except Exception:
        print('Ошибка: Неверное количество значений.\n(Ожидается два).')
        return get_min_and_max_value()
    return int(min_p), int(max_p)


print(get_min_and_max_value())
