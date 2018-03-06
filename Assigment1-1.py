from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np 
import os
   
def yahoo_stock_price (shortName):
    url = urlopen("https://finance.yahoo.com/quote/"+shortName+"?p="+shortName)
    content = url.read()
    soup = BeautifulSoup(content, 'html.parser')
    
    #get stock short name and company name
    title = soup.find_all('h1',{"class":"D(ib)"})
    for title in soup.find_all('h1',{"class":"D(ib)"}):
        symbal=(title.text.split("-"))[0]
        company=(title.text.split("-"))[1]
        #print(symbal, company)      

    #get stock price
    price = soup.find_all('span',{"class":"Mb(-4px)"})
    for price in soup.find_all('span',{"class":"Mb(-4px)"}):
        price=price.text.replace(",","")
        
    #buying a stock
    ask = soup.find_all("td",{"data-test":"ASK-value"})
    for ask in soup.find_all("td",{"data-test":"ASK-value"}):
        ask=(ask.text.split(" "))[0]
        ask=ask.replace(",","")

    #selling a stock
    bid = soup.find_all("td",{"data-test":"BID-value"})
    for bid in soup.find_all("td",{"data-test":"BID-value"}):
        bid=(bid.text.split(" "))[0]
        bid=bid.replace(",","")
    return symbal+"|"+company+"|"+price+"|"+ask+"|"+bid;

    
def action(shortName):
    print("\n")
    action = { '1':'Sell', 
               '2':'Buy', 
               '3':'Quit', 
             }
    print(action)
    print("\n")
    
    action_number = input("Do you want to sell(1) or buy(2) stock or quit(3): ")
    side = action[action_number]
    
    try:
        #Sell stocks on bid price
        if action_number == '1':
            quatity = input("How many shares: ")
            info = yahoo_stock_price (shortName)
            price = (info.split("|"))[4]
            print("Sell price: $"+price)
            decision = input("Confirm the price Yes(1) or No(2): ")
            if decision == '1':
                info = yahoo_stock_price (shortName)
                price = (info.split("|"))[4]
                total_amount = str(float(price) * float(quatity))
                timestamp = datetime.datetime.now().isoformat()
                print("Trade Sell price: $"+price)
                print("Trade total amount: $"+total_amount)
                print("Timestamp: "+timestamp)
                
                quatity = (-1)*float(quatity)
                return side+"|"+shortName+"|"+str(quatity)+"|"+price+"|"+timestamp+"|"+str(total_amount);            
            else:
                return;            
        
        #buy stocks on ask price
        elif action_number == '2':
            quatity = input("How many shares: ")
            info = yahoo_stock_price (shortName)
            price=(info.split("|"))[3]
            print("Buy price: $"+price)
            decision = input("Confirm the price Yes(1) or No(2): ")
            if decision == '1':
                info = yahoo_stock_price (shortName)
                price=(info.split("|"))[3]
                total_amount = str((-1)*float(price)* float(quatity))
                timestamp = datetime.datetime.now().isoformat()
                print("Trade Buy price: $"+price)
                print("Trade total amount: $"+total_amount)
                print("Timestamp: "+timestamp)
                return side+"|"+shortName+"|"+str(quatity)+"|"+price+"|"+timestamp+"|"+str(total_amount);              
            
        #quit action
        else:
            return;
    except KeyError:
        print ('Action %s not found' % action) 
    main()
    return;

    
def trade():
    print("\n")
    print('========================= Stock List =========================')
    print("\n")
    stock_list = {  '1':'AMZN', 
                    '2':'AAPL', 
                    '3':'INTC', 
                    '4':'MSFT',
                    '5':'SNAP',
                 }
    print(stock_list)
    print("\n")
    print("================================================================")
    print("\n")

    stock_number = input("Select your stock: ")
    shortName = stock_list[stock_number]

    try:
        if stock_number == '1':        
            info = yahoo_stock_price (shortName)
            print(info)
            df = action(shortName)
            return df;
        elif stock_number == '2':
            info = yahoo_stock_price (shortName)
            print(info)
            df = action(shortName)
            return df;
        elif stock_number == '3':
            info = yahoo_stock_price (shortName)
            print(info)
            df = action(shortName)
            return df;
        elif stock_number == '4':
            info = yahoo_stock_price (shortName)
            print(info)
            df = action(shortName)
            return df;
        else:
            info = yahoo_stock_price (shortName)
            print(info)
            df = action(shortName)
            return df;
    except KeyError:
        print ('Stock %s not found' % stock_list)

    return;

  
def remain_amount(trade_his):
    total_trade_amount =0.0
    
    for i in range(int(len(trade_his)/6)): 
        total_trade_amount = total_trade_amount + float(trade_his[i*6+5])
    
    remain_amount = total_trade_amount + 100000000
    return remain_amount;
       
#display a list of historic trades made by user
#the most recent trade at the top:1
def showBlotter(trade_his):
    ncol=6
    nrow=int((len(trade_his)/6))
    
    trade_arr=[['' for j in range(ncol)] for i in range(nrow)]
       
    for i in range(nrow):    
        for j in range(ncol):
           trade_arr[i][j] = trade_his[i*5+j+i]
    df=trade_arr[::-1]
    
    df = np.asarray(df)
    print(df)
    return;
    
 
