import sys
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

TOKEN = ''





def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    try:
        print('[EDIT][',msg['edit_date'],']:',msg['message_id'],' -->',msg['text'])
    except:
        time.sleep(0)
    else:
        time.sleep(0)
    if chat_type == 'private':
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            if content_type != 'text':
                try:
                    print('[Info][',msg['message_id'],']',msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                except:
                    print('[Info][',msg['message_id'],']',chat_id, ' sent a ', content_type)
                return
            try:
                print('[Info][',msg['message_id'],']',msg['chat']['username'],'(',chat_id, ') :', msg['text'])
            except:
                print('[Info][',msg['message_id'],']',chat_id, ' :', msg['text'])
        else:
            if content_type != 'text':
                try:
                    print('[Info][',msg['message_id'],'](Reply)',msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                except:
                    print('[Info][',msg['message_id'],'](Reply)',chat_id, ' sent a ', content_type)
                return
            try:
                print('[Info][',msg['message_id'],'](Reply)',msg['chat']['username'],'(',chat_id, ') :', msg['text'])
            except:
                print('[Info][',msg['message_id'],'](Reply)',chat_id, ' :', msg['text'])
            return
        if msg['text'] == '/start':
            bot.sendMessage(chat_id,'歡迎！給我英文字母我就會幫你轉成注音',reply_to_message_id=msg['message_id'])
            return
        if msg['text'] == '/a2z':
            bot.sendMessage(chat_id,'此指令只能在群組中使用',reply_to_message_id=msg['message_id'])
            return
        string=a2z(msg['text'])
        bot.sendMessage(chat_id,string,reply_to_message_id=msg['message_id'])
        print('[Info] --->',string)
    elif chat_type == 'group' or chat_type == 'supergroup':
        try:
            reply_to = msg['reply_to_message']
        except:
            if content_type != 'text':
                if content_type == 'new_chat_member':
                    if msg['new_chat_member']['id'] == bot_me['id']:
                        try:
                            print('[Info][',msg['message_id'],'] I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                        except:
                            print('[Info][',msg['message_id'],'] I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                    else:
                        try:
                            print('[Info][',msg['message_id'],'] ',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        except:
                            print('[Info][',msg['message_id'],'] ',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                elif content_type == 'left_chat_member':
                    if msg['left_chat_member']['id'] == bot_me['id']:
                        try:
                            print('[Info][',msg['message_id'],'] I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                        except:
                            print('[Info][',msg['message_id'],'] I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                    else:
                        try:
                            print('[Info][',msg['message_id'],'] ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        except:
                            print('[Info][',msg['message_id'],'] ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                else:
                    try:
                        print('[Info][',msg['message_id'],']',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                    except:
                        print('[Info][',msg['message_id'],']',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                return
            try:
                print('[Info][',msg['message_id'],']',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
            except:
                print('[Info][',msg['message_id'],']',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
            if msg['text'] == '/a2z' or msg['text'] == '/a2z@'+username:
                bot.sendMessage(chat_id,'請回覆一個信息來將英文字母轉成注音',reply_to_message_id=msg['message_id'])
        else:
            if content_type != 'text':
                if content_type == 'new_chat_member':
                    if msg['new_chat_member']['id'] == bot_me['id']:
                        try:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                        except:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                                except:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                    else:
                        try:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        except:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                except:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                elif content_type == 'left_chat_member':
                    if msg['left_chat_member']['id'] == bot_me['id']:
                        try:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                        except:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                                except:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                    else:
                        try:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                        except:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                except:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                else:
                    try:
                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                    except:
                        try:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                        except:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                            except:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                return
            try:
                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
            except:
                try:
                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                except:
                    try:
                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                    except:
                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
            if msg['text'] == '/a2z' or msg['text'] == '/a2z@'+username:
                try:
                    tcm = reply_to['text']
                except:
                    try:
                        bot.sendMessage(chat_id,'@' + msg['from']['username'].replace(' ','') + ' ,請回復一個文字信息',reply_to_message_id=reply_to['message_id'])
                    except:
                        bot.sendMessage(chat_id,msg['from']['first_name'].replace(' ','')+' '+msg['from']['last_name'].replace(' ','') + ' ,請回復一個文字信息',reply_to_message_id=reply_to['message_id'])
                        bot.sendMessage(chat_id,'機器人發現您沒有設置用戶名稱(username),所以我只能這樣tag您',reply_to_message_id=msg['message_id'])
                        bot.sendMessage(chat_id,'請設置用戶名稱，以獲得更好的體驗',reply_to_message_id=msg['message_id'])
                        bot.sendMessage(chat_id,'https://telegram.me/StartTG/92',reply_to_message_id=msg['message_id'])
                else:
                    string=a2z(tcm)
                    bot.sendMessage(chat_id,string,reply_to_message_id=reply_to['message_id'])
                    print('[Info] --->',string)
                
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
    zh = zh.replace('1','ㄅ')
    zh = zh.replace('2','ㄉ')
    zh = zh.replace('3','ˇ')
    zh = zh.replace('4','ˋ')
    zh = zh.replace('5','ㄓ')
    zh = zh.replace('6','ˊ')
    zh = zh.replace('7','˙')
    zh = zh.replace('8','ㄚ')
    zh = zh.replace('9','ㄞ')
    zh = zh.replace('0','ㄢ')
    zh = zh.replace('-','ㄦ')
    zh = zh.replace('q','ㄆ')
    zh = zh.replace('w','ㄊ')
    zh = zh.replace('e','ㄍ')
    zh = zh.replace('r','ㄐ')
    zh = zh.replace('t','ㄔ')
    zh = zh.replace('y','ㄗ')
    zh = zh.replace('u','ㄧ')
    zh = zh.replace('i','ㄛ')
    zh = zh.replace('o','ㄟ')
    zh = zh.replace('p','ㄣ')
    zh = zh.replace('a','ㄇ')
    zh = zh.replace('s','ㄋ')
    zh = zh.replace('d','ㄎ')
    zh = zh.replace('f','ㄑ')
    zh = zh.replace('g','ㄕ')
    zh = zh.replace('h','ㄘ')
    zh = zh.replace('j','ㄨ')
    zh = zh.replace('k','ㄜ')
    zh = zh.replace('l','ㄠ')
    zh = zh.replace(';','ㄤ')
    zh = zh.replace('z','ㄈ')
    zh = zh.replace('x','ㄌ')
    zh = zh.replace('c','ㄏ')
    zh = zh.replace('v','ㄒ')
    zh = zh.replace('b','ㄖ')
    zh = zh.replace('n','ㄙ')
    zh = zh.replace('m','ㄩ')
    zh = zh.replace(',','ㄝ')
    zh = zh.replace('.','ㄡ')
    zh = zh.replace('/','ㄥ')
    return zh



bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

bot.message_loop({'chat': on_chat_message})
print('[Info] Bot has started')
print('[Info] Listening ...')


# Keep the program running.
while 1:
    time.sleep(10)
