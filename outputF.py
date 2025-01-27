from datetime import datetime, timedelta

def commission(total, units):
    commission=units*0.005
    if commission>total*0.005:
        commission=total*0.005
    
    return commission

def daily_trade(raw_data, last_infos, current_date, minimal_note, TP, further_day):
    
   

    trade_infos=[]
    
    position=last_infos['position']
    initial_cash=last_infos['cash']

    news=last_infos['news']
    note=last_infos['note']
    alpha=2/(10+1)
    #print(news)
    
    buy=None
    sell=None

    
    

    for new in news:
            
            new_time= datetime.strptime(new['time'], '%H:%M:%S')

            if 4>new_time.hour:
                total_product_score=new['relevance_score']*new['sentiment_score']
                note=(alpha*total_product_score+(1-alpha)*note)/(new['relevance_score']*alpha+(1-alpha))
        
    

    for time, ohlc in raw_data.items():
        
        ohlc['1. open'] = round(float(ohlc['1. open']),5)
        ohlc['2. high'] = round(float(ohlc['2. high']),5)
        ohlc['3. low'] = round(float(ohlc['3. low']),5)
        ohlc['4. close'] = round(float(ohlc['4. close']),5)



        if position['buy']==True: 

    
            if last_infos['surprise']['surprise']==False and last_infos['surprise']['time']==True and current_date==last_infos['date_following']:
                sell=position['buy_position']['units']*ohlc['1. open']
                selling='bad earning'

            if last_infos['surprise']['surprise']==False and last_infos['surprise']['time']==False and current_date>last_infos['date_following']:
                sell=position['buy_position']['units']*ohlc['1. open']
                selling='bad earning'


            if ohlc['4. close']>=position['takeProfit']:
                sell=position['buy_position']['units']*ohlc['4. close']
                selling='TP'
                #print('takeprofit', position['takeProfit'])

            elif  ohlc['4. close']<=position['stopLoss'] and current_date>=last_infos['date_following']: 
                sell=position['buy_position']['units']*ohlc['4. close']
                selling='SL'
                #print('stoploss', position['stopLoss'])

           
            
            
            elif current_date>=last_infos['date_following']+timedelta(days=further_day):
                sell=position['buy_position']['units']*ohlc['4. close']
                selling='end'

        
        if sell!=None:

           last_cash=last_infos['cash']  

           last_infos['cash']-=commission(position['buy_position']['price']*position['buy_position']['units'], position['buy_position']['units'])

           last_infos['cash']-=commission(sell, sell/position['buy_position']['units'])
           
           last_infos['cash']+=sell-position['buy_position']['units']*position['buy_position']['price']

           trade_infos.append({'gains':round(last_infos['cash']/last_cash-1, 8), 'note': position['Note'], 'buy_time':position['buy_time'], 'sell_time': current_date, 'selling':selling })

           position={'buy_position': None, 'stopLoss': None, 'takeProfit':None, 'buy':False,  'Note': None, 'buy_time': None}

           sell=None
           buy=None
        

       
        
        
        time_obj = datetime.strptime(time, "%H:%M:%S").time()
        
        for new in news:
            new_time= datetime.strptime(new['time'], '%H:%M:%S')
            if time_obj.hour==new_time.hour:
                total_product_score=new['relevance_score']*new['sentiment_score']
                note=(alpha*total_product_score+(1-alpha)*note)/(new['relevance_score']*alpha+(1-alpha))
                #print(note, 'jour', new['time'])
        
        if position['buy']==False and current_date<last_infos['date_following']:
            
            if note>minimal_note:
                buy={'price':ohlc['4. close'], 'units': round((last_infos['cash'])/ohlc['4. close'],5)}
                #on peut supposer un controle humain de la situation avec une prise de position au closing après vérification
                if TP<=0.11:
                    position={'buy_position': buy ,'stopLoss': ohlc['4. close']*(1-(TP-0.03)), 'takeProfit': ohlc['4. close']*(1+TP), 'buy':True,  'Note': note, 'buy_time': current_date}
                else:
                    position={'buy_position': buy ,'stopLoss': ohlc['4. close']*(1-(0.1)), 'takeProfit': ohlc['4. close']*(1+TP), 'buy':True,  'Note': note, 'buy_time': current_date}
        last_infos['position']=position
        last_infos['note']=note


        
    
    for new in news:
            new_time= datetime.strptime(new['time'], '%H:%M:%S')
            if time_obj.hour<new_time.hour:
                total_product_score=new['relevance_score']*new['sentiment_score']
                note=(alpha*total_product_score+(1-alpha)*note)/(new['relevance_score']*alpha+(1-alpha))
                #print(note, 'Soir',new['time'])


    #print(trade_infos)
    if trade_infos!=[]:
        return  {'last_infos': last_infos, 'yield':last_infos['cash']/initial_cash, 'trade_infos':trade_infos}
    else: 
        return {'last_infos': last_infos}