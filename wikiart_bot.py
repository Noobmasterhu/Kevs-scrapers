import datetime
import requests
from bs4 import *
from pyrogram import *
import time
from time import sleep
import random
import json
import os
from telegraph import Telegraph
from datetime import datetime as dt 
from pyrogram.types import *

telegraph = Telegraph()
telegraph.create_account(short_name='637')

bot1 = Client(" ", , " ")


##  >>  WIKIART SCRAP

#   > all paintings


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
	     print(f"got {title}")
	     iurl = (h[0]["src"])
	     
	     jsondata = {
	         "title":title,
	         "image":iurl.replace("!Large.jpg","")
	     }
	     
	     allpaint.append(jsondata)
	     
	 return allpaint


#  > artist's info	 	 	 	 
	 	 	 
def artist(name):
	 
	 period = []
	 
	 jname = name.replace("-"," ")
	 
	 url = f"https://www.wikiart.org/en/{name}"
	 r = requests.get(url)
	 soup = BeautifulSoup(r.text, 'html.parser')
	 infos = (soup.find_all('div',{"class": "wiki-layout-artist-info"}))[0]
	 
	 image = (infos.find_all('div',{"class": "wiki-layout-artist-image-wrapper"}))[0].find_all("img")[0]["src"]

	 try:
	 	bdate = infos.find_all('span',{"itemprop": "birthDate"})[0].text	 
	 except:
	 	bdate = " "
	 
	 try:
	 	bplace = infos.find_all('span',{"itemprop": "birthPlace"})[0].text
	 except:
	 	bplace = " "
	 
	 try:
	 	ddate = infos.find_all('span',{"itemprop": "deathDate"})[0].text
	 except:
	 	ddate = " "
	 
	 try:
	 	dplace = infos.find_all('span',{"itemprop": "deathPlace"})[0].text
	 except:
	 	dplace = " "
	 	
	 try:
	 	nation = infos.find_all('span',{"itemprop": "nationality"})[0].text
	 except:
	 	nation = " "
	 	
	 per = infos.find_all("li",{"class":"dictionary-values"})[1].find_all("a")
	 
	 for i in range(0,len(per)):
	 	period.append(per[i].text)
	 
	 
	 try:
	 	wikip = infos.find_all("a",{"class":"truncate external"})[0]["href"]
	 except:
	 	wikip = "https://www.wikipedia.org"
	 	
	 jsondata = {
	       "name":jname,
	       "image":image,
	       "birthday":bdate,
	       "birthplace":bplace,
	       "deathday":ddate,
	       "deathplace":dplace,
	       "nationality":nation,
	       "wikipedia":wikip,
	       "artperiod":period	       
	       }
	       
	 
	 
	 return jsondata
	


##  >> MAIN BOT


@bot1.on_message(filters.text & filters.chat("preciousarts"))
def getart(bot,m):
	print(m.text)
	
	st = dt.now()
	nam = m.text.lower()
	name = nam.replace(" ","-")
	fm = bot.send_message(m.chat.id,f"`getting {nam}'s artworks..`")
	data = artist(name)
	data1 = paintin(name)
	m.delete()
	tele =[]
	lm = bot.get_messages("preciousarts", 20)

	artag = str([naam[0] for naam in nam.split(" ")]).replace("['",'').replace("']",'').replace("', '","").upper() + str(len(data1))
	
	wurl = data["wikipedia"]
	waurl = "https://www.wikiart.org/en/"+name
	butt=[
		       [
		         InlineKeyboardButton("WIKIPEDIA",url=wurl)
		       ],
		       
		       [
		         InlineKeyboardButton("WIKIART",url=waurl)
		       ]
		       
		 ]
		     
	key= InlineKeyboardMarkup(butt)
	bot.send_photo(m.chat.id,data["image"],caption=f"""`Artist Name` : **{nam}**\n\n`Birth` : **{data["birthday"]}** ({data["birthplace"]})\n\n`Death` : **{data["deathday"]}** ({data["deathplace"]})\n\n`Art Period` : **{str(data["artperiod"]).replace("[","").replace("]","").replace("'","")}**\n\n`Nationality` : **{data["nationality"]}**\n\n[#{artag}]""",reply_markup=key)
	
	sm = bot.send_message(m.chat.id,"list will appear here.")
	
	jfile = {
		"artist":data,
		"artworks":data1
		
	}
	
	jsonFile = open(f"{nam}'s database ~Kev~.json", "w")
	jsonFile.write(str(json.dumps(jfile,indent=4)))
	jsonFile.close()
	
	bot.send_document(m.chat.id,f"{nam}'s database ~Kev~.json")
	
	for painting in data1:
		
		tele.append("<li>"+painting["title"]+"</li>")
		print(f"""sent {painting["image"]}""")
		bot.send_message("piperidine",f"""sent {painting["image"]}""")
		
		try:
			sleep(2)
			bot.send_photo(m.chat.id,f"""{painting["image"]}""",caption=painting["title"])
			bot.send_document(m.chat.id,painting["image"],caption=painting["title"])
			#print(f"""sent {painting["title"]}""")
			
		except:
		  
		  try:
		    with open(f"""/storage/emulated/0/{painting["title"]} ~Kev~.jpg""", 'wb') as f:
		              r = requests.get(painting["image"], "wb")
		              for chunk in r.iter_content(chunk_size = 1024*1024):
		              	if chunk:
		              		f.write(chunk)
		              		
		    bot.send_photo(m.chat.id,f"""{painting["image"]}!Large.jpg""",caption=painting["title"])          		
		    bot.send_document(m.chat.id,f"""/storage/emulated/0/{painting["title"]} ~Kev~.jpg""",caption=painting["title"])
		    os.remove(f"""/storage/emulated/0/{painting["title"]} ~Kev~.jpg""")
		  
		  except:
		  	pass
		
		
			
	alllist = str(tele).replace("', '","").replace("['","").replace("']","").replace(",","").replace('["','').replace('"','')
	
	response = telegraph.create_page(
        f"{nam}'s paintings",
        author_name="{~Kev~}",
        html_content=f"<ol>{alllist}</ol>"
        )
        
	sm.edit(f"""[List of {nam}'s Artworks]({response["url"]})""")
	fm.delete()
	bot1.send_sticker(m.chat.id,"CAACAgUAAxkBAAEBGD5k1H20D-HxjDw3I_PUsLByddaUJgACaAIAAlZwQFTv2oBVKHOz1jAE")
	tele.clear()
	bot1.edit_message_text("preciousarts",20,f"**{lm.text}\n• {nam} [#{artag}]**")
	et = dt.now()
	pt = (et-st).seconds / 60
	bot1.send_message("piperidine",f"took {pt} minutes.")
	
bot1.run()

