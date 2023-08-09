import requests
from bs4 import *

def poems(na):
	
	allpoems = []
	name = (na.lower()).replace(" ", "")
	
	r = requests.get(f"https://hellopoetry.com/poets/{name}/")
	soup = BeautifulSoup(r.text, 'html.parser')    
	page = soup.find_all('div',{"class":"poem-view inner"})
	
	for i in range(0,len(page)):
		title= page[i].find_all("div")[1].text
		poem = page[i].find_all("div")[2].text
		
		jsondata = {
			"title":title.strip(),
			"poem":poem.strip()
		}
		
		allpoems.append(jsondata)
		
	return allpoems

print(poems("mirabai"))
