import time,datetime
import codecs
import json
from TwitterAPI import TwitterAPI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from TwitterAPI import TwitterAPI

#TwitterAPI Settings
api = TwitterAPI('Consumer Key', 'Consumer Secret', 'Access Token', 'Access Token Secret')

#Open session to write
outputFile = codecs.open("output.txt/output.csv", "w+", "utf-8")
outputFile.write('username;date;time;text;tweetID;placeID;pusatkota;lokasi;longitude;latitude\n')

#Open webdriver Chrome
#Use location to your chromedriver.exe
browser = webdriver.Chrome("D:/Your folder/chromedriver.exe")

#search url
browser.get("https://twitter.com/search?src=typd&q=%23hashtag%20since%3A2014-01-31%20until%3A2015-03-14")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

#Scroll value
scroll = 1000

while scroll:
	elem.send_keys(Keys.PAGE_DOWN)
	time.sleep(0.2)
	scroll-=1
	
#tweet_contents = browser.find_elements_by_css_selector("div > div.content")
tweet_contents = browser.find_elements_by_class_name("js-stream-tweet")

for tweet in tweet_contents:
	#Tweet text
	text = tweet.find_element_by_css_selector("div.js-tweet-text-container > p").text.replace('\n',' ').encode('ascii', 'ignore')
	
	#Username
	username = tweet.find_element_by_css_selector("div.stream-item-header > a > span.username.js-action-profile-name > b").text.encode('ascii', 'ignore')
	
	#Date of tweet
	dateInt = int(tweet.find_element_by_css_selector("div.stream-item-header > small > a > span").get_attribute('data-time'))
	dateFormat = datetime.datetime.fromtimestamp(dateInt)
	
	#Place ID
	if len(tweet.find_elements_by_class_name("Tweet-geo")) > 0:
		placeID = tweet.find_element_by_css_selector("div.stream-item-header > span > a").get_attribute('data-place-id')
		r = api.request('geo/id/:%s' % placeID)
		json_var = r.json()


		#name
		pusatkota = json_var['name']
		#fullname
		lokasi = json_var['full_name']
		#longitude
		longitude = json_var['centroid'][0]
		#latitude
		latitude = json_var['centroid'][1]

	else:
		placeID = ''
		lokasi = ''
		pusatkota = ''
		longitude = ''
		latitude = ''

	#Tweet ID
	tweetID = tweet.get_attribute("data-tweet-id")
	
	outputFile.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n' % (username, dateFormat.strftime("%Y-%m-%d"),dateFormat.strftime("%H:%M"), text, tweetID, placeID,pusatkota,lokasi, longitude,latitude))