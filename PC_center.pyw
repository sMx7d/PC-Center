import telebot , os , time , datetime , pytz
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import win32com.client
import threading
from threading import Thread
import win32com.client
import mss
import mss.tools
from PIL import Image
import io
from io import BytesIO
import psutil


#TODO : single menu for apps
colMonitoredEvents = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".", "root\cimv2").ExecNotificationQuery("Select * from Win32_PowerManagementEvent")

User_Chat_id = (YOUR_CHAT_ID)
bot = telebot.TeleBot('TOKEN')
tz = pytz.timezone('TIMEZONE')

notfication = True




colMonitoredEvents = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".", "root\cimv2").ExecNotificationQuery("Select * from Win32_PowerManagementEvent")
Full_time_format = '%Y-%m-%d --- %H:%M:%S'
jt = datetime.now(tz)
date_now = (jt.strftime(Full_time_format))

#print ("Started!")
try:
    os.remove ('Running_tasks.txt')
except:
    pass


def commends_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    markup.add(InlineKeyboardButton("Shutdown 🛑", callback_data="shutdown"))
    markup.add(InlineKeyboardButton("Restart ♻️", callback_data="restart"), InlineKeyboardButton("Sleep 💤", callback_data="sleep"))
    markup.add(InlineKeyboardButton("Apps 🔰", callback_data="Apps"), InlineKeyboardButton("Running Tasks 📃", callback_data="Tasks"))
    markup.add(InlineKeyboardButton("Screenshot 🖼️", callback_data="screenshot"))
    markup.add(InlineKeyboardButton("System Info 🖥️", callback_data="sysinfo"))

    markup.add(InlineKeyboardButton("ُ", callback_data="1"))
    markup.add(InlineKeyboardButton("Settings ⚙️", callback_data="settings"))


    return markup

def apps_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3


    markup.add(InlineKeyboardButton("WhatsApp 🟢", callback_data="WhatsApp"))
    markup.add(InlineKeyboardButton("Brave 🟠", callback_data="Brave"))
    markup.add(InlineKeyboardButton("Telegram 🔵", callback_data="Telegram"))



    return markup

def settings_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    markup.add(InlineKeyboardButton("ON ✅", callback_data="ON"))
    markup.add(InlineKeyboardButton("OFF ❎", callback_data="OFF"))

    return markup


