from pandas import DataFrame,to_datetime
from requests import get
from sqlalchemy import create_engine
from time import sleep

engine2 = create_engine('mysql+mysqlconnector://tom:123@192.168.1.74:3306/trades2')

class public:
    def __init__(self,book):
        self.book = book
        
    def data(self):
    
        #print(self.book)
        
        x = get('https://api.bitso.com/v3/trades/?book='+self.book)
        
        return x

def executeData():
    '''If either of the two try staments raise an error then will loop over and over
    '''
    coins = ['btc_mxn','eth_mxn','ltc_mxn','xrp_mxn','bat_mxn']
    for coin in coins:
        print(coin)
        try:
            public_instance = public(coin).data()
            #print(public_instance)
            #raise IndexError
        except:
            print('Error')
            sleep(5)
            executeData()
        
        try:
            y = public_instance.json()['payload']
            #raise IndexError
        except:
            print('Error No.2')
            sleep(5)
            executeData()
        
        finally:
            df = DataFrame(y)
            df['created_at'] = to_datetime(df['created_at'])
            df['created_at'] = df['created_at'].dt.tz_convert('America/Tijuana')
            df['date'] = df['created_at'].dt.date
            df['time'] = df['created_at'].dt.time
            print(df.head(n=3))
            
            intial_q = """INSERT INTO """+coin+""" 
( created_at,date,time,price)
VALUES
"""
            values_q = ",".join(["""('{}','{}','{}','{}')""".format(
        row.created_at,
        row.date,
        row.time,
        row.price ) for idx, row in df.iterrows()])

    
            end_q = """ ON DUPLICATE KEY UPDATE
    created_at = values(created_at),
    date = values(date),
    time = values(time),
    price = values(price); """
 
            query = intial_q + values_q + end_q  

            engine2.execute(query)
            #return df
    
while True:
    executeData()
    sleep(60)
#type(executeData())