def calculateProfitLoss(trade_his,shortName):
    ticker_list=[]
    
    ncol=6
    nrow=int((len(trade_his)/6))
    
    trade_arr=[['' for j in range(ncol)] for i in range(nrow)]
       
    for i in range(nrow):    
        for j in range(ncol):
           trade_arr[i][j] = trade_his[i*5+j+i]
        
    for i in range(int(len(trade_his)/6)):
        if trade_arr[i][1] == shortName:
            ticker_list = ticker_list + trade_arr[i]
        else:
            i=i+1
    print(ticker_list)
    
    if ticker_list != '':
        last_trade = ticker_list[(len(ticker_list)-6):len(ticker_list)]
        print(last_trade)
                
        #print('Ticker: '+shortName)                
        position=0.0
        for j in range(int(len(ticker_list)/6)):
            position = position + float(ticker_list[j*6+2])
        position = str(position)
        print('Position: '+position)
                
        info = yahoo_stock_price (shortName)
        price = (info.split("|"))[2]
        print('Current Market Price: '+price)
                
        #VMAP of what the user holded the ticker
        total_quatity = 0.0
        total_buySell = 0.0
        VMAP = 0.0
        for k in range(int(len(ticker_list)/6)):
            total_quatity = total_quatity + float(ticker_list[k*6+2])
            total_buySell = total_buySell + float(ticker_list[k*6+5])
        #print(total_quatity)
        #print(total_buySell)
        if total_quatity == 0.0:
            VMAP = 0.0
        else:
            VMAP = abs(total_buySell/total_quatity)
        print('VMAP: '+str(VMAP))
                
        #bid/ask price on holded quatity
        bid=0.0
        ask=0.0
        UPL=0.0
        bid = (info.split("|"))[4]
        ask = (info.split("|"))[3]
        if float(position) >= 0:
            UPL = float(position) * (float(bid)-VMAP)
        else:
            UPL = float(position) * (float(ask)-VMAP)
        print('Unrealized P/L: '+str(UPL))
        
        #RPL happened while the user buy and sell the ticker
        #RPL only count min(#buy, #sell) *(avg of sell - avg of buy)
        RPL=0.0
        buy_quantity = 0.0
        buy_total = 0.0
        sell_quantity = 0.0
        sell_total = 0.0
        for h in range(int(len(ticker_list)/6)):
            if float(ticker_list[h*6+2]) >= 0:
                buy_quantity = buy_quantity + float(ticker_list[h*6+2])
                buy_total = buy_total + float(ticker_list[h*6+5])
            else:
                sell_quantity = sell_quantity + float(ticker_list[h*6+2])
                sell_total = sell_total + float(ticker_list[h*6+5])
        if buy_quantity == 0.0 or sell_quantity == 0.0:
            RPL = 0.0
        else:
            if buy_quantity > abs(sell_quantity):
                RPL = abs(sell_quantity) *((sell_total/abs(sell_quantity)) - (abs(buy_total)/buy_quantity))
            else:
                RPL = buy_quantity *((sell_total/abs(sell_quantity)) - (abs(buy_total)/buy_quantity))
        print('Realized P/L: '+str(RPL))
        
        return str(last_trade)+"|"+shortName+"|"+str(position)+"|"+str(price)+"|"+str(VMAP)+"|"+str(UPL)+"|"+str(RPL);     
    else:
        print('No trade records on '+shortName+'.')
    return;


def showprofitLoss(pl): 
    print("\n")
    print('Your last trade :')
    print((pl.split("|"))[0]) 
    print("\n")           
    print("====================== P/L ======================")
    print("\n")
    print('    Ticker              : '+(pl.split("|"))[1])
    print('    Position            : '+(pl.split("|"))[2])
    print('    Current Market Price: $'+(pl.split("|"))[3])
    print('    VWAP                : '+(pl.split("|"))[4])
    print('    Unrealized P/L      : $'+(pl.split("|"))[5]) 
    print('    Realized P/L        : '+(pl.split("|"))[6])
    print("\n")
    print("==================================================")
    print("\n")
    return;

    

# show the main menu
def main():  
    #creat a list to store trade history
    trade_his=[]
    
    print("\n")
    print('======================== The Main Menu ========================')
    print("\n")
    items = {   '1':'Trade', 
                '2':'Show Blotter', 
                '3':'Show P/L', 
                '4':'Quit',}
    print(items)
    print("\n")
    print("================================================================")
    print("\n")
    
    choice = 0 
    while int(choice) in range (4):
        choice = int(input("Select a number of your choice: "))
        print(items[str(choice)] )

        total_cash = remain_amount(trade_his)
        
        if choice == 1:            
            df = trade()
            
            if df != '':
                side = (df.split("|"))[0] 
                shortName = (df.split("|"))[1]
                quatity =  float((df.split("|"))[2])
                price = float((df.split("|"))[3])
                timestamp = (df.split("|"))[4]
                total_amount = float((df.split("|"))[5])
                
                remain_cash = total_amount + total_cash
                if remain_cash >= 0:
                    #update trade recodes for Blotter 
                    new_trade = [side,shortName,quatity,price,timestamp,total_amount]
                    trade_his = np.append(trade_his,new_trade)
                    trade_his = np.asarray(trade_his)                    
                    #print(trade_his)
                    
                    #update P/L
                    calculateProfitLoss(trade_his,shortName)                 
                else:
                    print('You have $'+str(total_cash))
                    print("You don't have enought cash to purchase new trade.")

        elif choice == 2:
            #print(trade_his)
            showBlotter(trade_his)

        elif choice == 3:
            print("\n")
            print('========================= Stock List =========================')
            print("\n")
            stock_list = {  '1':'AMZN', 
                            '2':'AAPL', 
                            '3':'INTC', 
                            '4':'MSFT',
                            '5':'SNAP',
                         }
            print(stock_list)
            print("\n")
            print("================================================================")
            print("\n")
            
            stock_number = int(input("Select your stock: "))
            shortName = stock_list[str(stock_number)]
                
            pl = []
            pl = calculateProfitLoss(trade_his,shortName)            
            showprofitLoss(pl)
        else:
            return;
    else:
        print ('Item %s not found' % choice)  
main()