@bot.message_handler(commands=['start'])
def start (message):
    global start_message
    start_message = bot.send_message(User_Chat_id,'*System Is Running  💫* \n _Notifications: ON 🔊_', parse_mode='markdown' , reply_markup=commends_markup()).message_id
    print (start_message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global chat_id2
    global notfication
    global start_message
    global notfication_message
    jt = datetime.now(tz)
    date_now = (jt.strftime(Full_time_format))


    if call.data == "shutdown":
        
        try:
            os.system('shutdown /s /t 1')
            bot.send_message(User_Chat_id,f'*System Is Off ❇️* \n {date_now}' , parse_mode='markdown')
        except Exception as e:
            bot.send_message(User_Chat_id,f"Error: \n \n {e}")


    elif call.data == "restart":
        try:
            os.system('shutdown /r')
            bot.send_message(User_Chat_id,f'*System Is Restarting 🔄️* \n {date_now}' , parse_mode='markdown')
        except Exception as e:
            bot.send_message(User_Chat_id,f"Error: \n \n {e}")


    elif call.data == "sleep":

        bot.send_message(User_Chat_id,f'*System Is Sleeping 💤* \n {date_now}' , parse_mode='markdown')
        os.system('powercfg /hibernate off')
        os.system('RUNDLL32.EXE powrprof.dll,SetSuspendState 0,1,0')


    elif call.data == "Tasks":

        try:
            x = os.popen('tasklist /v|find /v /i " services "').read()
            if "WhatsApp" in x:
                bot.send_message (chat_id=User_Chat_id , text='WhatsApp is Running!')
            else:
                pass
            with open ("Running_tasks.txt", "a") as log_apps:
                log_apps.write(x)
                log_apps.close()

            log_apps_file = open ("Running_tasks.txt", "rb")
            bot.send_document(chat_id=User_Chat_id,caption=f'*Running Apps 🔰* \n {date_now}', document=log_apps_file , parse_mode='markdown')
            log_apps_file.close()
            os.remove ('Running_tasks.txt')

        except Exception as e:
            bot.send_message(User_Chat_id,f"Error: \n \n {e}")


    elif call.data == "Brave":
        try:
            Brave_status = os.popen('taskkill /IM Brave.exe /F').read()
            if '"Brave.exe" not found.' in Brave_status:
                bot.send_message(User_Chat_id , "Brave isn't running !")
            else:
                bot.send_message(User_Chat_id,f'*Brave is Killed 💠* \n {date_now}' , parse_mode='markdown')
        except Exception as e:
            bot.send_message(User_Chat_id,f"Error: \n \n {e}")


    elif call.data == "WhatsApp":
        try:
            WhatsApp_status = os.popen('taskkill /IM WhatsApp.exe /F').read()
            WhatsApp_status = WhatsApp_status.strip()
            WhatsApp_trigger = ('ERROR: The process "WhatsApp.exe" not found.').strip()
            print (str(WhatsApp_status))
            if str(WhatsApp_trigger) == str(WhatsApp_status):
                bot.send_message(User_Chat_id, "WhatsApp isn't running !")
            else:
                bot.send_message(User_Chat_id, f'*WhatsApp is Killed 💠* \n {date_now}', parse_mode='markdown')
        except Exception as e:
            bot.send_message(User_Chat_id, f"Error: \n \n {e}")
            
    elif call.data == "Telegram":
        try:
            Telegram_status = os.popen('taskkill /IM Telegram.exe /F').read()
            print (Telegram_status)
            if '"Telegram.exe" not found.' in Telegram_status:
                bot.send_message(User_Chat_id , "Telegram isn't running !")
            else:
                bot.send_message(User_Chat_id,f'*Telegram is Killed 💠* \n {date_now}' , parse_mode='markdown')
        except Exception as e:
            bot.send_message(User_Chat_id,f"Error: \n \n {e}")
            
    elif call.data == "screenshot":
        with mss.mss() as sct:
            screenshot_time_format = '%Y-%m-%d -- %I:%M %p'
            date_now = (jt.strftime(screenshot_time_format))
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.name = f'screenshot_{date_now}.png'
            img_io.seek(0)
            bot.send_document(User_Chat_id, img_io)

    elif call.data == "sysinfo":
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        uptime = time.time() - psutil.boot_time()
        bot.send_message(User_Chat_id, f"*System Info:*\n🖥️ CPU: {cpu}%\n💾 RAM: {ram.percent}%\n📀 Disk: {disk.percent}%\n⏳ Uptime: {int(uptime/3600)}h {int((uptime%3600)/60)}m", parse_mode='markdown')




    elif call.data == "settings":
        notfication_message = bot.send_message(text="Notifications 🔔" , chat_id=User_Chat_id , reply_markup=settings_markup()).message_id
        #notfication_message2 = bot.edit_message_reply_markup(User_Chat_id , notfication_message , reply_markup=settings_markup()).message_id
    


    elif call.data == "ON":
        notfication = True
        bot.delete_message(User_Chat_id , notfication_message)
        start_message = bot.send_message(User_Chat_id,'*System Is Running  💫* \n   _Notifications: ON 🔊_', parse_mode='markdown' , reply_markup=commends_markup()).message_id

    elif call.data == "OFF":
        notfication = False
        bot.delete_message(User_Chat_id , notfication_message)
        start_message = bot.send_message(User_Chat_id,'*System Is Running  💫* \n   _Notifications: OFF 🔈_', parse_mode='markdown' , reply_markup=commends_markup()).message_id

    elif call.data == "Apps":
        start_message = bot.send_message(User_Chat_id,'ًُ', parse_mode='markdown' , reply_markup=apps_markup()).message_id

def Main ():
    bot.infinity_polling()
while True:
    try:
        Thread(target=lambda: Main()).start()
        print ("Running!")
        bot.send_message(User_Chat_id,f'*System Started Successfully ✅!* \n {date_now}' , parse_mode='markdown', reply_markup=commends_markup())

        break
    except Exception as e:
        print (e)
        time.sleep (10)
        pass


#works but not needed for me

#while True:
#    try:
#        if notfication == True:
#            x = os.popen('tasklist /v|find /v /i " services "').read()
#            if "WhatsApp" in x:
#                bot.send_message (chat_id=User_Chat_id , text='WhatsApp is Running (❁´◡`❁)')
#            elif "Steam" in x:
#                bot.send_message (chat_id=User_Chat_id , text='Steam is Running ☆*: .｡. o(≧▽≦)o .｡.:*☆')
#            else:
#                print ("not running")
#                pass
#
#        elif notfication == False:
#            print ('No notification')
#            pass
#
#        time.sleep (1000)
#    except:
#        pass
#
