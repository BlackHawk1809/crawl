import shutil
import bs4
import requests

url="https://www.imdb.com/list/ls002913270/"
response = requests.get(url)
#print(type(response))
#print(response.text)
filename ="temp.html"
bs = bs4.BeautifulSoup(response.text,"html.parser")

formatted_text = bs.prettify()
#print(formatted_text)

try:
    with open(filename, "w+") as f:
        f.write((formatted_text))
except Exception as e:
    print(e)

list_imgs=bs.find_all('img')
no_of_imgs = len(list_imgs)
list_as = bs.find_all('a')
no_of_as = len(list_as)
print("number of img tags ",no_of_imgs)
print("number of anchor tags ",no_of_as)

j=1
for imgTag in list_imgs:
    #print(imgTag)
    try:
        imgLink = imgTag.get('src')
        #print(imgLink)
        ext = imgLink[imgLink.rindex('.'):]
        if ext.startswith(".png"):
            ext = ".png"
        elif ext.startswith(".jpeg"):
            ext = ".jpeg"
        elif ext.startswith(".jpg"):
            ext = ".jpg"
        elif ext.startswith(".svg"):
            ext = ".svg"


        filen = str(j)+ext
        res = requests.get(imgLink,stream=True)

        with open(filen,"wb") as file:
            shutil.copyfileobj(res.raw,file)
    except Exception as e:
        print(e)
    j = j + 1