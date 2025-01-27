import json
import os

#bibliothèque permettant d'effectuer des requêtes HTTP de manière asynchrone
import aiohttp

from datetime import datetime, timedelta

async def news_recovery(day_news, symbol, start_date):

    news=await telecharger_donnees_alpha_vantage2(symbol, day_news, start_date)
    
    return news

async def telecharger_donnees_alpha_vantage2(symbol, day_news, start_date):

    news=[]

    data_directory = "dataNF"  # Répertoire pour stocker les données localement

    # Vérifier si le répertoire de données existe, sinon le créer
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)


    file_path = os.path.join(data_directory, f"{symbol}_{day_news}_news.json")
        
    if os.path.exists(file_path):
        # Charger les données à partir du fichier local
        with open(file_path, "r") as file:
            news = json.load(file)


    
    else:

        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&topics=earnings&time_from={day_news}&sort=EARLIEST&apikey=40N5RGVOW4H6UJZ4'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        day_news=date_obj = datetime.strptime(day_news, '%Y%m%dT%H%M%S')
        day_news=date_obj.date()     

        for article in data['feed']:
                    date_obj = datetime.strptime(article['time_published'], '%Y%m%dT%H%M%S')
                    time_str = date_obj.strftime('%H:%M:%S')  # Conversion en string
                    date_obj = date_obj.date()
                    if date_obj == day_news:
                        for ticker in article['ticker_sentiment']:
                            if ticker['ticker'] == symbol:
                                news.append({
                                    'time': time_str,  # Utilisation de la chaîne de caractères
                                    'relevance_score': float(ticker['relevance_score']),
                                    'sentiment_score': float(ticker['ticker_sentiment_score'])
                                })
        with open(file_path, "w") as file:
                json.dump(news, file)
    return news


#main fonction qui va récupérer les données OHLC de l'action donnée (par le symbole) pour des intervalles de temps d'OHLC
#précisés et une durée de backtest donnée.
async def ohlc_recovery(symbol, start_date, end_date):
    
    #les données sont téléchargées dans une variable data grâce à la fonction telecharger_donnees_alpha_vantage
    data = await telecharger_donnees_alpha_vantage(symbol, start_date, end_date)
    
    return data

async def telecharger_donnees_alpha_vantage(symbol,start_date, end_date):
    data_directory = "dataF"  # Répertoire pour stocker les données localement
    time_interval="60min"
    # Vérifier si le répertoire de données existe, sinon le créer
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    all_data = {}
    file_path = os.path.join(data_directory, f"{symbol}_OHLC.json")
        
    if os.path.exists(file_path):
        # Charger les données à partir du fichier local
        with open(file_path, "r") as file:
            all_data = json.load(file)
    
    else:
        
        for month in reversed(last_months(start_date, end_date)):
            
            # Télécharger les données depuis l'API Alpha Vantage
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={time_interval}&month={month}&outputsize=full&apikey=40N5RGVOW4H6UJZ4'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
            
            # Ajouter les données au dictionnaire global
            all_data.update(data_by_day(data[f'Time Series ({time_interval})']))
        # Sauvegarder les données localement
        with open(file_path, "w") as file:
            json.dump(all_data, file)

    
    return all_data

def last_months(start_date, end_date):


    #récupération de la date actuelle
    current_date = end_date
    result = []
    
    while current_date>start_date:
        month_str = current_date.strftime('%Y-%m')
        result.append(month_str)
        #recule d'un mois pour pouvoir y ajouter le précédent 
        current_date -= timedelta(days=current_date.day)
        #récupère le mois demandé dans le format adapté pour l'API d'Alpha Venture
        
    #print(result)
    return result

def data_by_day(donnees_brutes):
    # Dictionnaire de récupération des données journalières
    donnees_par_jour = {}

    # Parcours des données brutes
    for timestamp, valeurs in donnees_brutes.items():
        # Séparation de la date et de l'heure
        date, heure = timestamp.split(" ")

        # Création d'une nouvelle journée si elle n'existe pas encore
        if date not in donnees_par_jour:
            donnees_par_jour[date] = {}

        # Ajout des valeurs pour cette heure
        donnees_par_jour[date][heure] = valeurs

    # Inversion de l'ordre des heures dans chaque journée
    for date in donnees_par_jour:
        donnees_par_jour[date] = dict(reversed(list(donnees_par_jour[date].items())))

    # Inversion de l'ordre des jours du plus ancien au plus récent
    donnees_par_jour_inversees = dict(reversed(list(donnees_par_jour.items())))

    return donnees_par_jour_inversees



async def calendar_earnings(earnings, symbol):

    calendar=await telecharger_donnees_alpha_vantage3(symbol, earnings)

    return calendar


async def telecharger_donnees_alpha_vantage3(symbol, earnings):

    calendar=[]
    data_directory = "dataCF"  # Répertoire pour stocker les données localement

    # Vérifier si le répertoire de données existe, sinon le créer
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)


    file_path = os.path.join(data_directory, f"{symbol}_{earnings}_calendar.json")
        
    if os.path.exists(file_path):
        # Charger les données à partir du fichier local
        with open(file_path, "r") as file:
            calendar = json.load(file)
    else:
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey=40N5RGVOW4H6UJZ4'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        for i in range(earnings):
            date_str = data['quarterlyEarnings'][i]['reportedDate']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            # Convertir la date en chaîne de caractères
            if float(data['quarterlyEarnings'][i]['surprise'])>=0: 
                surprise=True
            else:
                surprise=False
            
            if data['quarterlyEarnings'][i]['reportTime']=='pre-market':
                time=True
            else:
                time=False
            
            calendar.append({'date':date_obj.isoformat(), 'surprise':surprise, 'time': time})

        with open(file_path, "w") as file:
            json.dump(calendar, file)

    #print(calendar)
    return calendar


async def ema_recovery(symbol):
    
    #les données sont téléchargées dans une variable data grâce à la fonction telecharger_donnees_alpha_vantage
    data = await telecharger_donnees_alpha_vantage4(symbol)
    data=data["Time Series (Daily)"]
    
    return data

async def telecharger_donnees_alpha_vantage4(symbol):
    data_directory = "dataEMA"  # Répertoire pour stocker les données localement
    
    # Vérifier si le répertoire de données existe, sinon le créer
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    data = {}
    file_path = os.path.join(data_directory, f"{symbol}_daily.json")
        
    if os.path.exists(file_path):
        # Charger les données à partir du fichier local
        with open(file_path, "r") as file:
            data = json.load(file)
    
    else:
        
        # Télécharger les données depuis l'API Alpha Vantage
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey=40N5RGVOW4H6UJZ4'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        # Sauvegarder les données localement
        with open(file_path, "w") as file:
            json.dump(data, file)

    return data