import requests
from bs4 import *


def books(authour):
	
	links=[]
	allbooks = []
	
	url = f"https://www.globalgreyebooks.com/{authour}-books.html"
	r = requests.get(url)
	s = BeautifulSoup(r.text, 'html.parser')
	b = (s.find_all('aside',{"class": "aside-books" }))
	
	for i in range(0,len(b)):
		links.append(b[i].find_all("a")[0]["href"])
		
	for url in links:
		category = []
		br = requests.get(url)
		bs = BeautifulSoup(br.text, 'html.parser')
		bb = (bs.find_all('div',{"id": "wrapper"})[0])
		
		name = bb.find_all("h1")[0].text
		
		cat = bb.find_all("button",{"class":"btn-category"})
		for i in range(0,len(cat)):
			category.append(cat[i].text)
			
		cover = bb.find_all("img",{"class":"book"})[0]["src"]
		desc = (bb.find_all("section",{"class","description"}))[0].find_all("p")[0].text
		pdf = (bb.find_all("section",{"class","downloads"}))[0].find_all("a",{"class":"button"})[0]["href"]
		epub = (bb.find_all("section",{"class","downloads"}))[0].find_all("a",{"class":"button"})[1]["href"]
		
		
		jsondata = {
	       "name":name,
	       "cover":cover,
	       "categories":category,
	       "description":desc,
	       "pdf":pdf,
	       "epub":epub
	       
	       }
		
		allbooks.append(jsondata)
	
	return allbooks
		
print(books("arthur-conan-doyle"))
