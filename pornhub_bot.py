# batch file on 500th line to be merged




import os
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download
import requests
from bs4 import *

#from config import OWNER, BOT_NAME, REPO_BOT, ARQ_API_KEY, UPDATES_CHANNEL, TOKEN

#bot1 = Client(f"{BOT_NAME}", bot_token=f"{TOKEN}", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")


#------
# Config Check-----------------------------------------------------------------

# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()


arq = ARQ("http://arq.hamker.dev", "DIBVUP-JJRWWE-ZHCSHM-UWEHXH-ARQ", session)
pornhub = arq.pornhub

bot1 = Client("kakashibot", 2573805, "493592bc787a8ba7874dbfc8f0307d7b")



db = {}

# Let's Go----------------------------------------------------------------------
@bot1.on_message(filters.command(["search"]) & ~filters.command("help") & ~filters.command("start") & ~filters.command("repo"))
async def sarch(_,message):
    m = await message.reply_text("finding your desirable video...")
    search = message.text.split(' ', 1)[1]
    try:
        resp = await pornhub(search,thumbsize="large_hd")
        res = resp.result
    except:
        await m.delete()
        pass
    if not resp.ok:
        await m.edit("error search or link detected.")
        return
    resolt = f"""
**➡️ TITLE:** {res[0].title}
**⏰ DURATION:** {res[0].duration}
**👁‍🗨 VIEWERS:** {res[0].views}
**🌟 RATING:** {res[0].rating}
"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("NEXT",
                                         callback_data="next"),
                    InlineKeyboardButton("LINK",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad"),
               
                ]               
            ]
        )
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
@bot1.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss")
                    
                ],
                [
                    InlineKeyboardButton("LINK",
                                         callback_data="delete"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad")
              
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("NEXT",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("LINK",
                                         callback_data="delete"),
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad"),
              
                    
                ]
              ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[cur_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}
"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        
    )
 
# Previous Button-------------------------------------------------------------------------- 
@bot1.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("NEXT",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("LINK",
                                         callback_data="delete"),
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad")
              
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("NEXT",
                                         callback_data="next"),
                    InlineKeyboardButton("LINK",
                                         callback_data="Delete"),
                ],
                [ 
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad"),
              
                ]
                
            ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[cur_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}
"""
    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        
    )


# Delete Button-------------------------------------------------------------------------- 
#@bot1.on_callback_query(filters.regex("delete"))
@bot1.on_callback_query(filters.regex("delete"))
def callback_query_delete(bot, query):
    #await query.message.delete()
     data = db[query.message.chat.id]
     res = data['result']
     curr_page = int(data['curr_page'])
     cur_page = curr_page-1
     db[query.message.chat.id]['curr_page'] = cur_page
     umrl = res[curr_page].url
     bot.send_message(text=umrl,chat_id=query.message.chat.id,disable_web_page_preview=True)



# SCREENSHOT BUTTON ---------------------------------------

