import sys
import time
import telepot
import urllib
import urllib.request
import os
import io
from telepot.loop import MessageLoop
try:
    fs = open("./config.json", "r")
except:
    tp, val, tb = sys.exc_info()
    print("Errored when loading config.json:"+\
        str(val).split(',')[0].replace('(', '').replace("'", ""))
    programPause = input("Press any key to stop...\n")
    exit()

#load config
config = eval(fs.read())
fs.close()
TOKEN = config["TOKEN"]
Debug = config["Debug"]

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot_me = bot.getMe()
    username = bot_me['username'].replace(' ', '')
    log("[Debug] Raw message:"+str(msg))
    dlog = "["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info]"
    try:
        dlog = dlog+"[EDITED"+str(msg['edit_date'])+"]"
    except:
        time.sleep(0)
    try:
        fuser = bot.getChatMember(chat_id, msg['from']['id'])
    except:
        fnick = "Channel Admin"
        fuserid = None
    else:
        fnick = fuser['user']['first_name']
        try:
            fnick = fnick + ' ' + fuser['user']['last_name']
        except:
            fnick = fnick
        try:
            fnick = fnick +"@"+ fuser['user']['username']
        except:
            fnick = fnick
        fuserid = str(fuser['user']['id'])
    if chat_type == 'private':
        dlog = dlog + "[Private]["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            dlog = dlog
        else:
            if reply_to == bot_me['id']:
                dlog = dlog + "( Reply to my message "+\
                str(msg['reply_to_message']['message_id'])+" )"
            else:
                tuser = msg['reply_to_message']['from']['first_name']
                try:
                    tuser = tuser + ' ' + msg['reply_to_message']['from']['last_name']
                except:
                    tuser = tuser
                try:
                    tuser = tuser + '@' + msg['reply_to_message']['from']['username']
                except:
                    tuser = tuser
                dlog = dlog + "( Reply to "+tuser+"'s message "+\
                str(msg['reply_to_message']['message_id'])+" )"
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) : " + msg['text']
        else:
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) sent a "+ content_type
        clog(dlog)
        flog = media_log(msg, content_type)
        if flog != None:
            clog(flog)
        #command_detect
        if content_type == 'text':
            if msg['text'] == '/start':
                dre = bot.sendMessage(chat_id, \
                    '歡迎！給我英文字母我就會幫你轉成注音', reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                return
            if msg['text'] == '/a2z':
                dre = bot.sendMessage(chat_id, '此指令只能在群組中使用', reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                return
            string = a2z(msg['text'])
            dre = bot.sendMessage(chat_id, string, reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            print('[A2Z] --->', string)
    elif chat_type == 'group' or chat_type == 'supergroup':
        dlog = dlog + "["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            dlog = dlog
        else:
            if reply_to == bot_me['id']:
                dlog = dlog + "( Reply to my message "+\
                    str(msg['reply_to_message']['message_id'])+" )"
            else:
                tuser = msg['reply_to_message']['from']['first_name']
                try:
                    tuser = tuser + ' ' + msg['reply_to_message']['from']['last_name']
                except:
                    tuser = tuser
                try:
                    tuser = tuser + '@' + msg['reply_to_message']['from']['username']
                except:
                    tuser = tuser
                dlog = dlog + "( Reply to "+tuser+"'s message "+\
                    str(msg['reply_to_message']['message_id'])+" )"
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+\
                msg['chat']['title']+' ( '+str(chat_id)+ ' ): ' + msg['text']
        elif content_type == 'new_chat_member':
            if msg['new_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' I have been added to ' +\
                    msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
            else:
                tuser = msg['new_chat_member']['first_name']
                try:
                    tuser = tuser + ' ' + msg['new_chat_member']['last_name']
                except:
                    tuser = tuser
                try:
                    tuser = tuser + '@' + msg['new_chat_member']['username']
                except:
                    tuser = tuser
                dlog = dlog+' '+ tuser +' joined the ' + chat_type+\
                     ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) '
        elif content_type == 'left_chat_member':
            if msg['left_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' I have been kicked from ' +msg['chat']['title']+\
                    ' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
            else:
                tuser = msg['left_chat_member']['first_name']
                try:
                    tuser = tuser + ' ' + msg['left_chat_member']['last_name']
                except:
                    tuser = tuser
                try:
                    tuser = tuser + '@' + msg['left_chat_member']['username']
                except:
                    tuser = tuser
                dlog = dlog+' '+ tuser +' left the ' + chat_type +\
                     ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) '
        else:
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+\
                msg['chat']['title']+' ( '+str(chat_id)+ ' ) sent a '+ content_type
        clog(dlog)
        flog = media_log(msg, content_type)
        if flog != None:
            clog(flog)
        #command_detect
        if content_type == 'text':
            cmd = msg['text'].split()
            if cmd[0] == '/a2z' or cmd[0] == '/a2z@'+username:
                a2zc(chat_id, msg)
    elif chat_type == 'channel':
        dlog = dlog + "["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']
        except:
            dlog = dlog
        else:
            dlog = dlog + "( Reply to "+str(msg['reply_to_message']['message_id'])+" )"
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick
            if fuserid:
                dlog = dlog + " ( "+fuserid+" )"
            dlog = dlog + " in channel "+msg['chat']['title']+\
                ' ( '+str(chat_id)+ ' ): ' + msg['text']
        else:
            dlog = dlog + ' ' + fnick
            if fuserid:
                dlog = dlog + " ( "+fuserid+" )"
            dlog = dlog +" in channel"+msg['chat']['title']+\
                ' ( '+str(chat_id)+ ' ) sent a '+ content_type
        clog(dlog)
        flog = media_log(msg, content_type)
        if flog != None:
            clog(flog)

def media_log(msg, content_type):
    if content_type == 'photo':
        flog = "[Photo]"
        photo_array = msg['photo']
        photo_array.reverse()
        try:
            flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
        except:
            flog = flog +"FileID:"+ photo_array[0]['file_id']
    elif content_type == 'audio':
        flog = "[Audio]"
        try:
            flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
        except:
            flog = flog +"FileID:"+ msg['audio']['file_id']
    elif content_type == 'document':
        flog = "[Document]"
        try:
            flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
        except:
            flog = flog +"FileID:"+ msg['document']['file_id']
    elif content_type == 'video':
        flog = "[Video]"
        try:
            flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
        except:
            flog = flog +"FileID:"+ msg['video']['file_id']
    elif content_type == 'voice':
        flog = "[Voice]"
        try:
            flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
        except:
            flog = flog +"FileID:"+ msg['voice']['file_id']
    elif content_type == 'sticker':
        flog = "[Sticker]"
        try:
            flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
        except:
            flog = flog +"FileID:"+ msg['sticker']['file_id']
    else:
        flog = None
    return flog

def a2zc(chat_id, msg):
    try:
        reply_to = msg['reply_to_message']
    except:
        alpt = msg['text'].split(' ', 1)
        try:
            tcm = alpt[1]
        except:
            dre = bot.sendMessage(chat_id, '/a2z <string>\n或回覆一個信息來將英文字母轉成注音',\
                 reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            string = a2z(tcm)
            dre = bot.sendMessage(chat_id, string, reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[A2Z] --->'+string)
    else:
        try:
            tcm = reply_to['text']
        except:
            dre = bot.sendMessage(chat_id, '請回復一個文字信息',\
                reply_to_message_id=msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
        else:
            string = a2z(tcm)
            dre = bot.sendMessage(chat_id, string, reply_to_message_id=reply_to['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            clog('[A2Z] --->'+string)
    return

def a2z(textLine):
    zh = textLine.lower()
    zh = zh.replace("ａ", "a")
    zh = zh.replace("ｂ", "b")
    zh = zh.replace("ｃ", "c")
    zh = zh.replace("ｄ", "d")
    zh = zh.replace("ｅ", "e")
    zh = zh.replace("ｆ", "f")
    zh = zh.replace("ｇ", "g")
    zh = zh.replace("ｈ", "h")
    zh = zh.replace("ｉ", "i")
    zh = zh.replace("ｊ", "j")
    zh = zh.replace("ｋ", "k")
    zh = zh.replace("ｌ", "l")
    zh = zh.replace("ｍ", "m")
    zh = zh.replace("ｎ", "n")
    zh = zh.replace("ｏ", "o")
    zh = zh.replace("ｐ", "p")
    zh = zh.replace("ｑ", "q")
    zh = zh.replace("ｒ", "r")
    zh = zh.replace("ｓ", "s")
    zh = zh.replace("ｔ", "t")
    zh = zh.replace("ｕ", "u")
    zh = zh.replace("ｖ", "v")
    zh = zh.replace("ｗ", "w")
    zh = zh.replace("ｘ", "x")
    zh = zh.replace("ｙ", "y")
    zh = zh.replace("ｚ", "z")
    zh = zh.replace("１", "1")
    zh = zh.replace("２", "2")
    zh = zh.replace("３", "3")
    zh = zh.replace("４", "4")
    zh = zh.replace("５", "5")
    zh = zh.replace("６", "6")
    zh = zh.replace("７", "7")
    zh = zh.replace("８", "8")
    zh = zh.replace("９", "9")
    zh = zh.replace("０", "0")
    zh = zh.replace("－", "-")
    zh = zh.replace("；", ";")
    zh = zh.replace("，", ",")
    zh = zh.replace("．", ".")
    zh = zh.replace("／", "/")
    zh = zh.replace('1', 'ㄅ')
    zh = zh.replace('2', 'ㄉ')
    zh = zh.replace('3', 'ˇ')
    zh = zh.replace('4', 'ˋ')
    zh = zh.replace('5', 'ㄓ')
    zh = zh.replace('6', 'ˊ')
    zh = zh.replace('7', '˙')
    zh = zh.replace('8', 'ㄚ')
    zh = zh.replace('9', 'ㄞ')
    zh = zh.replace('0', 'ㄢ')
    zh = zh.replace('-', ' ㄦ')
    zh = zh.replace('q', 'ㄆ')
    zh = zh.replace('w', 'ㄊ')
    zh = zh.replace('e', 'ㄍ')
    zh = zh.replace('r', 'ㄐ')
    zh = zh.replace('t', 'ㄔ')
    zh = zh.replace('y', 'ㄗ')
    zh = zh.replace('u', 'ㄧ')
    zh = zh.replace('i', 'ㄛ')
    zh = zh.replace('o', 'ㄟ')
    zh = zh.replace('p', 'ㄣ')
    zh = zh.replace('a', 'ㄇ')
    zh = zh.replace('s', 'ㄋ')
    zh = zh.replace('d', 'ㄎ')
    zh = zh.replace('f', 'ㄑ')
    zh = zh.replace('g', 'ㄕ')
    zh = zh.replace('h', 'ㄘ')
    zh = zh.replace('j', 'ㄨ')
    zh = zh.replace('k', 'ㄜ')
    zh = zh.replace('l', 'ㄠ')
    zh = zh.replace(';', 'ㄤ')
    zh = zh.replace('z', 'ㄈ')
    zh = zh.replace('x', 'ㄌ')
    zh = zh.replace('c', 'ㄏ')
    zh = zh.replace('v', 'ㄒ')
    zh = zh.replace('b', 'ㄖ')
    zh = zh.replace('n', 'ㄙ')
    zh = zh.replace('m', 'ㄩ')
    zh = zh.replace(',', 'ㄝ')
    zh = zh.replace('.', 'ㄡ')
    zh = zh.replace('/', 'ㄥ')
    return zh

def clog(text):
    print(text)
    log(text)
    return

def log(text):
    if text[0:7] == "[Debug]":
        if Debug == True:
            logger = io.open(logpath+ "-debug.log", "a", encoding='utf8')
            logger.write("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"]"+text+"\n")
            logger.close()
        return
    logger= io.open(logpath+".log", "a", encoding='utf8')
    logger.write(text+"\n")
    logger.close()
    return

if os.path.isdir("./logs") == False:
    os.mkdir("./logs")
logpath = "./logs/"+time.strftime("%Y-%m-%d-%H-%M-%S").replace("'", "")
bot = telepot.Bot(TOKEN)
#bot = telepot.DelegatorBot(TOKEN,
#   pave_event_space()(
#        per_chat_id(), create_open, Player, timeout=20),
#]))
log("[Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
log("[Debug][Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
log("[Debug] Bot's TOKEN is "+TOKEN)
answerer = telepot.helper.Answerer(bot)

#bot.message_loop({'chat': on_chat_message})
MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info] Bot has started")
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'", "")+"][Info] Listening ...")

# Keep the program running.
while 1:
    time.sleep(10)