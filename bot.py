from Classes import *           # Imports RawProcessing, mysql_db, project, sendEmailNotification and userBalance
from Request import *           # Imports PrivateApi & createSignature method
from Variables import *         # Imports credentials, email, password and queries
import requests
import time
import sqlalchemy as sql
import pandas as pd
import json

engine = sql.create_engine(ubuntu_erick)  

def placedata():
    coins = ['btc', 'eth', 'ltc', 'xrp','bat']
    for coin in coins:
        try:
            bitcoin = PublicApi(coin+'_mxn')
            dat = bitcoin.data()
        except requests.exceptions.ConnectionError:
            time.sleep(120)
            mesg = 'Hello World, There has been a connection error.'
            send_email_inst = sendEmailNotification(sender,password,mesg,recipient)
            send_the_email = send_email_inst.send_the_message()
            placedata()
        finally:
            proces = RawProcessing(dat)     # Create instance of RawProcessing class
            try:
                formatt = proces.myfunc()    # Usually there is a json decode error here
            except:
                time.sleep(10)
                placedata()
            finally:
                table = coin+'_trades'
                sq = mysql_db(formatt,table)
                insert = sq.myfunc_two()
                time.sleep(5)
def get_returns():
    item = 0    
    df_returns = pd.read_sql(query_balance, engine)           # This will query & calculate returns for the selected coin.
    result_to_dict = df_returns.to_dict()                     #  We convert it to a dict to visualize it better.
    while True:
        try:
            the_coin = result_to_dict['currency'][item]       # Name of the crypto (str)
            the_price = result_to_dict['price'][item]
            the_available = result_to_dict['available'][item]
            the_invested = (the_price) * (the_available)
        except:
            break   
        item = item + 1    
        query_returns = '''
    SELECT CONCAT (     ( (price/  '''+str(the_price)  + ''' )-1 )*100,2)  as Returns
    , format(('''+str(the_available)  + ''' * price),2)  as Pesos
    , '''+str(the_invested)  + ''' as Investment
    ,   ('''+str(the_available)  + ''' * price)-'''+str(the_invested)  + ''' as Delta
    FROM '''+ the_coin  + '''_trades ORDER BY created_at DESC
    LIMIT 0,1
'''

        query_returns_percentage = '''
    SELECT CONCAT (  format(   ( (price/  '''+str(the_price)  + ''' )-1 )*100,2), ' %')  as Returns
    , format(('''+str(the_available)  + ''' * price),2)  as Pesos
    , '''+str(the_invested)  + ''' as Investment
    ,   ('''+str(the_available)  + ''' * price)-'''+str(the_invested)  + ''' as Delta
    FROM '''+ the_coin  + '''_trades ORDER BY created_at DESC
    LIMIT 0,1
'''
        results_returns_percentage = pd.read_sql(query_returns_percentage,engine)
        results_returns = pd.read_sql(query_returns,engine)
        print('\n' + '=' * 51)
        print('Returns'+' '+the_coin+' '+ 'Data :','\n',results_returns_percentage,'\n')    # Display important information.
        
        results_returns_dict = results_returns.to_dict()
        returns = results_returns_dict['Returns'][0]
        convertion = round(float(returns))
        available_coin = round(float(the_available))
        print('COIN:',the_coin)
        print('AVAILABLE:',the_available)
        
        if the_coin =='btc' and convertion  >=18 and the_available>0:     # Both conditions have to be met, convertion is a rounded int.
            print('Success!!')
            get_balance = PrivateApi(my_key,bts_key,http_meth='GET',req_path='/v3/balance')
            resp = get_balance.createSignature()
            data = resp.json()
            coin_avai = data['payload']['balances'][2]['available']
            param={
    'book': the_coin+'_mxn',
    'side': 'sell',
    'type': 'market',
    'major': coin_avai
    }
            privateapi_inst = PrivateApi(my_key,bts_key,http_meth='POST',req_path='/v3/orders',param=param)       # Instantiates the Object.
            print(privateapi_inst.createSignature().text)                                                   # Prints Request POST response.
            resp = PrivateApi(my_key,bts_key,http_meth='GET',req_path='/v3/balance').createSignature()      # Now we update our balance
            UserBalance(resp).insert_data()


            mesg = 'Congratulations you have just sold'+str(the_available)+'of'+the_coin
            send_email_inst = sendEmailNotification(sender,password,mesg,recipient)
            send_the_email = send_email_inst.send_the_message()

       
        if the_coin =='ltc' and convertion  >=15 and the_available>0:     # Both conditions have to be met, convertion is a rounded int.
            print('Success!!')
            get_balance = PrivateApi(my_key,bts_key,http_meth='GET',req_path='/v3/balance')
            resp = get_balance.createSignature()
            data = resp.json()
            coin_avai = data['payload']['balances'][5]['available']     # LITECOIN
            param={
    'book': the_coin+'_mxn',
    'side': 'sell',
    'type': 'market',
    'major': coin_avai
    }
            privateapi_inst = PrivateApi(my_key,bts_key,http_meth='POST',req_path='/v3/orders',param=param)       # Instantiates the Object.
            print(privateapi_inst.createSignature().text)                                                   # Prints Request POST response.
            resp = PrivateApi(my_key,bts_key,http_meth='GET',req_path='/v3/balance').createSignature()      # Now we update our balance
            UserBalance(resp).insert_data()


            mesg = 'Congratulations you have just sold'+str(the_available)+'of'+the_coin
            send_email_inst = sendEmailNotification(sender,password,mesg,recipient)
            send_the_email = send_email_inst.send_the_message()

        if the_coin =='eth' and convertion  >=26 and the_available>0:     # Both conditions have to be met, convertion is a rounded int.
            print('Success!!')
            get_balance = PrivateApi(my_key,bts_key,http_meth='GET',req_path='/v3/balance')
            resp = get_balance.createSignature()
            data = resp.json()
            coin_avai = data['payload']['balances'][4]['available'] # eth
            param={
    'book': the_coin+'_mxn',
    'side': 'sell',
    'type': 'market',
    'major': coin_avai
    }
            privateapi_inst = PrivateApi(my_key,bts_key,http_meth='POST',req_path='/v3/orders',param=param)       # Instantiates the Object.
            print(privateapi_inst.createSignature().text)                                                   # Prints Request POST response.
            resp = PrivateApi(my_key,bts_key,http_meth='GET',req_path='/v3/balance').createSignature()      # Now we update our balance
            UserBalance(resp).insert_data()


            mesg = 'Congratulations you have just sold'+str(the_available)+'of'+the_coin
            send_email_inst = sendEmailNotification(sender,password,mesg,recipient)
            send_the_email = send_email_inst.send_the_message()


        

        
while True:
    #placedata()
    get_returns()
    time.sleep(3)



#get_balance = PrivateApi(my_key,bts_key,http_meth='GET',req_path='/v3/balance')
#resp = get_balance.createSignature()
#data = resp.json()
#coin_avai_btc = data['payload']['balances'][2]['currency']     # BTC
#coin_avai_eth = data['payload']['balances'][4]['currency']     # ETH
#coin_avai_ltc = data['payload']['balances'][6]['currency']     # LTC
#print(coin_avai_ltc)



#resp = PrivateApi(my_key,bts_key,http_meth='GET',req_path='/v3/balance').createSignature()      # Now we update our balance
#UserBalance(resp).insert_data()
