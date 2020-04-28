import shutil
import sqlite3

import requests
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client



page_url = "https://www.imdb.com/list/ls002913270/"




uClient = uReq(page_url)

page_soup = soup(uClient.read(), "html.parser")
uClient.close()

containers = page_soup.findAll("div", {"class": "lister-item mode-detail"})
out_filename = "graphics_cards.csv"
#headers = "Personality Traits of Celebrities\n"

conn = sqlite3.connect(r"C:\Users\hp-p\PycharmProjects\beautifulsoup\bollywood.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bollywood_tb 
(name TEXT,desc TEXT, image BLOB)""")


j = 0
for container in containers:
    div_img = container.select('div', {"class": "lister-item-image"})
    image_tag = div_img[0].a.img
    image = None
    try:
        imgLink = image_tag.get('src')
        ext = imgLink[imgLink.rindex('.'):]
        if ext.startswith(".png"):
            ext = ".png"
        elif ext.startswith(".jpeg"):
            ext = ".jpeg"
        elif ext.startswith(".jpg"):
            ext = ".jpg"
        elif ext.startswith(".svg"):
            ext = ".svg"

        filen = str(j) + ext
        res = requests.get(imgLink, stream=True)

        with open(filen, "wb") as file:
            shutil.copyfileobj(res.raw, file)
        with open(filen, "rb") as file:
            image = file.read()
    except Exception as e:
        print(e)
    div = container.select('div', {"class": "lister-item-content"})
    name = div[1].select('a')[0].text
    content = div[1].select('p')[1].text
    try:
        cursor.execute(""" INSERT INTO bollywood_tb 
            (name, desc, image) VALUES (?,?,?)""", (name, content, image))
    except:
        print('err')

    j+=1

conn.commit()
cursor.close()
conn.close()