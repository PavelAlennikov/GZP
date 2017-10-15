import xml.etree.ElementTree as etree
from collections import OrderedDict
from utils.xml_processor import get_auc_prices_with_corr_jns, get_auction_attr
import pandas as pd

NS = '{http://zakupki.gov.ru/oos/types/1}'


def extract_fields(files, data_frame):
    single_flag = len(files.keys()) == 1
    file_fields_as_table = OrderedDict()
    prices_with_jns = {}
    for key in sorted(files):
        if single_flag:
            file_fields_as_table = extract_auc_attrs(files[key])
        elif '2' in key:
            prices_with_jns = extract_prices(files[key])
        elif '3' in key:
            file_fields_as_table = extract_auc_attrs(files[key])
            file_fields_as_table['price'] = reorder_prices_by_jn(prices_with_jns, file_fields_as_table['journalNumber'])
        files[key].close()
    result = pd.DataFrame(file_fields_as_table)
    return data_frame.append(result)


def extract_auc_attrs(file):
    tree = etree.parse(file)
    return get_auction_attr(tree)


def extract_prices(file):
    tree = etree.parse(file)
    return get_auc_prices_with_corr_jns(tree)


def reorder_prices_by_jn(price_with_jns, journal_number_list):
    return [price_with_jns[jn] for jn in journal_number_list]
