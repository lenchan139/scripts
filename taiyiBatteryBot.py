# coding=utf-8
#!/usr/bin/python
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os,random
import sys
import time
import datetime
import json
import requests

def getMe(token):
    response = requests.post(
    url='https://api.telegram.org/bot' + token + "/" + method
).json()
    return response;

def getUpdates(token,offset):
    response = requests.post(
        url='https://api.telegram.org/bot' + token + "/getUpdates",
        data={'offset': offset}
).json()
    return response;

def sendMessage(token,chat_id,message_id,text):
    response = requests.post(
        url='https://api.telegram.org/bot' + token + "/sendMessage",
        data={'chat_id': chat_id,'reply_to_message_id': message_id, 'text': text}
).json()
    return response

def sendPhoto(token,chat_id,message_id,img):
    response = requests.post(
        url='https://api.telegram.org/bot' + token + "/sendPhoto",
        data={'chat_id': chat_id,'reply_to_message_id': message_id},
        files={'photo': img},
).json
    return response

def getImg(folder):
    a = [];
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder,f)):
            a.append(f);
    pic = random.choice(a);
    picLoc = os.path.join(folder,pic)
    img = open(picLoc,'rb')
    return img

def getReplyIDs(js,index):
    chat_id = js['result'][index]['message']['chat']['id']
    message_id = js['result'][index]['message']['message_id']
    return chat_id, message_id

def calBattery():
    dateToday = datetime.date.today()
    timeEnds = datetime.time(21,50,00)
    timeStarts = datetime.time(9,00,00)
    batteryStarts = datetime.datetime.combine(dateToday,timeStarts)
    batteryEnds = datetime.datetime.combine(dateToday,timeEnds)
    batteryNow = datetime.datetime.now()
    result = float((batteryEnds - batteryNow).total_seconds())/float((batteryEnds - batteryStarts).total_seconds())
    return "{:.2%}".format(result)

if __name__ == "__main__":
    token = sys.argv[1]
    offset = sys.argv[2]
    offset_old = 0
    while True:
        print offset
        response = getUpdates(token,offset)
        offset = response['result'][-1]['update_id']
        if offset == offset_old:
            pass;
        else:
            for i in range(1,len(response['result'])):
                a,b = getReplyIDs(response,i)
                text = calBattery()
                r = response['result'][i]['message']
                if r.has_key("text"):
                    if response['result'][i]['message']['text'] == "/batteryreport":
                        sendMessage(token,a,b,text)
                    elif response['result'][i]['message']['text'] == "/leg":
                        #img = getImg("/Users/yk/Downloads/New/")
                        #sendPhoto(token,a,b,img)
                        sendMessage(token,a,b,"（〃｀д´ )( ´ｪ`)")
                    elif response['result'][i]['message']['text'] == "/crossdressfubuki":
                        sendMessage(token,a,b,"🌚")
                    else:
                        sendMessage(token,a,b,"🍼")
        offset_old = offset 
        time.sleep(1);
