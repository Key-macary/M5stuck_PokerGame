from m5stack import *
from m5ui import *
from uiflow import *
import random
import time

dic={
    "card":"S-2^H-j",
    "action":"bet",
    "bet":"100"
    }


def info():
    color = 0x006400
    color_text = lcd.WHITE
    lcd.clear(lcd.BLACK)
    
    #背景
    lcd.fillRect(10, 10, 145, 105, color)
    lcd.fillRect(10, 125, 145, 105, color)
    lcd.fillRect(165, 125, 145, 105, color)
    lcd.fillRect(165, 10, 145, 105, color)
    #P1~3背景
    lcd.fillRect(17,17, 30, 19, lcd.RED)
    lcd.fillRect(167,17, 30, 19, lcd.BLUE)
    lcd.fillRect(17,127, 30, 19, 0xffa500)

    #P1情報
    lcd.font(lcd.FONT_DejaVu18)
    lcd.print('P1', 20, 20,lcd.WHITE)
    lcd.print('Fund:',20,37,color_text)
    lcd.print('Bet:'+str(dic["bet"]),35,54,color_text)
    lcd.print('Get:',34,71,color_text)
    lcd.print('Lost:',30,88,color_text)
    
    #P2情報
    lcd.font(lcd.FONT_DejaVu18)
    lcd.print('P2', 170, 20,lcd.WHITE)
    lcd.print('Fund:',170,37,color_text)
    lcd.print('Bet:'+str(dic["bet"]),185,54,color_text)
    lcd.print('Get:',184,71,color_text)
    lcd.print('Lost:',180,88,color_text)
    
    #P3情報
    lcd.font(lcd.FONT_DejaVu18)
    lcd.print('P3', 20, 130,lcd.WHITE)
    lcd.print('Fund:',20,147,color_text)
    lcd.print('Bet:'+str(dic["bet"]),35,164,color_text)
    lcd.print('Get:',34,181,color_text)
    lcd.print('Lost:',30,198,color_text)
    

    lcd.print('Players',182, 155, color_text)
    lcd.print('Informetion',182, 175, color_text)

info()