import requests
import smtplib
import email.utils
from email.mime.text import MIMEText
import pandas as pd
import numpy as np
import sqlalchemy as sql
from Variables import *                     # Imports queries and mysql credential
engine = sql.create_engine(ubuntu_local)    # Creates the engine for connecting to the database
class RawProcessing:                        #This class will process the json data obtained from bitso api
    def __init__(self, coin, df=None):
        self.coin = coin                    # Cryptocurrency ticker
        self.df = df                        # Dataframe object

    def myfunc(self):
        json_response = self.coin.json()
        data = json_response['payload']
        df = self.df
        df = pd.DataFrame(data)
        df['created_at']=pd.to_datetime(df['created_at'])   
        df['created_at'] = df['created_at'].dt.tz_convert('America/Tijuana')
        int_conv = df.amount.astype(np.float64)
        int_conv_two = df.price.astype(np.float64)
        pesos= int_conv * int_conv_two
        df['pesos'] = pesos
        return df
class mysql_db:                             # This class will insert data in the correct table from the bitso_api database.
    def __init__(self, t1, tbl):
        self.t1 = t1         # This is the dataframe passed
        self.tbl = tbl       # This is the table

    def myfunc_two(self):
        df = self.t1
        tbl = self.tbl
        intial_q = """INSERT INTO """ +tbl+ """
( created_at,amount,maker_side,price,pesos)
VALUES
"""
        values_q = ",".join(["""('{}','{}','{}','{}','{}')""".format(
        row.created_at,
        row.amount,
        row.maker_side,
        row.price,
        row.pesos) for idx, row in df.iterrows()])

        end_q = """ ON DUPLICATE KEY UPDATE
    created_at = values(created_at),
    amount = values(amount),
    maker_side = values(maker_side),
    price = values(price),
    pesos = values(pesos); """

        query = intial_q + values_q + end_q

        engine.execute(query)
#        print('''

  #      ''')
 #       print('*** Trading Project Phase 1.0 ***')
  #      print('''
#         By Erick Sandoval
 #       ''')
#        print(df.head(n=1),'\n')

        return self.t1

class PublicApi:
    def __init__(self, book):
        self.book = book
    def data(self):
        return requests.get('https://api.bitso.com/v3/trades/?book='+self.book)

class sendEmailNotification:

    def __init__(self,sender,passwrd,mesg,recipient):
        self.sender = sender
        self.passwrd = passwrd
        self.mesg = mesg
        self.recipient = recipient
    def send_the_message(self):
        msg = MIMEText(self.mesg)
        msg['To'] = email.utils.formataddr(('Recipient', self.recipient))   
        msg['From'] = email.utils.formataddr(('Author', self.sender))
        msg['Subject'] = 'Project Bot'    
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(self.sender, self.passwrd)
        server.sendmail(self.sender, [self.recipient], msg.as_string())
        server.quit()  

class UserBalance:
    def __init__(self, resp):
        self.resp = resp
    def insert_data(self):
        resp = self.resp
        data = resp.json()
        payload = data['payload']['balances']
        df = pd.DataFrame(payload)
        print(df)

        insert_query = '''
            INSERT INTO balance (currency, available, locked, total, pending_deposit, pending_withdrawal)
            VALUES
'''

        the_data = ",".join(["""('{}','{}','{}','{}','{}','{}')""".format(
        row.currency,
        row.available,
        row.locked,
        row.total,
        row.pending_deposit,
        row.pending_withdrawal ) for idx, row in df.iterrows()])

        update_data_on_duplicate = """ ON DUPLICATE KEY UPDATE
    currency = values(currency),
    available = values(available),
    locked = values(locked),
    total = values(total),
    pending_deposit = values(pending_deposit),
    pending_withdrawal = values(pending_withdrawal); """

        query = insert_query+the_data+update_data_on_duplicate

        engine.execute(query)
