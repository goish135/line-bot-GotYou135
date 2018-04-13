from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)
import urllib.request
from bs4 import BeautifulSoup
import requests
import re

from urllib.request import urlretrieve
import os
import time
import random
from random import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Your Cannel Access Token')
# Channel Secret
handler = WebhookHandler('Your Channel Secret')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

import urllib.request
from bs4 import BeautifulSoup

def get_weather():
	quote_page = 'https://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm'
	page = urllib.request.urlopen(quote_page)
	soup = BeautifulSoup(page,'html.parser')
	name_box = soup.find('tbody').find_all('tr')
	add='台中天氣:\n'
	count  = 0
	for tr in name_box:
		for td in tr:
			if td.string != None :
				if count == 9 or count == 20 or count == 31:
					add+='降雨機率(%):\n'
				if count == 3 or count == 14 or count == 25:
					add+='氣溫(度C):\n'
				add+=td.string
				#print(td.string)
			elif td.string == None:
				add+='舒適度:'
			count = count + 1
			#print(count)	
		add+='/'		
	return add

#print(get_weather())

def get_weather_2():
	quote_page = 'https://www.cwb.gov.tw/V7/forecast/taiwan/Chiayi_City.htm'
	page = urllib.request.urlopen(quote_page)
	soup = BeautifulSoup(page,'html.parser')
	name_box = soup.find('tbody').find_all('tr')
	add='嘉義天氣:\n'
	for tr in name_box:
		for td in tr:
			if td.string != None :
				add+=td.string
			elif td.string == None:
				add+='舒適度:'
		add+='/'		
	return add

def get_time_3():
	quote_page = 'http://www.lib.ntcu.edu.tw/mp.asp?mp=1'
	page = urllib.request.urlopen(quote_page)
	soup = BeautifulSoup(page,'html.parser')
	name_box = soup.find('div',attrs={'class':'activity'})	
	name = name_box.text.strip('\n')
	#print ('台中教育大學圖書館:\n')
	#print (name)
	location='台中教育大學圖書館:\n\n'
	location+=name
	return location
	
def movie():
	source = 'http://www.atmovies.com.tw/movie/new/'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
	req = urllib.request.Request(url=source, headers=headers)  
	page = urllib.request.urlopen(req).read()  

	soup = BeautifulSoup(page,'html.parser')

	urls = soup.find_all('article',attrs={'class':'box post'}) 

	count = 0
	total = 0
	hf = []
	title = []
	for url in urls:
		ass=url.find_all('a',attrs={'class':'image filmListPoster'})
		bss =url.find_all('a',attrs={'target':''})
		for item in ass:
			count = count + 1
			temp = 'http://www.atmovies.com.tw'+item['href']+'\n'
			hf.append(temp)
		
		
		for it in bss:
			total=total+1
			tp=''.join(it.text.strip())
			title.append(tp)

		
	css = []
	re = 0 		
	for i in range(1,total,3): 
		css.append(title[i])
		re = re + 1

	reply =''
	reply += '本週新片:\n'	
	for j in range(0,re):		
		reply+= css[j]+'\n'+hf[j]
	return reply


	
def movie_dis():
    target_url = 'http://disp.cc/b/Movie'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content

def volley():
	string = "排球直播";
	url = "https://www.youtube.com/results?search_query=" + string
	res = requests.get(url, verify=False)
	soup = BeautifulSoup(res.text,'html.parser')
	last = None
	vv=''
	for entry in soup.select('a'):
		m = re.search("v=(.*)",entry['href'])
		if m:
			target = m.group(1)
			if target == last:
				continue
			if re.search("list",target):
				continue
			last = target
			v = 'https://www.youtube.com/watch?v='+target+'\n'
			vv+=v
	return vv

def techAI():
	source = 'https://buzzorange.com/techorange/tag/artificialintelligence/'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
	req = urllib.request.Request(url=source, headers=headers)  
	page = urllib.request.urlopen(req).read()  
	soup = BeautifulSoup(page,'html.parser')

	urls = soup.find_all('h4',attrs={'class':'entry-title'}) #find_all 回傳 list
	ans ='' 	
	for url in urls:
		a=url.find('a')
		ans+=a.text+'\n'+a['href']+'\n'+'\n'
	return ans		

def techNew():
	source = 'https://buzzorange.com/techorange/'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
	req = urllib.request.Request(url=source, headers=headers)  
	page = urllib.request.urlopen(req).read()  
	soup = BeautifulSoup(page,'html.parser')

	urls = soup.find_all('h4',attrs={'class':'entry-title'}) #find_all 回傳 list
	ans ='' 	
	for url in urls:
		a=url.find('a')
		ans+=a.text+'\n'+a['href']+'\n'+'\n'
	return ans

