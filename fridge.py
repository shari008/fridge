import datetime
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'

goods = {
    'Пельмени Универсальные': [
        {'amount': Decimal('0.5'), 'expiration_date': datetime.date(2023, 7, 15)},
        {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 1)},
    ],
    'Вода': [
        {'amount': Decimal('1.5'), 'expiration_date': None}
    ],
}


def add(items, title, amount, expiration_date=None):
    if expiration_date is not None:
        expiration_date = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()

    batch = {'amount': amount, 'expiration_date': expiration_date}

    if title in items:
        items[title].append(batch)
    else:
        items[title] = [batch]


def add_by_note(items, note):
    parts = note.split(' ')
    last_part = parts[-1]

    try:
        datetime.datetime.strptime(last_part, DATE_FORMAT)
        expiration_date = last_part
        amount = Decimal(parts[-2])
        title_parts = parts[:-2]
    except ValueError:
        expiration_date = None
        amount = Decimal(last_part)
        title_parts = parts[:-1]

    title = ' '.join(title_parts)
    add(items, title, amount, expiration_date)


def find(items, needle):
    result = []
    needle = needle.lower()

    for title in items:
        if needle in title.lower():
            result.append(title)

    return result


def get_amount(items, needle):
    total = Decimal('0')
    found_titles = find(items, needle)

    for title in found_titles:
        for batch in items[title]:
            total = total + batch['amount']

    return total


def get_expired(items, in_advance_days=0):
    result = []
    today = datetime.date.today()
    last_date = today + datetime.timedelta(days=in_advance_days)

    for title in items:
        expired_amount = Decimal('0')

        for batch in items[title]:
            date = batch['expiration_date']
            if date is not None and date <= last_date:
                expired_amount = expired_amount + batch['amount']

        if expired_amount > 0:
            result.append((title, expired_amount))

    return result


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)
in_hundred_years = today + datetime.timedelta(days=36500)

fridge = {}

add(fridge, 'Молоко', Decimal('1'), str(yesterday))
add(fridge, 'Молоко', Decimal('2'), str(tomorrow))
add(fridge, 'Сыр', Decimal('0.3'), str(in_hundred_years))
add(fridge, 'Вода', Decimal('1.5'))
add(fridge, 'Вода', Decimal('2'), None)
print('add:', fridge)

add_by_note(fridge, 'Яйца Фабрики №1 4 ' + str(tomorrow))
add_by_note(fridge, 'Яйца Фабрики №1 10')
add_by_note(fridge, 'Хлеб 1 ' + str(yesterday))
add_by_note(fridge, 'Сыр 0.2')
print('add_by_note:', fridge['Яйца Фабрики №1'], fridge['Хлеб'], fridge['Сыр'])

print('find мол:', find(fridge, 'мол'))
print('find ВОД:', find(fridge, 'ВОД'))
print('find нет такого:', find(fridge, 'ананас'))

print('get_amount Вода:', get_amount(fridge, 'вода'))
print('get_amount Молоко:', get_amount(fridge, 'молоко'))
print('get_amount яйца:', get_amount(fridge, 'яйц'))
print('get_amount ананас:', get_amount(fridge, 'ананас'))

print('get_expired 0 дней:', get_expired(fridge))
print('get_expired 1 день:', get_expired(fridge, 1))
print('get_expired 40000 дней:', get_expired(fridge, 40000))
print('get_expired старый goods:', get_expired(goods))