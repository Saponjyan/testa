# python -m pip install sqlite3-api
# pip install requests bs4 pysqlite3 lxml
import json
import os
import requests
from bs4 import BeautifulSoup
import sqlite3 as sq

with sq.connect("mydb.db") as con:
    cur = con.cursor()

# db = SQL("sqlite:///mydb.db")

# создаем таблицу если нет
cur.execute("CREATE TABLE IF NOT EXISTS info (domain varchar(15) NOT NULL, rating varchar(15) , reviews varchar(15) , downloads varchar(15) , age varchar(15));")

# читаем ссылки из json
with open(os.path.join(os.path.dirname(__file__), "urls.json"),"r", encoding="utf-8") as json_data:
    urls = json.load(json_data)

headers = ({'user-agent': 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'})


def scan(dom,url):
    """парсит каждую ссылку"""
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    meen = soup.find("div",class_="w7Iutd")
    meen = meen.text.split()
    dom = dom
        
    try:
        meen2 = meen[0].split('star')[1]
    except:
        meen2  = ''
        
    try:
        count = meen[0].split('star')[0]
    except:
        count = ''
        
    try:
        countinst = meen[1].split('+')[0].split('reviews')[1]
    except:
        countinst = 0
    try:
        age = meen[3].split('+')[0]
    except:
        age = ''
    cur.execute(f"INSERT INTO info VALUES('{dom}','{meen2}','{count}','{countinst}','{age}')")
    con.commit()

def main():
    for dom, url in urls.items():
        try:
            scan(dom,url)
        except:
            print("ERR")

if __name__ == "__main__":
    main()