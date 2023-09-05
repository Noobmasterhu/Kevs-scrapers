from bs4 import *
import requests
import json

def soupp(link):
	
	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	return soup
	
	
def apod():
	
	
	url = "https://apod.nasa.gov/apod/astropix.html"
	soup = soupp(url)
	
	try:
		date = soup.find_all("center")[0].find_all("p")[1].text.strip()
	except:
		date = " "
		
	try:
		imageHD = "https://apod.nasa.gov/" + soup.find_all("center")[0].find_all("p")[1].find("a")["href"]
	except:
		imageHD = " "
	
	try:
		image = "https://apod.nasa.gov/" + soup.find_all("center")[0].find_all("p")[1].find("img")["src"]
	except:
		image = " "
		
	try:
		title = soup.find_all("center")[1].find_all("b")[0].text.strip()
	except:
		title = " "
		
	try:
		credit = soup.find_all("center")[1].find_all("a")[0].text.strip()
	except:
		credit = " "
	
	try:
		creditURL = soup.find_all("center")[1].find_all("a")[0]["href"]
	except:
		creditURL = " "
	
	try:
		ex = soup.find("body").find_all("p")[2].text.strip().replace("Explanation:","").replace(f'{soup.find("body").find_all("p")[3].text.strip()}',"").strip()
		exp = " ".join(line.strip() for line in ex.splitlines())
	except:
		exp = " "
	
	jsondata ={
	
	"title"       : title,
	"date"        : date,
	"image"       : image,
	"imageHD"     : imageHD,
	"credit"      : credit,
	"creditURL"   : creditURL,
	"explanation" : exp
	
	}
	
	aopdjson = json.dumps(jsondata, indent=4)
	
	return aopdjson
	
#print(apod())	
