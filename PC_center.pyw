import telebot , os , time , datetime , pytz
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import win32com.client
import threading
from threading import Thread
import win32com.client
import pyautogui

colMonitoredEvents = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".", "root\cimv2").ExecNotificationQuery("Select * from Win32_PowerManagementEvent")

User_Chat_id = (YOUR_CHAT_ID)
bot = telebot.TeleBot('TOKEN')
notfication = True




colMonitoredEvents = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".", "root\cimv2").ExecNotificationQuery("Select * from Win32_PowerManagementEvent")
Full_time_format = '%Y-%m-%d --- %H:%M:%S'
tz = pytz.timezone('Asia/Riyadh')
jt = datetime.now(tz)
date_now = (jt.strftime(Full_time_format))

bot.send_message(User_Chat_id,f'*System Started Successfully ✅!* \n {date_now}' , parse_mode='markdown')
print ("Started!")
try:
    os.remove ('Running_tasks.txt')
except:
    pass


def commends_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    markup.add(InlineKeyboardButton("Shutdown 🛑", callback_data="shutdown"))
    markup.add(InlineKeyboardButton("Restart ♻️", callback_data="restart"))
    markup.add(InlineKeyboardButton("Sleep 💤", callback_data="sleep"))
    markup.add(InlineKeyboardButton("Apps 🔰", callback_data="apps"))
    markup.add(InlineKeyboardButton("Screenshot 🖼️", callback_data="screenshot"))
    markup.add(InlineKeyboardButton("Chrome 💠", callback_data="chrome"))
    markup.add(InlineKeyboardButton("Paladins 💠", callback_data="paladins"))
    markup.add(InlineKeyboardButton("ُ", callback_data="1"))
    markup.add(InlineKeyboardButton("Settings ⚙️", callback_data="settings"))


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


    elif call.data == "apps":

        try:
            x = os.popen('tasklist /v|find /v /i " services "').read()
            if "Paladins" in x:
                bot.send_message (chat_id=User_Chat_id , text='Paladins is Running!')
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


    elif call.data == "chrome":
        try:
            chrome_status = os.popen('taskkill /IM chrome.exe /F').read()
            if '"chrome.exe" not found.' in chrome_status:
                bot.send_message(User_Chat_id , "Chrome isn't running !")
            else:
                bot.send_message(User_Chat_id,f'*Chrome is Killed 💠* \n {date_now}' , parse_mode='markdown')
        except Exception as e:
            bot.send_message(User_Chat_id,f"Error: \n \n {e}")


    elif call.data == "paladins":
        try:
            paladins_status = os.popen('taskkill /IM Paladins.exe /F').read()
            print (paladins_status)
            if '"Paladins.exe" not found.' in paladins_status:
                bot.send_message(User_Chat_id , "Paladins isn't running !")
            else:
                bot.send_message(User_Chat_id,f'*Paladins is Killed 💠* \n {date_now}' , parse_mode='markdown')
        except Exception as e:
            bot.send_message(User_Chat_id,f"Error: \n \n {e}")
    
    elif call.data == 'screenshot':
        screenshot = pyautogui.screenshot()
        bot.send_photo(User_Chat_id,screenshot)


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


if __name__ == "__main__":
    Thread(target=lambda: bot.infinity_polling()).start()




#it works but i don't want it anymore (:
#while True:
#    try:
#        if notfication == True:
#            x = os.popen('tasklist /v|find /v /i " services "').read()
#            if "Paladins" in x:
#                bot.send_message (chat_id=User_Chat_id , text='Paladins is Running (❁´◡`❁)')
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
