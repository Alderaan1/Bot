# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 18:42:11 2021

@author: Alderaan
"""

from webull import webull
import winsound
import datetime
import time
import requests

wb = webull()

tickerintrade = []
    
def bell():
    duration = 1000  
    freq = 3000  
    winsound.Beep(freq, duration)

    
def place_order():
    
    global ticker
    global expdt
    global stprice
    global direction
    global weekormnth
    global nodaysexp
    global tickerintrade
          
    op = wb.get_options_by_strike_and_expire_date(stock=ticker, expireDate=expdt, strike=stprice, direction=direction)
    
    for c in op : 
        c1 = c['call'] 
        c2 = c['put'] 
        
    if 'unSymbol' in c1:
        ticker = c1['unSymbol']
        strikePrice = c1['strikePrice']
        direction = c1['direction']
        price = c1['close']
        expireDate = c1['expireDate']
        tickerId = c1['tickerId']
        belongTickerId = c1['belongTickerId']
    
    if 'unSymbol' in c2:
        ticker = c2['unSymbol']
        strikePrice = c2['strikePrice']
        direction = c2['direction']
        price = c2['close']
        expireDate = c2['expireDate']
        tickerId = c2['tickerId']
        belongTickerId = c2['belongTickerId']
    
    print(' ')
    print(' ')
    print('         Suggested Option to Buy')
    print('         -----------------------')
    print('ticker                           : ', ticker)
    print('expireDate                       : ', expireDate)
    print('direction                        : ', direction)
    print('strikePrice                      : ', strikePrice )
    print('weekly Or monthly option expiry  : ', weekormnth)
    print('currentprice                     : ', price )
    print('num of days for option expiry    : ', nodaysexp)
    print('time now is                      : ',datetime.datetime.now().time())
    print(' ')
    print(' ')
        
    pt = input('Continue scanning ? Hit Any Key to continue  : ')
    tickerintrade.append(ticker)
    

# This is the main  

while  True:
     
    file_in = []
    lines = []
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    txt = requests.get('https://pastebin.com/raw/7d4TWvRR',headers = headers).text
     
    file_in = txt.splitlines()
    
    for line in file_in:
           lines.append(line) 

    for i in lines:
        i = i.rstrip()
        x = i.split()
        ticker = x[0]
        sorl = x[1]
        triggerprice = x[3]
        
        if ticker in tickerintrade:
            continue
        
        print('Chekcing ticker : ', ticker)


        op = wb.get_quote(stock=ticker)
        
        direction = 'N'
        if sorl.upper() == 'SHORT':
            if float(op['close']) < float(triggerprice) :
                direction= 'put'
        else:
            if float(op['close']) > float(triggerprice) :
                direction = 'call'

        
               
        if direction != 'N':
            print('Alert!!!!! ====> ', i ,' now at : ',op['close'])
            bell()
       
        
            optexp = wb.get_options_expiration_dates(stock=ticker, count=-1)
            for k in optexp:
                if int(k['days']) <= 1:
                    continue
                expdate = k['date']    
                nodaysexp = k['days']
                break
                        
            chain = wb.get_options(stock=ticker, count=-1, includeWeekly=1, direction=direction, expireDate=expdate, queryAll=0)
   
            for j in chain:

                if direction == 'call':
                    ch = j['call']
                    if round(float(ch['strikePrice'])) > float(op['close']):
                        stprice = ch['strikePrice']
                        expdt = ch['expireDate']
                        if ch['weekly'] == 1:
                            weekormnth = 'weekly'
                        else:
                            weekormnth = 'Monthly'
                        break
                if direction == 'put':
                    ch = j['put']
                    if round(float(ch['strikePrice'])) > float(op['close']):
                        stprice = priorstprice
                        expdt = priorexpdt
                        if ch['weekly'] == 1:
                            weekormnth = 'weekly'
                        else:
                            weekormnth = 'Monthly'
                        break
                    priorstprice = ch['strikePrice']
                    priorexpdt = ch['expireDate']

            place_order()
        
    time.sleep(5)