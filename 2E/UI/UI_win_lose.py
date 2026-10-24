from m5stack import *
from m5ui import *
from uiflow import *
import random
import time



bet_num=100
game_win=0
change_num=200

def result(bet_num,game_win):
    color = 0x006400
    lcd.clear(color)

    if game_win==0:
        lcd.fillRect(50, 40, 225, 160, lcd.WHITE)
        lcd.rect(50, 40, 225, 160, lcd.RED)
        lcd.font(lcd.FONT_DejaVu40)
        time.sleep(1)
        lcd.print('You WIN!',70,75,lcd.RED)
        lcd.font(lcd.FONT_DejaVu24)
        time.sleep(1)
        lcd.print('Bet: ' + str(bet_num), 110, 115, lcd.BLACK)  # ベット金額を表示
        time.sleep(1)
        lcd.print('Get: ' + str(change_num), 107, 140, lcd.BLACK)  # 獲得金額を表示
        lcd.font(lcd.FONT_DejaVu18)
        time.sleep(2)
        while True:
                lcd.print('Touch to continue', 73, 205, lcd.BLACK)
                time.sleep(0.5)
                lcd.fillRect(73, 205, 180, 20,0x006400)
                time.sleep(0.5)
            
        
    else:
        lcd.fillRect(50, 40, 225, 160, lcd.WHITE)
        lcd.rect(50, 40, 225, 160, lcd.BLUE)
        lcd.font(lcd.FONT_DejaVu40)
        time.sleep(1)
        lcd.print('You LOSE',67,75,lcd.BLUE)
        lcd.font(lcd.FONT_DejaVu24)
        time.sleep(1)
        lcd.print('Bet: ' + str(bet_num), 110, 115, lcd.BLACK)  # ベット金額を表示
        time.sleep(1)
        lcd.print('Lost: ' + str(change_num), 100, 140, lcd.BLACK)  # 損失金額を表示
        lcd.font(lcd.FONT_DejaVu18)
        time.sleep(1)
        lcd.print('Touch to continue', 50, 200, lcd.BLACK)
        while True:
                lcd.print('Touch to continue', 70, 205, lcd.BLACK)
                time.sleep(0.5)
                lcd.fillRect(70, 205, 180, 20,0x006400)
                time.sleep(0.5)
        
    
        
result(bet_num,game_win)
 
 