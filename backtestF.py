import asyncio
from local_dataF import ohlc_recovery, news_recovery, calendar_earnings, ema_recovery
from datetime import timedelta, datetime
from outputF import daily_trade
import csv


def analysis(daily_results):
    
    analysis={'total_yield':1.0 , 'cash':0,'trades':{}, 'global':{'trade':0, 'duree':0 ,'plus':0, 'yield':0}}

    for day, results in daily_results.items():

        if 'yield' in results:
            
            analysis['total_yield']*=results['yield']

            analysis['cash']=results['last_infos']['cash']

            for trade in results['trade_infos']:
                difference=trade['sell_time']-trade['buy_time']
                analysis['trades'][day]={'gain':trade['gains']+1, 'date':trade['buy_time'], 'type':trade['selling']}
                analysis['global']['duree']+=difference.days
                analysis['global']['trade']+=1
                analysis['global']['yield']+=trade['gains']+1
                if trade['gains']>0:
                    analysis['global']['plus']+=1

    return analysis
    


async def main_backtest(symbol,earnings, before_earning, minimal_note, TP,further_day, backtest):
    
    calendar=await calendar_earnings(6,symbol)
    calendar = [{'date':datetime.strptime(earning['date'], '%Y-%m-%d').date(),'surprise': earning['surprise'], 'time':earning['time'] } for earning in calendar]

    
    debut=calendar[-1]['date']-timedelta(days=30)
    fin=calendar[0]['date']+timedelta(days=30)
    
    raw_data=await ohlc_recovery(symbol, debut, fin)


    ema_data=await ema_recovery(symbol)
    
    start_date=calendar[-earnings]['date']-timedelta(days=before_earning+5)  #-1 que end_date précédent
    end_date=calendar[-earnings]['date']+timedelta(days=further_day+5)

    i=1

    last_infos = {
        'cash': 1000,
        'news': [],
        'position': {'buy_position': None, 'stopLoss': None, 'takeProfit':None, 'buy':False,  'Note': None, 'buy_time': None},
        'date_following': calendar[-i]['date'],
        'surprise':{'surprise':calendar[-i]['surprise'], 'time':calendar[-i]['time']}, 
        'note': 0
    }

    last_date='0'
    daily_results = {'0':{'last_infos': last_infos, 'yield':1, 'trade_infos':[]}}

    current_date = start_date

    o=0  #permet de calculer la moyenne arithmétique de la note


    last_closes=[]
    j=0
    while len(last_closes)<200:
        j+=1
        if str(current_date-timedelta(days=j)) in ema_data:
            last_closes.append(float(ema_data[str(current_date-timedelta(days=j))]['4. close']))

        
    number_of_news=0

    while current_date <= end_date:
        

        if last_infos['date_following']+timedelta(days=30)<current_date:
            i+=1
            last_infos['date_following']=calendar[-i]['date']
            last_infos['surprise']['surprise']=calendar[-i]['surprise']
            last_infos['surprise']['time']=calendar[-i]['time']
            last_infos['position']
        

        date_obj = datetime.strptime(str(current_date) + ' ' + '00:00:00', '%Y-%m-%d %H:%M:%S')
        day_news = date_obj.strftime('%Y%m%dT%H%M')
        last_infos['news']=await news_recovery(str(day_news), symbol, debut)
        
        ii=0
        for new in last_infos['news']:
            if new['sentiment_score']==0:
                last_infos['news'].pop(ii)
                
            ii+=1   
        number_of_news+=len(last_infos['news'])

        if str(current_date) in ema_data:
            last_closes.pop()
            last_closes.insert(0, float(ema_data[str(current_date)]['4. close']))
        ema_50=round(sum(last_closes[:50])/50,1)
        ema_150=round(sum(last_closes[:150])/150,1)


        if current_date>=last_infos['date_following']-timedelta(days=before_earning) and number_of_news>10 and ema_50>=ema_150:
            o=0  
            if str(current_date) in raw_data:
                daily_results[str(current_date)]=daily_trade(raw_data[str(current_date)], daily_results[last_date]['last_infos'], current_date, minimal_note, TP, further_day)
                last_date=str(current_date)

        else:
            total_product_score = sum(news.get('relevance_score', 0) * news.get('sentiment_score', 0) for news in last_infos['news'])
            if total_product_score!=0:
                last_infos['note']=(last_infos['note']*o+total_product_score)/(o+sum(news.get('relevance_score', 0) for news in last_infos['news']))
            o+=sum(news.get('relevance_score', 0) for news in last_infos['news'])
            
            
        current_date += timedelta(days=1)
    
    
    return analysis(daily_results)



async def extraction(filename,earnings, action, combinaison):

    #nombre de jours à partir de quand on trade et de quand on sort du trade
    before=[3,5] #max 25

    TPs=[0.04,0.05, 0.06,0.07,0.08,0.09, 0.1] #entre 0 et 0.2
    note=[0.2,0.22,0.24,0.26, 0.28,0.3]

    further=[3,5]
    #note minimale
    
    #utilisation des différents ratio (plus tard pour perfectionner)
    if combinaison!=None:
        before=[3]
        TPs=[combinaison[0]]
        note=[combinaison[1]]
        further=[3]
    
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['action', 'total_yield', 'cash', 'trades','parameters', 'global']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            
            writer.writeheader()
        
        print(action)
        best_parameters={}
        liste=[]
        score=0   

        for further_day in further:
            for before_earning in before:
                for TP in TPs:
                    for minimal_note in note:

                        total_result=1

                        total_trades=0

            
                    
                        result = await main_backtest(action, earnings,before_earning, minimal_note,  TP , further_day, True)
                                
                        total_result=result['total_yield']*total_result
                        total_trades+=result['global']['trade']
                            
                        if total_trades>0:
                            
                            if  score<=total_result:
                                best_parameters = {'before_earning': before_earning, 'note': minimal_note, 'TP':TP, 'further_day': further_day}
                                score=total_result


                            if 1<=total_result:

                                entry = {
                                            'before_earning': before_earning,
                                            'note': minimal_note,
                                            'TP': TP,
                                            'further_day': further_day, 
                                            'total trades':total_trades,
                                            'rendement_moyen':total_result/total_trades
                                        }
                                liste.append(entry)
                                

        row = {'action': action}
        
        liste = sorted(liste, key=lambda x: x['rendement_moyen'], reverse=True)
        
        if best_parameters!={}: 
            
            
        
            resultat = await main_backtest(action, earnings,best_parameters['before_earning'], best_parameters['note'], best_parameters['TP'], best_parameters['further_day'], True)  
            
            if liste!=[]:

                best_parameters=[]
                
                for combinaison in liste:
                    if round(combinaison['rendement_moyen'], 1)==round(resultat['total_yield'], 1):
                        best_parameters.append({'TP':combinaison['TP'], 'note':combinaison['note'], 'before_earning':combinaison['before_earning'], 'further_day':combinaison['further_day']})
            
            row = {'action': action, 'parameters': best_parameters}

            resultat['total_yield']=str(resultat['total_yield']).replace('.', ',') 
            row.update(resultat)
        writer.writerow(row)

    
    




