import pandas as pd
import sqlite3
import sqlalchemy
from bs4 import BeautifulSoup
import requests

conn =sqlite3.connect('restaurants.db')
cur = conn.cursor()

# cur.execute('CREATE TABLE food_network(Name TEXT, Address TEXT, Description TEXT)')
cur.execute('DROP TABLE IF EXISTS NAME')

sauce = requests.get('https://www.foodnetwork.com/restaurants/shows/diners-drive-ins-and-dives/a-z')
soup = BeautifulSoup(sauce.text, 'lxml')

name_list = []
address_list = []
desc_list = []

for article in soup.find_all('div', class_="m-MediaBlock o-Capsule__m-MediaBlock"):
        name = article.find('span', class_="m-MediaBlock__a-HeadlineText").text
        name_list.append(name)
        address = article.find("div", class_="m-Info__a-Address").text.lstrip()
        address_list.append(address)
        description = article.find('div', class_="m-MediaBlock__a-Description").text.lstrip()
        desc_list.append(description)
        if len(name_list) == 15:
            break

places = pd.DataFrame({'Name': name_list, 'Address' : address_list, 'Description' : desc_list})

engine = sqlalchemy.create_engine('sqlite:///restaurants.db')
places.to_sql('DDD', engine)





