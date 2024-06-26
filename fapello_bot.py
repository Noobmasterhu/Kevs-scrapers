# need some work

import requests
from bs4 import *
import requests
from bs4 import *
from pyrogram import *
import time
import random
import json
import os
from time import sleep

bot1 = Client("kakashibot", 2573805, "493592bc787a8ba7874dbfc8f0307d7b")


@bot1.on_message(filters.command("fap"))
def imgs(bot, message):
	
	tag = (message.text).lower().split(" ",1)[1]
	l1 = str(tag)[0]
	l2 = str(tag)[1]
	print(tag)
	print(l1,l2)
	
	
	r = requests.get(f"https://fapello.com/{tag}/")
	soup = BeautifulSoup(r.text, 'html.parser')    
	#h = (soup.find_all('img',{"class": "w-full h-full absolute object-cover inset-0"}))
	h = (soup.find_all("div",{"class": "flex lg:flex-row flex-col"}))
	total = int(h[0].text.replace("Media",""))
	oh = message.reply(f"uploading {total} files..")

	for i in range(1,total+1):
	    	lent= f"{i:04}"
	    	
	    	#print(f"https://fapello.com/content/{l1}/{l2}/{tag}/{(int(str(lent)[0]))+1}000/{tag}_{i:04}.jpg")
	    	
	    	try:
	    			sleep(1)
	    			bot1.send_photo(message.chat.id,f"https://fapello.com/content/{l1}/{l2}/{tag}/{(int(str(lent)[0]))+1}000/{tag}_{i:04}.jpg",caption=i)
	    			bot1.send_document(message.chat.id,f"https://fapello.com/content/{l1}/{l2}/{tag}/{(int(str(lent)[0]))+1}000/{tag}_{i:04}.jpg",caption=i)
	    	except:
	    			pass
	    			
	    	try:
	    			bot1.send_video(message.chat.id,f"https://fapello.com/content/{l1}/{l2}/{tag}/{(int(str(lent)[0]))+1}000/{tag}_{i:04}.mp4",caption=i)
	    	except:
	    			pass
	    			
	oh.edit(f"uploaded {total} files.")	     	
     	   	
bot1.run()    	   	    	 
