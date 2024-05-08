from bs4 import BeautifulSoup
import requests

def get_live_data(stock_name):

    url=f'https://in.tradingview.com/symbols/ETHUSD/'
    response = requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')

    price=soup.find_all(class_='last-JWoJqCpY js-symbol-last')
    

    print(price)

   

    # code to get live data from website
    return "live data"