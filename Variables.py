ubuntu_erick = 'mysql+mysqlconnector://tom:123@192.168.1.74:3306/trades'
ubuntu_local = 'mysql+mysqlconnector://local:123@192.168.1.74:3306/trades'
sender = 'cryptoproject2@gmail.com'
password = 'cryptoanalysts'
recipient = 'emscanalyst@gmail.com'



query_balance = '''
SELECT distinct currency, available,max(  price  )  over (partition by currency) as 'price'
FROM balance b LEFT JOIN user_trades t ON b.currency = t.fees_currency
WHERE available>0  and currency not in ('mxn')
'''

initial_q = '''
INSERT INTO balance 
(
        currency, available, locked, total, pending_deposit, pending_withdrawal
)
VALUES 
'''


end_q = """ ON DUPLICATE KEY UPDATE
    currency = values(currency),
    available = values(available),
    locked = values(locked),
    total = values(total),
    pending_deposit = values(pending_deposit),
    pending_withdrawal = values(pending_withdrawal); """  
