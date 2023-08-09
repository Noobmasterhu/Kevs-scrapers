import requests
from bs4 import *


def paintin(name):
	 
	 paintingurl=[]
	 allpaint = []
	 
	 url = f"https://www.wikiart.org/en/{name}/all-works/text-list"
	 r = requests.get(url)
	 soup = BeautifulSoup(r.text, 'html.parser')    
	 all = (soup.find_all('li',{"class": 'painting-list-text-row'}))
	 
	 for i in range(0,len(all)):
       paintingurl.append("https://www.wikiart.org"+(all[i].find_all('a'))[0]["href"])
	 	 
	 for url in paintingurl:
	     
	     r = requests.get(url)
	     soup = BeautifulSoup(r.text, 'html.parser')    
	     h = (soup.find_all('img',{"itemprop":"image"}))
	     
       title= (h[0]["title"])
	     iurl = (h[0]["src"])
	     
	     jsondata = {
	         "title":title,
	         "image":iurl.replace("!Large.jpg","")
	     }
	     
	     allpaint.append(jsondata)
	     
	 return allpaint


print(paintin("chuck-close"))
