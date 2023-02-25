import telebot,sys
from datetime import *
import os,requests,time,keyboard,json,csv,aiohttp,asyncio
from pprint import pprint
import tracemalloc#,pyfiglet
from telebot import types


#Api source from Xdownload

token = 'Your-token-here'
bot = telebot.TeleBot(token)

headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
	   }


#download publish video facebook function
def dl_facebook(link_fb,id_user):
	global link_download
	url_res = 'https://x2download.com/api/ajaxSearch'
	data = {'q':f'{link_fb}','vt': 'home'}
	res = requests.post(url_res,headers=headers,data=data)
	try:
		jsondata = res.json()
		data = jsondata['links']
		link_download = data['sd']
		duration = jsondata['duration']
		title = jsondata['title']
		image = jsondata['thumbnail']
		print(link_download)
		print(duration)
		print(title)
		print(image)
		return link_download
	except:
		print("Vui Lòng Kiểm Tra Lại Link! Có Thể Link Sai Hoặc Link Từ Group Kín Facebook.")
		uptele = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id_user}&text="+"Vui Lòng Kiểm Tra Lại Link! Có Thể Link Sai Hoặc Link Từ Group Kín Facebook.")



#download video youtube function
def dl_youtube(link_youtube,id_user):
	url_res1 = 'https://x2download.com/api/ajaxSearch'
	headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
   }
	data = {'q':f'{link_youtube}','vt': 'home'}
	res = requests.post(url_res1,headers=headers,data=data)
	try:
		data = res.json()
		print(data)
		vid = data['vid']
		title = data['title']
		token = data['token']
		timeExpires = data['timeExpires']
		print(vid)
		print(title)
		print(token)
		print(timeExpires)
		data_dl_youtube = getlink_youtube(vid,title,token,timeExpires,id_user)
		return data_dl_youtube
	except:
		print("Vui Lòng Kiểm Tra Lại Link.")


def getlink_youtube(vid,title,token,timeExpires,id_user):
	list_fquality = ['1080p','720p','480p','360p','144p']
	for i in list_fquality:
		data = {
	  'v_id': f'{vid}',
	  'ftype': 'mp4',
	  'fquality': f'{i}',
# 	  'fname': f'{title}',
	  'token': f'{token}',
	  'timeExpire': f'{timeExpires}',
	'client': 'X2Download.app'
		}
		try:
			response = requests.post('https://dd107.opoaidazzc.xyz/api/json/convert', headers=headers, data=data)
			datajson = response.json()
			result = datajson['result']
			statusCode = datajson['statusCode']
			if statusCode == 200:
				print(result)
				return result
				break
			else:
				print('Converting')
		except:
			print("Vui Lòng Kiểm Tra Lại Link!.")



#start command
@bot.message_handler(commands=['start'])
def send_start(message):
	bot.send_message(message.chat.id,"Chào bạn, Chào Mừng Bạn Đến Với Bot Tải Video Từ Youtube & Facebook (Công Khai) Được Thiết Kể Bởi @gocsandeal.\n\n Gõ /help Để Xem Các Lệnh Của Bot")

#help command
@bot.message_handler(commands=['help'])
def send_help(message):
	text_help = "MỘT SỐ LỆNH CÓ THỂ SỬ DỤNG DƯỚI ĐÂY:\n\n   /youtube -> Download Video Youtube\n   /facebook -> Download Video Facebook\n   /help -> Là Lệnh Bạn Đang Sử Dụng\n   /contact -> Liên Hệ Người Tạo Bot\n\n❗️LƯU Ý:\nĐể Nhập Link Cần Download, Vui lòng nhập đúng cú pháp\n   /fb link cần tải (Đối với lệnh download video facebook)\n   /yt link cần tải. (Đối với lệnh download video facebook)"
	bot.send_message(message.chat.id,text_help)
#❗️LƯU Ý:\n 1/ Để Nhập Link Cần Download, Vui lòng nhập đúng cú pháp\n/fb_dấucách_link cần tải. ex : /fb facebook.com/xxx (Đối với lệnh download video facebook)\n/yt_dấucách_link cần tải. ex : /yt youtube.com/xxx (Đối với lệnh download video facebook)
#contact command
@bot.message_handler(commands=['contact'])
def send_contact(message):
	text_contact = "MỘT SỐ THÔNG TIN BẠN CÓ THỂ LIÊN LẠC ĐỂ HỖ TRỢ:\n\n   Người tạo bot -> @RealVincent1312\n   Facebook -> https://www.facebook.com/gocsandeal\n   Telegram -> @gocsandeal"
	bot.send_message(message.chat.id,text_contact)



#Facebook command
@bot.message_handler(commands=['facebook'])
def facebook_command(message):
	id_user = message.chat.id
	bot.send_message(message.chat.id,"💥Vui lòng nhập Link Facebook theo dạng : _/fb facebook.com/xxx_",parse_mode="Markdown")
	@bot.message_handler(commands="fb")
	def echo_account(message):
		link_fb= message.text
		link_fb = link_fb.replace('/fb ','')
		bot.send_message(message.chat.id,"Bạn Vui Lòng Chờ Tí Nhé 🥰")
		data = dl_facebook(link_fb,id_user)
		if data != None:
			keyboard = types.InlineKeyboardMarkup()
			url_btn = types.InlineKeyboardButton(url=f"{data}", text="Click Để Tải ^^")
			keyboard.add(url_btn)
			bot.send_message(message.chat.id, "✨Dưới Đây Là Link Tải Facebook Của Bạn", reply_markup=keyboard)


#Youtube command
@bot.message_handler(commands=['youtube'])
def facebook_command(message):
	id_user = message.chat.id
	bot.send_message(message.chat.id,"💥Vui lòng nhập Link Youtube theo dạng : _/yt youtube.com/xxx_",parse_mode="Markdown")
	@bot.message_handler(commands="yt")
	def echo_account(message):
		link_youtube= message.text
		link_youtube = link_youtube.replace('/yt ','')
		bot.send_message(message.chat.id,"Bạn Vui Lòng Chờ Tí Nhé 🥰")
		data = dl_youtube(link_youtube,id_user)
		if data != None:
			keyboard = types.InlineKeyboardMarkup()
			url_btn = types.InlineKeyboardButton(url=f"{data}", text="Click Để Tải ^^")
			keyboard.add(url_btn)
			bot.send_message(message.chat.id, "✨Dưới Đây Là Link Tải Youtube Của Bạn", reply_markup=keyboard)
		

bot.polling()
