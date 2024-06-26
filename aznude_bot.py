# some work needed

import requests
from bs4 import *
from pyrogram import *
import time
from time import sleep
import random
import json
import os

bot1 = Client("kakashibot", 2573805, "493592bc787a8ba7874dbfc8f0307d7b")

icap = []
vcap = []
list = []
vidlist=[]


@bot1.on_message(filters.command("az"))
def imgs(bot, message):
	
	na = (message.text).lower().split(" ",1)[1]
	name = na.replace(" ", "")
	first = str(name)[0]
	print(first)
	print(name)
	
	r = requests.get(f"https://www.aznude.com/view/celeb/{first}/{name}.html")
	soup = BeautifulSoup(r.text, 'html.parser')    
	
	h = (soup.find_all('a',{"class": 'picture tt show-pic accessible'}))
	
	for i in range(0, len(h)):
	       icap.append(h[i]["lightbox"].lower().replace(f"{na}",""))
	       list.append(h[i]["href"])
	       
	#print(list)
	      
	for (img,caps) in zip(list,icap):
	       	try:
	       		sleep(1)
	       		bot1.send_photo(message.chat.id,img,caption=f"from : `{caps}`")
	       	    #bot1.send_document(message.chat.id,img,caption=f"from : `{caps}`")
	       	except:
	       		pass
	      		
	div= soup.find_all('a',{"class": 'video animate-thumb tt show-clip'})
	
	for i in range(0, len(div)):
	       vidlist.append(f"""https://cdn2.aznude.com/{div[i]["href"].replace("/azncdn","").replace(".html","")}.mp4""")
	       vcap.append(div[i]["lightbox"].lower().replace(f"{na}",""))
	
	#print(vidlist)
	#print(vcap)
	   
	for (vid,caps) in zip(vidlist,vcap):
	       	try:
	       		sleep(1)
	       		bot1.send_video(message.chat.id,vid,caption=f"from : `{caps}`")
	       	except:
	       		pass
	
	message.reply(f"total uploaded {len(list)} photos and {len(vidlist)} videos.")
	
	list.clear()
	vidlist.clear()
	icap.clear()
	vcap.clear()
	


bot1.run()
