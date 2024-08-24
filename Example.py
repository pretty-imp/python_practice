import pyautogui as pg                          # import pyautogui for pictures searching
import time
import pyscreeze                                # module for pyautogui
import telebot                                  # module for telegram bot manipulations
from threading import Thread                    # multitasking for telegram bot and bot simultaneous working
# -------------------BOT---------------------
TOKEN = '<Telegram bot token>'                  # token for telegram bot messaging
bot = telebot.TeleBot(TOKEN)
TARGET_CHAT_ID = '<Chat id>'                    # chat id for receiving a message from telegram bot
MESSAGE_THREAD_ID = '<Thread id>'               # channel chat id
# ---------------------------------------------


def scroll(a):                                  # function for hunting field scrolling
    if a % 2 == 0:
        pg.click(1645, 284)               # scroll up
    else:
        pg.click(1645, 924)               # scroll down
    time.sleep(0.5)


def hunting():                                  # function for manipulations with mob on hunting field
    pg.click((300, 360))                        # focusing on hunting field after script starting
    reg = (275, 290, 1355, 710)                 # hunting field square zone where bot is searching mobs
    s = 1                                       # variable for scrolling
    while True:
        last = 0                                # last busied mob
        while True:
            s += 1                              # change direction for scrolling
            try:
                img_list = list(pg.locateAllOnScreen('mob.png', region=reg, confidence=0.7))  # recognizing all
                for p in img_list:                                                                  # mobs on hunting
                    try:                                                                            # field
                        pg.locateOnScreen('i.png', region=(p[0]+10, p[1]-50, p[2]+50, p[3]+50), confidence=0.8)
                        if p == img_list[-1]:   # checking if the mob is already busy
                            last = 1            # the last busy mob
                    except pg.ImageNotFoundException:
                        pg.doubleClick(p[0] + 30, p[1] - 30, interval=0.3)      # attacking the mob
                        break
            except pyscreeze.ImageNotFoundException:    # there are no mobs, need to scroll the hunting field
                scroll(s)
                time.sleep(0.5)
                break
            if last == 1:  # if all mobs are busy, need to scroll the hunting field
                scroll(s)
                break
            time.sleep(0.9)
            try:
                pg.locateOnScreen('busy.png', confidence=0.9)   # after attacking there is a busy mob appeared
                time.sleep(0.5)
                x, y = pg.locateCenterOnScreen('cancel.png', confidence=0.8)  # skipping busy mob
                pg.click(x, y)
                pg.hotkey('alt', 'w')
                scroll(s)
                break
            except pg.ImageNotFoundException:
                pass
            time.sleep(0.3)
            try:
                pg.locateOnScreen('tired.png', confidence=0.9)  # after attacking there is a dead mob appeared
                time.sleep(0.3)
                x, y = pg.locateCenterOnScreen('close.png', confidence=0.8)  # skipping the alert window
                pg.click(x, y)
                pg.hotkey('alt', 'w')
                scroll(s)
                break
            except pg.ImageNotFoundException:
                pass
            try:
                pg.locateOnScreen('captcha.png', confidence=0.9)  # bot checking system window appeared
                bot.send_message(TARGET_CHAT_ID, f"Captcha on the bot", message_thread_id=MESSAGE_THREAD_ID)
                time.sleep(20)  # receiving the message from telegram bot about captcha window
            except pg.ImageNotFoundException:
                pass       
            while True:
                try:
                    pg.locateOnScreen('end.png', confidence=0.9)  # checking the end of battle
                    break
                except pg.ImageNotFoundException:    # if the battle is not finished after attacking the mob
                    pg.press('w', presses=15)  # need to hold the cast spell button before battle downloaded
                    pg.press('2')                   # using an amplification from second pocket
                    pg.press('3')                   # using an amplification from second pocket
                    pg.keyDown('q')                 # holding another spell button to try to kill with oneshot
            pg.keyUp('q')
            pg.hotkey('alt', 'w')             # entering the hunting field after battle ending
            time.sleep(0.5)


hunt = Thread(target=hunting)       # hunting function process
hunt.start()                        # hunting function process start
bot = Thread(target=bot.polling())  # telegram bot start process
bot.start()                         # telegram bot start process start
