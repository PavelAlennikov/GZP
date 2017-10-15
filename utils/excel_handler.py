import pandas as pd
import xlrd
from xlrd import xldate_as_tuple as number_to_date


def read_dates_and_protocols(file_name):
    print('Reading dates and protocols...')
    wb = xlrd.open_workbook('./' + file_name)
    sheet = wb.sheet_by_index(0)

    dates = [number_to_date(date, 0)[:2] for date in sheet.col_values(0)[1:]]
    protocols = sheet.col_values(1)[1:]

    dates_and_protocols = {}
    for date, protocol in zip(dates, protocols):
        dates_and_protocols.setdefault(date, []).append(protocol)

    print('Dates and protocols received successfully:')
    for date in dates_and_protocols:
        print('Date:', date, 'protocol numbers:', dates_and_protocols[date])

    return dates_and_protocols


def write_fields_into_excel(file_name, fields):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    fields.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return
