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
line_bot_api = LineBotApi('Q/s2uzDSQrn71rDMEBcVc2idkdKfm+o6fH/9Xwapm8eD28OfPOd3oK//673gV7mv6/cgYNM2bd5Ym3AKzdwuWVZYkhY2TJIPGqYYIR9y32tYgA2jcNcIoyZTf4zXuBv39KMcWdlFVWLOrlr/rxCCvQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('738c0079354df45faacb5d402d0c7e6f')

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

def get_weather():
	quote_page = 'https://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm'
	page = urllib.request.urlopen(quote_page)
	soup = BeautifulSoup(page,'html.parser')
	name_box = soup.find('tbody').find_all('tr')
	add='台中天氣:\n'
	for tr in name_box:
		for td in tr:
			if td.string != None :
				add+=td.string
			elif td.string == None:
				add+='舒適度:'
		add+='/'		
	return add

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
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    #print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmNextListAll a')):
        if index == 20:
            return content
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def joke():
    target_url = 'http://disp.cc/b/PttHot'
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

def menu():
	a = '指令'
	b = '說明'

	c1 = '天氣'
	c2 = '嘉義天氣'
	c3 = 'go studying'
	c4 = 'Hi'
	c5 = 'movie'
	c6 = 'joke'
	c7 = 'moviemovie'
	c8 = 'volleyball'

	d1 = '台中天氣'
	d2 = '嘉義天氣'
	d3 = '台中教育大學圖書館開閉館時間'
	d4 = 'Say Hi的圖片'
	d5 = '開眼電影網之近期上映電影'
	d6 = 'PTT有趣版'
	d7 = 'PTT電影版'
	d8 = '排球直播的youtube影片'

	#head = '%-30s%-50s\n'%(a,b) 
	#command_1 ='%-30s%-50s\n'%(c1,d1) 
	#command_2 ='%-30s%-50s\n'%(c2,d2)
	#command_3 ='%-30s%-50s\n'%(c3,d3)

	head = a.ljust(35) + '\t'+ b.ljust(100)+'\n'
	command_1 = c1.ljust(35)+'\t'+d1.ljust(100)+'\n'
	command_2 = c2.ljust(35)+'\t'+d2.ljust(100)+'\n'
	command_3 = c3.ljust(35)+'\t'+d3.ljust(100)+'\n'
	command_4 = c4.ljust(35)+'\t'+d4.ljust(100)+'\n'
	command_5 = c5.ljust(35)+'\t'+d5.ljust(100)+'\n'
	command_6 = c6.ljust(35)+'\t'+d6.ljust(100)+'\n'
	command_7 = c7.ljust(35)+'\t'+d7.ljust(100)+'\n'
	command_8 = c8.ljust(35)+'\t'+d8.ljust(100)+'\n'
	summary = head+command_1+command_2+command_3+command_4+command_5+command_6+command_7+command_8	
	return summary

def lun():
    lista = []
    lista.append('https://ppt.cc/f4Rufx@.jpg')
    lista.append('https://ppt.cc/fmRhzx@.jpg')
    lista.append('https://ppt.cc/f29mkx@.jpg')
    lista.append('https://ppt.cc/faLYkx@.jpg')
    lista.append('https://ppt.cc/fZhMsx@.jpg')
    lista.append('https://ppt.cc/fBWAHx@.jpg')
    lista.append('https://ppt.cc/fl0KGx@.jpg')
    lista.append('https://ppt.cc/fJvdNx@.jpg')
    lista.append('https://ppt.cc/ffPczx@.jpg')
    lista.append('https://ppt.cc/ft8YTx@.png')
    lista.append('https://ppt.cc/fuVIrx@.jpg')
    lista.append('https://ppt.cc/fSFTwx@.jpg')
    lista.append('https://ppt.cc/f60aLx@.jpg')
    lista.append('https://ppt.cc/fwlbzx@.jpg')
    lista.append('https://ppt.cc/fwWe0x@.jpg')
    lista.append('https://ppt.cc/fRB3cx@.jpg')
    lista.append('https://ppt.cc/f6fyJx@.jpg')
    lista.append('https://ppt.cc/fpBlgx@.jpg')
    lista.append('https://ppt.cc/fvnh6x@.jpg')
    lista.append('https://ppt.cc/fWWBwx@.jpg')
    x = randint(0,19)
	#print(lista[x])
    str=lista[x]
	#print(type(str))
    return str

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
			original_content_url='https://ppt.cc/fWabhx@.png',
			preview_image_url='https://ppt.cc/fWabhx@.png'
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
			original_content_url='https://ppt.cc/f7QJrx@.jpg',
			preview_image_url='https://ppt.cc/f7QJrx@.jpg'
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
    			
	#elif event.message.text == "fresh":
        #message = ImageSendMessage(
			#original_content_url=,
			#preview_image_url=
		#)
		#line_bot_api.reply_message(
			#event.reply_token,
			#message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
