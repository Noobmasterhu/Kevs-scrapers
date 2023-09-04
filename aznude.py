import requests
from bs4 import *


def aznude(na):
	
	name = (na.lower()).replace(" ", "")
	first = str(name)[0]
	
	
	r = requests.get(f"https://www.aznude.com/view/celeb/{first}/{name}.html")
	soup = BeautifulSoup(r.text, 'html.parser')    
	
	imagedata = []
	videodata = []
	
	azjson = []
	
	h = (soup.find_all('a',{"class": 'picture tt show-pic accessible'}))
	
	for i in range(0, len(h)):
	       jsondata = {
	       "name":h[i]["lightbox"].lower().replace(f"<small>{na}</small>",""),
	       "link":h[i]["href"]
	       }
	       
	       imagedata.append(jsondata)
	       
	v = soup.find_all('a',{"class": 'video animate-thumb tt show-clip'})
	
	for i in range(0, len(v)):
	       jsondata = {
	       "name":v[i]["lightbox"].lower().replace(f"<small>{na}</small>",""),
	       "link":f"""https://cdn2.aznude.com/{v[i]["href"].replace("/azncdn","").replace(".html","")}.mp4"""
	       }
	       
	       videodata.append(jsondata)
	
	alljson ={
	"images" : imagedata,
	"videos" : videodata
	
	}
	azjson.append(alljson)
	
	return azjson
            
	      

#print(aznude("florence pugh"))
