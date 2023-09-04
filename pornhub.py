import requests
from bs4 import *


def pagedata(lin,page):
  likks = []
  for i in range(1,page+1):
  	likks.append(f"https://www.pornhub.com/channels/bratty-sis/videos?page={i}")
  
  details =[]
  for link in likks:
    
    #print(link)
    r = requests.get(link)
    #print(r)
    soup = BeautifulSoup(r.text, 'html.parser')
    yy = (soup.find_all('div',{"class": 'phimage'}))
    #print(len(yy))
    
    
    
    for i in range(4,len(yy)):
    	test = (yy[i])
    	info = soup.find_all("div",{"class":"thumbnail-info-wrapper clearfix"})[i]
    	
    	if info.find_all("div",{"class":"rating-container neutral"}):
    		rats=info.find_all("div",{"class":"rating-container neutral"})[0].text.strip()
    		
    	else:
    		rats=" "
    		
    	jsondata = {
		"title":test.find_all('a')[0]["title"],
		"link":"https://www.pornhub.com"+test.find_all('a')[0]["href"],
		"duration":test.find_all('var')[0].text,
		"thumb":test.find_all('img')[0]["src"],
		"views": info.find_all("span",{"class":"views"})[0].text,
		"rating": rats
		}
		
    	details.append(jsondata)
    	
  return details
		


#print(pagedata("https://www.pornhub.com/channels/bratty-sis",5))


def videodata(link):
	
	r = requests.get(link)
	print(r)
	soup = BeautifulSoup(r.text, 'html.parser')
	
	yy = (soup.find_all('div',{"class": 'video-actions-menu'}))
	
	stars=[]
	cats=[]
	videoinfo = []
	
	title = (soup.find_all("h1",{'class':"title"})[0].text).strip()
	views =(yy[0].find_all("div",{'class':"views"})[0].text)
	rating =(yy[0].find_all("div",{'class':"ratingPercent"})[0].text)
	uploaded =(yy[0].find_all("div",{'class':"videoInfo"})[0].text)
	likes =(yy[0].find_all("span",{'class':"votesUp"})[0].text)
	dislikes =(yy[0].find_all("span",{'class':"votesDown"})[0].text)
	favorite =(yy[0].find_all("span",{'class':"favoritesCounter"})[0].text).strip()
	
	pstar = (soup.find_all('a',{"class": "gtm-event-link pstar-list-btn js-mxp"}))
	for i in range(0,len(pstar)):
		stars.append(str(pstar[i].text).strip())
		
	cater = (soup.find_all('div',{"class": 'video-info-row showLess'}))
	cat = cater[0].find_all('a',{"class":"gtm-event-link item"})
	
	for i in range(0,len(cat)):
		cats.append((cat[i].text))
	
	jsondata ={
	    "title":title,
    	"views":views,
		"rating":rating,
		"upload":uploaded,
		"likes":likes,
		"dislikes":dislikes,
		"favorite":favorite,
		"pornstars":stars,
		"categories":cats
		}
		
	videoinfo.append(jsondata)
	return videoinfo
	
	
#print(videodata("https://www.pornhub.com/view_video.php?viewkey=64caf75b2d887"))

