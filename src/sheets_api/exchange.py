
from datetime import datetime
from time import sleep
from typing import List
from googleapiclient.errors import HttpError
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from data import connect, select, run_query
from kurs_exchange import get_actual_rate
import decimal
import threading 


SAMPLE_SPREADSHEET_ID = '18GKiLKq4zcd1UlQQnrb_C686uJ6EY9YseLAizR36YAo'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_RANGE_NAME = 'Лист1!A2:E'

def get_data_from_sheet() -> List:
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    
    CREDENTIALS_FILE = 'service_account.json'  # имя файла с закрытым ключом

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    

    try:
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        return values

    except HttpError as err:
        print(err)



def run_script() -> None:
    """Run main script once"""
    # get data from google sheet
    list_of_data = get_data_from_sheet()
    list_for_insert = ', '.join([str(value).replace('[','(').replace(']',')') for value in list_of_data]) #format data for using in sql query

    # connect database
    connDatabase = connect()

    # query that compare data from sheet and database and return changed records
    sqlQuery = f"""CREATE TEMP TABLE temp_orders (
        tmp_id BIGSERIAL PRIMARY KEY NOT NULL, 
        tmp_my_order varchar, 
        tmp_my_amount numeric(15,2), 
        tmp_my_date TIMESTAMP NOT NULL DEFAULT current_timestamp);
        INSERT INTO temp_orders VALUES {list_for_insert};
        SELECT * FROM temp_orders
        FULL OUTER JOIN my_orders on my_orders.id = temp_orders.tmp_id WHERE my_orders.id IS Null OR (my_orders.my_order <> temp_orders.tmp_my_order 
        OR my_orders.my_amount <> temp_orders.tmp_my_amount 
        OR my_orders.my_date <> temp_orders.tmp_my_date);"""

    all_records = select(sqlQuery,connDatabase)
    #
    if len(all_records)>0:
        # getting the current exchange rate, before execute http query we check .ini file if there are actual rate
        rate = get_actual_rate()
        for i in all_records:
            if i[4] == None: #it is new record in sheet
                cyrr_ = i[2] * decimal.Decimal(rate if rate > 0.0 else 1.0)
                sqlQuery = f"""INSERT INTO my_orders VALUES ({i[0]}, {i[1]}, {i[2]}, '{i[3]}', {cyrr_})""" 
                run_query(sqlQuery,connDatabase) 
            elif i[0] == None: #delete record
                sqlQuery = f"""DELETE * FROM my_orders WHERE id={i[4]}"""
                run_query(sqlQuery,connDatabase)
            else: # in all other situations update data and update amount in RUB
                cyrr_ = i[2] * decimal.Decimal(rate if rate > 0.0 else 1.0)
                sqlQuery = f"""UPDATE my_orders SET my_order = {i[1]}, my_amount = {i[2]}, my_date = '{i[3]}', my_rub_amount = {cyrr_} WHERE id={i[0]}""" 
                run_query(sqlQuery,connDatabase) 

    #closing database      
    connDatabase.close()



def start_app():

    STOP_FLAG = False
    def running_script():
        while not STOP_FLAG:
            run_script()
            sleep(60)
    thr1 = threading.Thread(target = running_script) 
    thr1.start()
"""    STOP_FLAG = True
    while thr1.is_alive() == True: 
        pass"""

