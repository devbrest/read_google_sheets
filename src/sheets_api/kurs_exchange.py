from unicodedata import decimal
from config import config, update_config
from datetime import date
import urllib.request as urli
from xml.etree import ElementTree as ET

def get_actual_rate():
    """Get actual rate
    1. Read config file .ini
    if date in file is equal current date take rate from file
    2. Else connect to http://www.cbr.ru/scripts/XML_daily.asp"""
    params = config(filename='daily_rate.ini', section='daily_rate')
    today = date.today()

    d1 = today.strftime("%Y-%m-%d")
    if params['date'] == d1:
        return float(params['rate'].replace(',','.'))
    else:
        rate = return_daily_rate()
        update_config(param='date',value=d1);
        update_config(value=rate);
        return float(rate.replace(',','.'))


def get_xml(url):
    """get xml with current rate
    return xml-structured string"""
    response = urli.urlopen(url)
    return response.read()

def return_daily_rate():
    xml = get_xml('http://www.cbr.ru/scripts/XML_daily.asp')
    rate = 1.0
    xml_data = ET.fromstring(xml)
    for child in xml_data:
        if child.attrib['ID'] == 'R01235':
            for valute in child:
                if valute.tag == 'Value':
                    rate = valute.text

    return rate
"""if __name__ == '__main__':
    get_actual_rate()"""