from PIL import Image, ImageDraw
from telebot import types
import telebot
import time
import re
import os
import json

#individual bot token
token = "1022950277:AAFBiB615c0tExyam8Z6ILuH77MfdoB6avQ"

dir = os.path.abspath(os.curdir)

def makePNG(init1):
    init=" "
    init_r=""
    init_g=""
    init_b=""
    code_r=0
    code_g=0
    code_b=0



    if len(init1) == 7 and init1[0]=="#":
        for i in range(1, 7):
            if init1[i] not in '0123456789ABCDEFabcdef':
                print(init1[i])
                return 0 

        init_r = init1[1] + init1[2] 
        init_g = init1[3] + init1[4] 
        init_b = init1[5] + init1[6]

        code_r = int(convert_base(init_r))
        code_g = int(convert_base(init_g))
        code_b = int(convert_base(init_b))
        print(code_r)
        print(code_g)
        print(code_b)
    else:
        if len(init1) == 6:
            for i in range(6):
                if init1[i] not in '0123456789ABCDEFabcdef':
                    print(init1[i])
                    return 0 

            init_r = init1[0] + init1[1] 
            init_g = init1[2] + init1[3] 
            init_b = init1[4] + init1[5]

            code_r = int(convert_base(init_r))
            code_g = int(convert_base(init_g))
            code_b = int(convert_base(init_b))
        else:
            print("Invalid color code.")
            return 0

    color = (code_r, code_g, code_b)
    img = Image.new('RGB', (200, 200), color)
    imgDrawer = ImageDraw.Draw(img)
    img.save(init_r + init_g + init_b + ".png")
    return init_r + init_g + init_b + ".png"

def convert_base(num, to_base=10, from_base=16):
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id, "Привет! Я готов к работе, давай свой HEX-код : )")

@bot.message_handler(commands=['clean'])
def handle_text(message):
    file = open('stat/statistick' + str(message.chat.id) + '.json', 'w')
    json.dump({}, file)
    file.close()
    bot.send_message(message.chat.id, "Ура! благодаря тебе мой кэш наконец-то чист! Спасибо : )")
    print("###################\n\nCache is empty!\n\n###################")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    file = str(makePNG(message.text))
    if(file != "0"):
        img = open(dir+'/'+file,'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        for filename in os.listdir(dir+"/"):
            if filename.endswith('.png'):
                os.remove(filename)
                print(filename+" is deleted\n") 
        
        try:
            file = open('stat/statistick' + str(message.chat.id) + '.json', 'r')
        except FileNotFoundError:
            file = open('stat/statistick' + str(message.chat.id) + '.json', 'w')
            json.dump({}, file)
            file.close()
            file = open('stat/statistick' + str(message.chat.id) + '.json', 'r')
        finally:
            data = json.load(file)
            file.close()

        text = message.text.lower()
        if '#' in text:
            text = text[1:]
        if text in data:
            data[text] += 1
        else:
            data[text] = 1
        
        file = open('stat/statistick' + str(message.chat.id) + '.json', 'w')
        json.dump(data, file)
        file.close()
    else:
        bot.send_message(message.chat.id, "Такого цвета не существует.. Попробуй #ffcc00")


#need to finish
@bot.inline_handler(lambda query: len(query.query) != 0)
def query_text(inline_query):
    ok=0
    q = inline_query.query
    super_query = q.upper()
    print(super_query)
    if(len(super_query)==7 and super_query[0]=='#'):
        for i in range(1, 7):
            if super_query[i] not in '0123456789ABCDEFabcdef':
                print("Invalid code.")
                continue
            else:
                ok=1
    if(len(super_query)==6):
        for i in range(0, 6):
            if super_query[i] not in '0123456789ABCDEFabcdef':
                print("Invalid code.")
                continue
            else:
                ok=1
    if(ok == 1):         
        try:
            #hen picture
            pic = types.InlineQueryResultPhoto('1', 'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg', 'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg')
            bot.answer_inline_query(inline_query.id, [pic], cache_time=1)
        except Exception as e:
            print(e)

bot.polling(none_stop=True, interval=0)