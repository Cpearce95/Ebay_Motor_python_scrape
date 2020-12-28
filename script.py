##Imports
import pandas as pd 
import numpy as np 
import datetime
from datetime import *
import json
from bs4 import BeautifulSoup
import requests
import os

##Defining url requests headers
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

##Print start time
start_time = datetime.now()
print(f"Script starting at {start_time}")

##Define build urls list function
urls_list = []
def build_urls_list(): 
    pgn = 0
    url = f'https://www.ebay.co.uk/b/Cars-Motorcycles-Vehicles/9800/bn_1839671?rt=nc&_from=R40&_pgn={pgn}'
    for i in range(250):
        pgn += 1
        nw_url = f"{url}{pgn}"
        urls_list.append(nw_url)
        
##Scrape list of urls
titles,prices,bids,time_left,dates = [],[],[],[],[]
def scrape():
    for url in urls_list:
        r = requests.get(url,headers=headers, timeout=4)
        soup = BeautifulSoup(r.text, 'html.parser')
        for i in soup.find_all('li', attrs = {'class':'s-item'}):
            title = i.find('h3', class_='s-item__title').text
            price = i.find('span',class_='s-item__price').text
            bid = i.find('span',class_='s-item__bidCount')
            time = i.find('span',class_='s-item__time-left')
            titles.append(title)
            prices.append(price)  
            bids.append(bid.text if bid else '0')
            time_left.append(time.text if time else "NaN")
            dates.append(date.today())

##Call Functions            
build_urls_list()
scrape()

##Make dict from formed lists
dict = {'Date':dates,'Item_Name':titles,'Price':prices,'Bids':bids,'Time_Left':time_left}
df = pd.DataFrame(dict)

##Apply processing to convert data to desired data types
df['Price'] = df['Price'].map(lambda x: x.replace('£', '')).map(lambda x: x.replace(',', '')).apply(lambda x: x.replace('��', ''))
df['Bids'] = df['Bids'].apply(lambda x: x.replace('bids','')).apply(lambda x: x.replace('bid',''))
df['Price'] = df['Price'].astype(float)
df['Bids'] = df['Bids'].astype(int)
df['Item_Name'] = df['Item_Name'].apply(lambda x: x.title())

##Write data to json file
df.to_json('data.json')

##Print end time and num scraped rows
end_time = datetime.now()
print(f"Script ended at {end_time} and scraped {df.shape[0]} rows")