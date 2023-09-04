import requests
from bs4 import BeautifulSoup


def googlesearch(keyword):
	
	google_url = f"https://www.google.com/search?q= + {keyword}"
	response = requests.get(google_url)
	soup = BeautifulSoup(response.text, "html.parser")
	result_div = soup.find_all('div')
	
	
	gjson = []

	for r in result_div:
	   # Checks if each element is present, else, raise exception
	   try:
	       link = r.find('a', href = True)
	       title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
	       description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
	       # Check to make sure everything is present before appending
	       
	       if link != '' and title != '' and description != '':
	           
	           jsondata = {
	           "link"        :link['href'].split("?q=")[1],
	           "title"       :title,
	           "description" :description
	           }
	           
	           gjson.append(jsondata)
	   
	   # Next loop if one element is not present
	       
	   except:
	   	continue
	   	
	return gjson


#print(googlesearch("carbon"))
