import requests
from bs4 import *


def paintin(name):
	 
	 paintingurl=[]
	 allpaint = []
	 tele =[]
	 
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
	     
	     
def artist(name):
	 
	 period = []
	 artistinfo=[]
	 
	 url = f"https://www.wikiart.org/en/{name}"
	 r = requests.get(url)
	 soup = BeautifulSoup(r.text, 'html.parser')
	 infos = (soup.find_all('div',{"class": "wiki-layout-artist-info"}))[0]
	 
	 image = (infos.find_all('div',{"class": "wiki-layout-artist-image-wrapper"}))[0].find_all("img")[0]["src"]

	 bdate = infos.find_all('span',{"itemprop": "birthDate"})[0].text	 
	 bplace = infos.find_all('span',{"itemprop": "birthPlace"})[0].text
	 
	 try:
	 	ddate = infos.find_all('span',{"itemprop": "deathDate"})[0].text
	 except:
	 	ddate = " "
	 
	 try:
	 	dplace = infos.find_all('span',{"itemprop": "deathPlace"})[0].text
	 except:
	 	dplace = " "
	 	
	 nation = infos.find_all('span',{"itemprop": "nationality"})[0].text
	 per = infos.find_all("li",{"class":"dictionary-values"})[1].find_all("a")
	 
	 for i in range(0,len(per)):
	 	period.append(per[i].text)
	 
	 
	 wikip = infos.find_all("a",{"class":"truncate external"})[0]["href"]
	 
	 jsondata = {
	       "name":name,
	       "image":image,
	       "birthday":bdate,
	       "birthplace":bplace,
	       "deathday":ddate,
	       "deathplace":dplace,
	       "nationality":nation,
	       "wikipedia":wikip,
	       "artper":period	       
	       }
	       
	 artistinfo.append(jsondata)
	 
	 return artistinfo
	       
	 
	     
print(artist("s-h-raza"))
