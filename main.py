import datetime as dt


class Record:
    # Давай принимать значение по умолчанию аргумента date как None
    # и явно проверять на None при присваивании.
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            # Немного сложно читать подобный код, когда ты отделяешь not и переменную в отдельных строчках,
            # давай перетащим их в таком порядке
            # if not date
            # else ***
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # Давай изучим новую конструкцию под названием generator expression
        # и применим ее в коде? https://www.johndcook.com/blog/2020/01/15/generator-expression/
        # Она упростит наш код и сделает его более лаконичным.
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Давай сохраним (today - record.date).days в отдельную переменную.
            # Также в питоне можно использовать конструкцию 0 <= x < 7 вместо 0 <= x and x < 7.
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Старайся давать переменным более осмысленные названия,
        # будущему поколению придется разбираться, что за переменная х.
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Можем обойтись здесь без условия else здесь, ибо мы всегда будем возвращать `Хватит есть`
        # если x <= 0
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Давай обойдемся без лишнего объявления переменных и на вход будем принимать currency_type.
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Давай представим ситуацию, что у нас добавилась еще одна новая валюта,
        # нам придется добавлять еще одно условие, но мы можем забыть добавить это условие и мы не попадем
        # ни в одно условие. Советую тут создать словарик, где ключом будет валюта, а значением кортеж из
        # курса и идентификатора валюты. Это упростит наш код и сделает его более лаконичным и стабильным, так как
        # при обращении к несуществующему ключу программа выдаст исключение.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # Нехорошо использовать выражения любого вида в f-строках
                # Попробуй вынести round(cash_remained, 2) в отдельную переменную,
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Как и в предыдущем примере, давай обойдемся без условия cash_remained < 0,
        # а оставим только наш return, ибо мы всегда будем возвращать это значени, если дойдем до сюда.
        elif cash_remained < 0:
            # В предыдущих условиях ты используешь один вывод строки, а тут другой.
            # Старайся придерживаться единности.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Что-то изменится, если мы уберем этот метод?
    def get_week_stats(self):
        super().get_week_stats()
