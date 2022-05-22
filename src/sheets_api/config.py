#!/usr/bin/python
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def update_config(filename='daily_rate.ini', section='daily_rate',param='rate',value=0.0):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    parser.set(section, param, value)

    with open(filename, 'w') as configfile:
        parser.write(configfile)