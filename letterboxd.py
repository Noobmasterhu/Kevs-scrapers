# masty with letterboxd

import requests
from bs4 import *
import re
import json



def soupp(link):
	
	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	return soup

# to scrap specific movie details
	
def alldata(name):
	 
	 filam = name.replace(" ","-")
	 print(filam)
	 url = f"https://letterboxd.com/film/{filam}/"
	 r = requests.get(url)
	 soup = BeautifulSoup(r.text, 'html.parser')    
	 all = (soup.find_all('div',{"class": 'col-17'}))[0]
	 #print(all)
	 
	 staturl = f"https://letterboxd.com/film/{filam}/members/"
	 statr = requests.get(staturl,timeout=(5, 10))
	 statsoup = BeautifulSoup(statr.text, 'html.parser')
	 allstats = (statsoup.find_all("ul",{"class": "sub-nav"}))[0]

	 try:
	 	jd = soup.find_all("script",{"type":"application/ld+json"})[0].find(text=re.compile("CDATA")).string.strip().replace("*/","").replace("/*","").replace("<![CDATA[","").replace("]]>","")
	 	jsondata = json.loads(jd)
	 except:
	 	pass
	 
	 try:
	 	title = all.find_all("h1")[0].text
	 except:
	 	title = jsondata["name"]
	 
	 try:
	 	cover = soup.find_all('div',{"id": "backdrop"})[0]["data-backdrop"]
	 except:
	 	cover = " "
	 
	 try:
	 	poster = jsondata["image"].replace("230","500").replace("345","750")
	 except:
	 	poster = " "
	 
	 try:
	 	year = all.find_all("small")[0].text
	 except:
	 	year = " "
	 	
	 try:
	 	director = all.find_all("span",{"class": "prettify"})[0].text
	 except:
	 	director = jsondata["director"][0]["name"]
	 
	 try:
	 	trailer = "https:"+soup.find_all("a",{"data-track-category":"Trailer"})[0]["href"]
	 except:
	 	trailer = " "
	 
	 try:
	 	runtime = int(''.join(c for c in soup.find_all("p",{"class":"text-link text-footer"})[0].text if c.isdigit()))
	 except:
	 	runtime = " "
	 
	 try:
	 	tagline = all.find_all("h4",{"class": "tagline"})[0].text
	 except:
	 	tagline = " "
	 
	 try:
	 	synopsis = all.find_all("div",{"class": "truncate"})[0].text.strip()
	 except:
	 	synopsis = " "
	 	
	 
	 actors = []
	 
	 try:
	 	ac = all.find_all("a",{"class": "text-slug tooltip"})
	 	
	 	for i in range(0,len(ac)):
	 		actorjson ={
	 		"name": ac[i].text,
	 		"role": ac[i]["title"]
	 		}
	 		actors.append(actorjson)
	 
	 except:
	 	ac = jsondata["actors"]
	 	
	 	for i in range(0,len(ac)):
	 		actors.append(ac[i]["name"])
	 
	 
	 genre = []
	 
	 try:
	 	ge = all.find_all("div",{"id":"tab-genres"})[0].find_all("p")[0].find_all("a")
	 	for i in range(0,len(ge)):
	 		genre.append(ge[i].text)
	 except:
	 	gene = jsondata["genre"]
	 	genre.append(gene)
	 
	 
	 themes = []
	 
	 try:
	 	th = all.find_all("div",{"id":"tab-genres"})[0].find_all("p")[1].find_all("a")
	 	for i in range(0,len(th)-1):
	 		themes.append(th[i].text)
	 except:
	 	pass
	 	
	 try:
	 	imdb = all.find_all("a",{"data-track-action":"IMDb"})[0]["href"]
	 except:
	 	imdb = " "
	 	
	 try:
	 	avgrating = jsondata["aggregateRating"]["ratingValue"]
	 except:
	 	avgrating = " "
	 
	 try:
	 	ratingcount = jsondata["aggregateRating"]["ratingCount"]
	 except:
	 	ratingcount = " "
	 
	 
	 topreview = []
	 
	 try:
	 	tp = all.find_all("section",{"class":"film-recent-reviews -clear"})[0].find_all("section")[0]
	 	
	 	for i in range(0,len(tp)):
	 		topreview.append(tp.find_all("div",{"class": "body-text -prose collapsible-text"})[i].text)
	 except:
	 	pass
	 	
	 	
	 try:
	 	watches = allstats.find_all("li",{"class": "js-route-watches"})[0].find_all("a")[0]["title"].strip()
	 except:
	 	watches = " "
	 try:
	 	fans = allstats.find_all("li",{"class": "js-route-fans"})[0].find_all("a")[0]["title"].strip()
	 except:
	 	fans = " "
	 
	 try:
	 	likes = allstats.find_all("li",{"class": "js-route-likes"})[0].find_all("a")[0]["title"].strip()
	 except:
	 	likes = " "
	 
	 try:
	 	reviews = allstats.find_all("li",{"class": "js-route-reviews"})[0].find_all("a")[0]["title"].strip()
	 except:
	 	reviews = " "
	 
	 try:
	 	lists = allstats.find_all("li",{"class": "js-route-lists"})[0].find_all("a")[0]["title"].strip()
	 except:
	 	lists = " "
	 
	 relatedfilms = []
	 similarfilms = []
	 
	 try:
	 	sf = all.find_all("section",{"class":"section related-films -clear"})
	 	if len(sf) == 2:
	 		ref = sf[0].find_all("li")
	 		for i in range(0,len(ref)):
	 			#print(sf[i].find_all("img")[0])
	 			url = "https://letterboxd.com/film/"+ref[i].find_all("div")[0]["data-film-slug"]
	 			
	 			sfdata ={
	 			"title": ref[i].find_all("img")[0]["alt"],
	 			"url": url
	 			} # json db
	 			relatedfilms.append(sfdata)
	 			
	 		sif = sf[1].find_all("li")
	 		for i in range(0,len(sif)):
	 			#print(sf[i].find_all("img")[0])
	 			url = "https://letterboxd.com/film/"+sif[i].find_all("div")[0]["data-film-slug"]
	 			
	 			sfdata ={
	 			"title": sif[i].find_all("img")[0]["alt"],
	 			"url": url
	 			} # json db
	 			similarfilms.append(sfdata)
	 			
	 	else:
	 		sif = sf[0].find_all("li")
	 		for i in range(0,len(sif)):
	 			#print(sf[i].find_all("img")[0])
	 			url = "https://letterboxd.com/film/"+sif[i].find_all("div")[0]["data-film-slug"]
	 			
	 			sfdata ={
	 			"title": sif[i].find_all("img")[0]["alt"],
	 			"url": url
	 			} # json db
	 			similarfilms.append(sfdata)
	 		
	 		
	 except:
	 	pass
	 	
	 
	 MOVIEJSON = {
	 
	 "title"          : title,
	 "releaseyear"    : year,
	 "poster"         : poster,
	 "cover"          : cover,
	 "trailer"        : trailer,
	 "runtime"        : runtime,
	 "tagline"        : tagline,
	 "synopsis"       : synopsis,
	 "director"       : director,
	 "actors"         : actors,
	 "genre"          : genre,
	 "themes"         : themes,
	 "imdb"           : imdb,
	 "averageratings" : avgrating,
	 "ratingcounts"   : ratingcount,
	 "watches"        : watches,
	 "likes"          : likes,
	 "fans"           : fans,
	 "lists"          : lists,
	 "topreviews"     : topreview,
	 "relatedmovies"  : relatedfilms,
	 "similarmovies"  : similarfilms
	 
	 
	 }
	 
	 
	 return MOVIEJSON

#print(alldata("barbie"))

# to scrap all the movies in the list
	
def bigjsondata(sit,pag):
	noshit = []
	allthemob = []
	for i in range(1,int(pag)+1):
		site = sit+f"page/{i}/"
		data = soupp(site).find_all("ul",{"class":"js-list-entries poster-list -p125 -grid film-list"})[0].find_all("li")
		print(len(data))
		#print(data[0])
		
		for mobi in data:
			title = mobi.find_all("div")[0]["data-film-slug"]
			allthemob.append(title)
			#print(title)
	
	for mov in allthemob:
			requests.get("https://kevs.onrender.com/")
			
			noshit.append(alldata(mov))         #json.dumps(alldata(mov), indent=4))
	
	with open("sample.json", "w") as outfile:
	   json.dump(noshit, outfile, indent=4)
	   
	return noshit

#bigjsondata("https://letterboxd.com/hershwin/list/all-the-movies/",308)

