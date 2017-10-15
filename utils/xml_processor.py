from xml.etree import ElementTree as etree
from collections import OrderedDict

namespaces = {'ztns': 'http://zakupki.gov.ru/oos/types/1'}


def get_auction_attr(tree):
    params = ['purchaseNumber', 'protocolNumber', 'protocolDate', 'fullName', 'journalNumber', 'price', 'appRating',
              'resultType', 'admitted', 'organizationName', 'inn', 'kpp', 'postAddress']
    rows = OrderedDict().fromkeys(params)
    rows.update(__get_base_auction_attr(tree, params[:3 + 1]))
    for application in tree.findall('.//ztns:application', namespaces):
        app_attr = __get_app_attr(application)
        for attr in app_attr:
            if rows[attr] is None:
                rows[attr] = [app_attr[attr]]
            else:
                rows[attr].append(app_attr[attr])
    return rows


def __get_base_auction_attr(tree, attr_names):
    return {name: tree.find('.//ztns:' + name, namespaces).text for name in attr_names}


def __get_app_attr(application):
    app_attr_objects = {'journalNumber': application.find('ztns:journalNumber', namespaces),
                        'price': application.find('ztns:price', namespaces),
                        'appRating': application.find('ztns:appRating', namespaces),
                        'resultType': application.find('.//ztns:resultType', namespaces),
                        'admitted': application.find('ztns:admitted', namespaces)
                        }

    app_participant = application.find('.//ztns:appParticipant', namespaces)
    app_attr_objects.update(__get_participant_attr(app_participant))

    app_attr_values = {
        app_attr: app_attr_objects[app_attr].text if app_attr_objects[app_attr] is not None else 'NOT_FOUND'
        for
        app_attr in app_attr_objects
        }
    return app_attr_values


def __get_participant_attr(app_participant_obj):
    app_participant_attributes = {'organizationName': app_participant_obj.find('ztns:organizationName', namespaces),
                                  'inn': app_participant_obj.find('ztns:inn', namespaces),
                                  'kpp': app_participant_obj.find('ztns:kpp', namespaces),
                                  'postAddress': app_participant_obj.find(
                                      'ztns:postAddress', namespaces)
                                  }
    return app_participant_attributes


def get_auc_prices_with_corr_jns(tree):
    result = {}
    applications = tree.findall('.//ztns:application', namespaces)
    for application in applications:
        jn = application.find('ztns:journalNumber', namespaces).text
        try:
            final_price = application.find('.//ztns:lastOffer', namespaces).find('ztns:price', namespaces).text
        except:
            final_price = 'not found'
        result[jn] = final_price
    return result