@bot1.on_callback_query(filters.regex("ss"))
async def callback_query_delete(bot, query):
    data = db[query.message.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    ss = res[curr_page].thumbnails
    for src in ss:
      await bot.send_photo(photo=src.src,chat_id=query.message.chat.id)



# DOWNLOAD BUTTON ------------------------------------------

import requests, os, validators
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton




def downloada(url, quality):
  
    if quality == "2":
        ydl_opts_start = {
            'format': 'best', #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'bot/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
    
@bot1.on_callback_query(filters.regex("downbad"))
def webpage(c, m): # c Mean Client | m Mean Message
    print(m.message.chat.id)
    data = db[m.message.chat.id]
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1

    vidtitle = data['result'][curr_page].title
    vidurl = data['result'][curr_page].url
    
    url1 = res = data['result'][curr_page].url
    if validators.url(url1):
        sample_url = "https://da.gd/s?url={}".format(url1)
        url = requests.get(sample_url).text
    

  
    global check_current
    check_current = 0
    def progress(current, total): #Thanks to my dear friend Hassan Hoot for Progress Bar :)
        global check_current
        if ((current//1024//1024) % 50 )== 0 :
            if check_current != (current//1024//1024):
                check_current = (current//1024//1024)
                upmsg.edit(f"{current//1024//1024}MB / {total//1024//1024}MB Uploaded.")
        elif (current//1024//1024) == (total//1024//1024):
            upmsg.delete()

   
    url1=f"{url} and 2"
    chat_id = m.message.chat.id
    data = url1
    url, quaitly = data.split(" and ")
    dlmsg = c.send_message(chat_id, '`downloading video..`')
    path = downloada(url, quaitly)
    upmsg = c.send_message(chat_id, '`uploading video..`')
    dlmsg.delete()
    thumb = path.replace('.mp4',".jpg",-1)
    if  os.path.isfile(thumb):
        thumb = open(thumb,"rb")
        path = open(path, 'rb')
        #c.send_photo(chat_id,thumb,caption=' ') #Edit it and add your Bot ID :)
        c.send_video(chat_id, path, thumb=thumb, caption=f'[{vidtitle}]({vidurl})',
                    file_name=" ", supports_streaming=True, progress=progress) #Edit it and add your Bot ID :)
        upmsg.delete()
        os.remove(path.name)
    else:
        path = open(path, 'rb')
        c.send_video(chat_id, path, caption=f'[{vidtitle}]({vidurl})',
                    file_name=" ", supports_streaming=True, progress=progress)
        upmsg.delete()
        os.remove(path.name)




def pagedata(link):
	
	r = requests.get(link)
	#print(r)
	soup = BeautifulSoup(r.text, 'html.parser')
	yy = (soup.find_all('div',{"class": 'phimage'}))
	#print(len(yy))
	
	details =[]
	
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
		
	#print(details)



def downloadab(url):
  
    
        ydl_opts_start = {
            'format': 'best', #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'



@bot1.on_message(filters.command(["batch"]) & filters.user(828632672))
def sarch(c,message):
    m = message.reply_text("getting videos...")
    search = message.text.split(' ', 1)[1]
    
    links = []
    names = []
    durs = []
    thumbs = []
    views = []
    ratings = []
    allvid = pagedata(search)
    
    for i in range(0,len(allvid)):
       links.append(allvid[i]["link"])
       names.append(allvid[i]["title"])
       durs.append(allvid[i]["duration"])
       thumbs.append(allvid[i]["thumb"])
       views.append(allvid[i]["views"])
       ratings.append(allvid[i]["rating"])
       
    #message.reply(links)
    #message.reply(names)
    
    
    
    
    for (vidtitle,vidurl,dur,thumb,view,rating) in zip(names,links,durs,thumbs,views,ratings):
    	url1 = vidurl
    	if validators.url(url1):
    	   sample_url = "https://da.gd/s?url={}".format(url1)
    	   url = requests.get(sample_url).text
    	   
    	global check_current
    	check_current = 0
    	def progress(current, total):
    	   global check_current
    	   if ((current//1024//1024) % 50 )== 0 :
    	           if check_current != (current//1024//1024):
    	           	check_current = (current//1024//1024)
    	           	upmsg.edit(f"{current//1024//1024}MB / {total//1024//1024}MB Uploaded.")
    	           elif (current//1024//1024) == (total//1024//1024):
    	           	upmsg.delete()
    	url1=f"{url}"
    	chat_id = message.chat.id
    	
    	url =url1
    	dlmsg = c.send_message(chat_id, f'`downloading` **{vidtitle}**.')
    	path = downloadab(url)
    	print(path)
    	upmsg = c.send_message(chat_id, f'`uploading` **{vidtitle}**.')
    	dlmsg.delete()
    	
    	img_data = requests.get(thumb).content
    	with open('thumb.jpg', 'wb') as handler:
    		handler.write(img_data)
    	
    	path = open(path, 'rb')
    	c.send_video(chat_id, path,thumb="thumb.jpg",caption=f'[{vidtitle}]({vidurl})\n\n**duration:** `{dur}`\n**views:** `{view}`\n**ratings:** `{rating}`',file_name=f"{vidtitle}", supports_streaming=True, progress=progress) #Edit it and add your Bot ID :)
    	upmsg.delete()
    	os.remove(path.name)




#  pornstar info

def infowebhtml(name):
	url = f"https://pornstarbyface.com/girls/{name}"
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')    
	
	return soup
	
	
def starinfo(name):
	
	name = name.replace(" ","-")
	soup = infowebhtml(name)
	img = "https://pornstarbyface.com" + (soup.find_all("img",{"class":"img-responsive"}))[1]["src"].replace(" ","%20")
	
	info = (soup.find("div",{"class":"star-info"})).find_all("div")
	
	

	jsondata = {
	
	"img" : img,
	info[2].text : info[3].text,
	info[4].text : info[5].text,
	info[6].text : info[7].text,
	info[8].text : info[9].text,
	info[10].text : info[11].text,
	info[12].text : info[13].text,
	info[14].text : info[15].text,
	info[16].text : info[17].text,
	info[18].text : info[19].text,
	info[20].text : info[21].text
	
	}
	
	return jsondata
	
	
@bot1.on_message(filters.command("info"))
def starinfocom(c,message):
	
	name = message.text.split(" ",1)[1]
	data = starinfo(name)
	
	message.reply_photo(data["img"],caption=str(data).replace(",","\n").replace("'","").replace("{","").replace("}",""))
	

bot1.run()










import requests, os, validators
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton

import os
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download

import requests
from bs4 import *
from time import sleep
def pagedata(lin,page):
  
  likks = []
  for i in range(1,int(page)+1):
  	likks.append(f"{lin}/videos?page={i}")
  
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
		
  #print(details)


#print(pagedata("https://www.pornhub.com/channels/step-siblings-caught"))



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

def popstar():
	
	popular = []
	
	url = "https://www.pornhub.com/pornstars?o=t"
	soup = BeautifulSoup(requests.get(url).text,"html.parser")
	allstar = soup.find("ul",{"id":"popularPornstars"}).find_all("li")
	
	for i in range(1,26):
		name = allstar[i].find_all("span")[5].text.strip()
		videos = allstar[i].find("div",{"class":"performerVideosViewsCount"}).find_all("span")[0].text.strip()
		views = allstar[i].find("div",{"class":"performerVideosViewsCount"}).find_all("span")[1].text.strip()
		thumb = allstar[i].find("img")["data-thumb_url"]
		link = "https://www.pornhub.com"+allstar[i].find("a")["href"]
		
		jsondata = {
		
		"name"     : name,
		"thumb"    : thumb,
		"videos"   : videos,
		"views"    : views,
		"link"     : link
		
		}
		
		popular.append(jsondata)
	
	return popular


bot1 = Client("kakashibot", 2573805, "493592bc787a8ba7874dbfc8f0307d7b")



def downloada(url,quality):
    
    print(quality)
        
    if quality == "1080":
        ydl_opts_start = {
            'format': 'best',  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
        
    elif quality == "720":
        ydl_opts_start = {
            'format': "best[height=720]",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
        
        
    elif quality == "480":
        ydl_opts_start = {
            'format': "best[height=480]",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'


    elif quality == "360":
        ydl_opts_start = {
            'format': "best[height=360]",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'


    elif quality == "240":
        ydl_opts_start = {
            'format': "best[height=240]",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'



def downloadadl(url,quality):
    
    print(quality)
        
    if quality == "1080":
        ydl_opts_start = {
            'format': 'best',  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
        
    elif quality == "720":
        ydl_opts_start = {
            'format': "best[height=720]",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
        
        
    elif quality == "480":
        ydl_opts_start = {
            'format': "best[height=480]",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'


    elif quality == "360":
        ydl_opts_start = {
            'format': "best[height=360]",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'


    elif quality == "240":
        ydl_opts_start = {
            'format': "best[height=240]",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'


    elif quality == "144":
        ydl_opts_start = {
            'format': "worst",  #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'



@bot1.on_message(filters.command("ping", prefixes= '.'))
def pingre(bot,message):
	ping = requests.get("https://kevs.onrender.com")
	message.reply(f"pinged render successfully\n\nstatus: {ping}")




@bot1.on_message(filters.command(["batch"]) & filters.user(828632672))
def sarch(c,message):
    m = message.reply_text("getting videos...")
    mes = message.text.split(' ')
    print(mes)
    search = mes[1]
    laspag = mes[2]
    fm = mes[3]
    quality = mes[4]
    print(fm)
    links = []
    names = []
    durs = []
    thumbs = []
    views = []
    ratings = []
    allvid = pagedata(search,laspag)
    print(len(allvid))
    m.edit(f"getting {len(allvid)} videos")
    
    for i in range(int(fm),len(allvid)):
       #allvid = json.loads(allvi[i])
       links.append(allvid[i]["link"])
       names.append(allvid[i]["title"])
       durs.append(allvid[i]["duration"])
       thumbs.append(allvid[i]["thumb"])
       views.append(allvid[i]["views"])
       ratings.append(allvid[i]["rating"])
       
    #message.reply(links)
    #message.reply(names)
    print("got data")
    
    
    
    
    for (vidtitle,vidurl,dur,thumb,view,rating) in zip(names,links,durs,thumbs,views,ratings):
    	requests.get("https://kevs.onrender.com")
    	url1 = vidurl
    	if validators.url(url1):
    	   sample_url = "https://da.gd/s?url={}".format(url1)
    	   url = requests.get(sample_url).text
    	   
    	global check_current
    	check_current = 0
    	def progress(current, total):
    	   global check_current
    	   if ((current//1024//1024) % 50 )== 0 :
    	           if check_current != (current//1024//1024):
    	           	check_current = (current//1024//1024)
    	           	upmsg.edit(f"{current//1024//1024}MB / {total//1024//1024}MB Uploaded.")
    	           elif (current//1024//1024) == (total//1024//1024):
    	           	upmsg.delete()
    	url1=f"{url}"
    	chat_id = message.chat.id
    	
    	url =url1
	    #print(url)
    	dlmsg = c.send_message(chat_id, f'`downloading` **{vidtitle}**.')
    	path = downloada(url,quality)
    	print(path)
    	upmsg = c.send_message(chat_id, f'`uploading` **{vidtitle}**.')
    	dlmsg.delete()
    	filename = f"{vidtitle}"+" {~Kev~}"
    	
    	img_data = requests.get(thumb).content
    	with open('thumb.jpg', 'wb') as handler:
    	   	handler.write(img_data)
    	   	
    	path = open(path, 'rb')
    	c.send_video(chat_id, path,thumb="thumb.jpg",caption=f'[{vidtitle}]({vidurl})\n#{quality}p\n\n**duration:** `{dur}`\n**views:** `{view}`\n**ratings:** `{rating}`',file_name=f"{filename}", supports_streaming=True, progress=progress) #Edit it and add your Bot ID :)
    	upmsg.delete()
    	os.remove(path.name)



@bot1.on_message(filters.command("ddl"))
def ddldl(c,message):
	
	mes = message.text.split(" ")
	link = mes[1]
	quality = mes[2]
	
	def reple(text):
		repled = str(text).replace("['","").replace("']","").replace("'","")
		return repled
		
	info = videodata(link)
	
	requests.get("https://kevs.onrender.com")
	url1 = link
	if validators.url(url1):
	   	   sample_url = "https://da.gd/s?url={}".format(url1)
	   	   url = requests.get(sample_url).text
	   	   
	global check_current
	check_current = 0
	def progress(current, total):
	   	   global check_current
	   	   if ((current//1024//1024) % 50 )== 0 :
	   	           	if check_current != (current//1024//1024):
	   	           		check_current = (current//1024//1024)
	   	           		upmsg.edit(f"{current//1024//1024}MB / {total//1024//1024}MB Uploaded.")
	   	           	elif (current//1024//1024) == (total//1024//1024):
	   	           		upmsg.delete()
	   	           		
	url1=f"{url}"
	chat_id = message.chat.id
	url =url1
	#print(url)
	dlmsg = c.send_message(chat_id, f'`downloading` **{info[0]["title"]}**.')
	path = downloadadl(url,quality)
	print(path)
	upmsg = c.send_message(chat_id, f'`uploading` **{info[0]["title"]}**.')
	dlmsg.delete()
	filename = info[0]["title"]+" {~Kev~}"
	
	thumb = path.replace("mp4","jpg")
	thum = open(thumb, 'rb')
	path = open(path, 'rb')
	
	likey = info[0]["likes"]
	dislikey = info[0]["dislikes"]
	lovey = info[0]["favorite"]
	
	pstar = reple(info[0]["pornstars"])
	print(pstar)
	catss = reple(info[0]["categories"])
	print(catss)
	c.send_video(chat_id, path,thumb=thum, caption=f'[{info[0]["title"]}]({link})\n#{quality}p\n\n**views:** `{info[0]["views"]}`\n**ratings:** `{info[0]["rating"]}`\n**likes:** `{likey}`    **dislikes:** `{dislikey}`\n**loved♥:** `{lovey}`\n**pornstars:** `{pstar}`\n**categories:** `{catss}`',file_name=f"{filename}", supports_streaming=True, progress=progress) #Edit it and add your Bot ID :)
	upmsg.delete()
	os.remove(path.name)
	
	
@bot1.on_message(filters.command("pop"))
def poplar(c,message):
	
	popall = popstar()
	mess = message.reply("parsing..")
	reply = ""
	for i in range(0,24):
		
		name = popall[i]["name"]
		vide = popall[i]["videos"]
		view = popall[i]["views"]
		link = popall[i]["link"]
		
		reply = reply + f"{i+1}. [{name}]({link})\n`{vide}   {view}`\n\n"
		mess.edit(reply,disable_web_page_preview=True)
		time.sleep(3)

bot1.run()
