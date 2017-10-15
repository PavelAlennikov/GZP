import calendar
import datetime


def add_months(source_date, months):
    if isinstance(source_date, datetime.date):
        month = source_date.month - 1 + months
        year = int(source_date.year + month / 12)
    else:
        month = source_date[1] - 1 + months
        year = int(source_date[0] + month / 12)
    month = month % 12 + 1
    result = datetime.date(year, month, 1) if isinstance(source_date, datetime.date) else (year, month, 1)
    return result


def generate_date_interval(date):
    first_date = datetime.date(date[0], date[1], 1)
    second_date = add_months(first_date, 1)
    return str(first_date).replace('-', '') + '00_' + str(second_date).replace('-', '') + '00'