def oil():
    source = 'https://gas.goodlife.tw/'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=source, headers=headers)  
    page = urllib.request.urlopen(req).read()  
    soup = BeautifulSoup(page,'html.parser')
    more = soup.find_all('div',attrs={'id':'cpc'})
    a = '油價資訊:\n\n'
    box = soup.find('li',attrs={'class':'main'})
    a += ''.join(box.text.strip())+'\n\n'
    print(a)
    for p in more:
        a += '  '.join(p.text.split())+'\n'
    return a

def lun():
    lista = []
    lista.append('https://i.imgur.com/PIu3C6Z.jpg')
    lista.append('https://i.imgur.com/RSYyfWr.jpg')
    lista.append('https://i.imgur.com/MdXOwdw.jpg')
    lista.append('https://i.imgur.com/cWi4c4Y.jpg')
    lista.append('https://i.imgur.com/DT9Lo8Y.jpg')
    lista.append('https://i.imgur.com/jt53zSO.jpg')
    lista.append('https://i.imgur.com/CrPvatt.jpg')
    lista.append('https://i.imgur.com/Yo9U8vY.jpg')
    lista.append('https://i.imgur.com/iJOdaMZ.jpg')
    lista.append('https://i.imgur.com/60fvT82.jpg')
    lista.append('https://i.imgur.com/xBNxuRg.jpg')
    lista.append('https://i.imgur.com/hU0LscU.jpg')
    lista.append('https://i.imgur.com/NLaDQoY.jpg')
    lista.append('https://i.imgur.com/22FPBNM.jpg')
    lista.append('https://i.imgur.com/PYPWQn8.jpg')
    lista.append('https://i.imgur.com/ucv5vIX.jpg')
    lista.append('https://i.imgur.com/DOU3AKE.jpg')
    lista.append('https://i.imgur.com/BCqAd8B.jpg')
    lista.append('https://i.imgur.com/1tbTvvz.jpg')
    lista.append('https://i.imgur.com/JFfy01q.jpg')
    lista.append('https://i.imgur.com/X9G6jhZ.jpg')
    lista.append('https://i.imgur.com/zrhU8Om.jpg')
    lista.append('https://i.imgur.com/0DnuLHi.jpg')
    lista.append('https://i.imgur.com/kqBWLzu.jpg')
    lista.append('https://i.imgur.com/EdEYMno.jpg')
    lista.append('https://i.imgur.com/SVI7yJj.jpg')
    lista.append('https://i.imgur.com/IOx98DM.jpg')
    lista.append('https://i.imgur.com/yGzKQTG.jpg')
    lista.append('https://i.imgur.com/jBygbj0.jpg')
    lista.append('https://i.imgur.com/K9Ihap7.jpg')
    lista.append('https://i.imgur.com/MH7ipZ2.jpg')
    lista.append('https://i.imgur.com/BT1Dyzn.jpg')
    x = randint(0,31)
    str=lista[x]
    return str	
	
#def mini():
#	Bob=''
#	Bob+="  /~~~~~~~~\\    ---------\n";
#	Bob+="  | ((*)(*))    | __Hi__|\n";
#	Bob+="y_|\___==__/|_y   \/\n";
#	Bob+="  \_|++++|_/\n";
#	Bob+="    _/  \_\n";
#	return Bob
		
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	if event.message.text == "天氣" or event.message.text == "1":
		message = TextSendMessage(text=get_weather())
		#name = get_weather()
		line_bot_api.reply_message(
			event.reply_token,
			message)
		#return 0	
	elif event.message.text == "嘉義天氣" or event.message.text == "2":
		message = TextSendMessage(text=get_weather_2())
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "go studying" or event.message.text == "11":
		message = TextSendMessage(text=get_time_3())
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "Hi" or event.message.text == "3":
		message = ImageSendMessage(
			original_content_url='https://i.imgur.com/HypvDWc.png',
			preview_image_url='https://i.imgur.com/HypvDWc.png'
		)
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "movie" or event.message.text=="4":
		message = TextSendMessage(text=movie())
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "PttHot" or event.message.text=="6":
		message = TextSendMessage(text=joke())
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "moviemovie" or event.message.text=="5":
		message = TextSendMessage(text=movie_dis())
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "volleyball" or event.message.text=="7":
		message = TextSendMessage(text=volley())
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "135" or event.message.text =="@GotYou135":
		message = ImageSendMessage(
			original_content_url='https://i.imgur.com/mGqK7dN.jpg',
			preview_image_url='https://i.imgur.com/mGqK7dN.jpg'
		)
		line_bot_api.reply_message(
			event.reply_token,
			message)
			
	elif event.message.text == "lovely" or event.message.text=="8":
		message = ImageSendMessage(
			original_content_url=lun(),
			preview_image_url=lun()
		)
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "AI" or event.message.text=="9":
		message = TextSendMessage(text=techAI())
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "technew" or event.message.text=="10":
		message = TextSendMessage(text=techNew())
		line_bot_api.reply_message(
			event.reply_token,
			message)
	elif event.message.text == "gas" or event.message.text=="12":
		message = TextSendMessage(text=oil())
		line_bot_api.reply_message(
			event.reply_token,
			message)

	
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
