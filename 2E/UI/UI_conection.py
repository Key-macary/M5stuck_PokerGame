from m5stack import *
from m5ui import *
from uiflow import *
import random
import time




#画面1
def connectting():
    color = 0x006400
    lcd.clear(color)
    lcd.fillRect(30, 100, 260, 28, lcd.WHITE)
    lcd.rect(30, 100, 260, 28, lcd.RED)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.print('connecting the game​​',45,105,lcd.BLACK)

    
    start_time = time.time()  # 開始時間を記録
    while True:
        if time.time() - start_time >= 5:  # 5秒が経過したらループを抜ける
            break

        x = 260 
        y = 120
        
        # 黒点を3回連続で表示
        for i in range(3):
            lcd.fillCircle(x, y, 2, lcd.BLACK)  # 黒点を表示
            time.sleep(0.5)  # 0.5秒待つ
            x += 10  # 次の点のX座標を移動

        # X座標をリセット
        x = 260

        # 黒点を3回連続で消す
        for i in range(3):
            lcd.fillCircle(x, y, 2, lcd.WHITE)  # 点を白で上書きして消す
            time.sleep(0.5)  # 0.5秒待つ
            x += 10  # 次の点のX座標を移動

        # X座標をリセット
        x = 260


#画面2
def waiting():
    color = 0x006400
    lcd.clear(color)
    lcd.fillRect(30, 75, 260, 80, lcd.WHITE)
    lcd.rect(30, 75, 260, 80, lcd.RED)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.print('You joined the game​',60,95,lcd.BLACK)
    time.sleep(2)
    lcd.print('waiting for player2​',60,115,lcd.BLACK)
    
    while True:
        if time.time() - start_time >= 5:  # 5秒が経過したらループを抜ける
            break
        
        x = 260 
        y = 130
        
        # 黒点を3回連続で表示
        for i in range(3):
            lcd.fillCircle(x, y, 2, lcd.BLACK)  # 黒点を表示
            time.sleep(0.5)  # 0.5秒待つ
            x += 10  # 次の点のX座標を移動

        # X座標をリセット
        x = 260

        # 黒点を3回連続で消す
        for i in range(3):
            lcd.fillCircle(x, y, 2, lcd.WHITE)  # 点を白で上書きして消す
            time.sleep(0.5)  # 0.5秒待つ
            x += 10  # 次の点のX座標を移動

        # X座標をリセット
        x = 200

       

#画面3
def starting():
    color = 0x006400
    lcd.clear(color)
    lcd.fillRect(5, 70, 310, 100, lcd.WHITE)
    lcd.rect(5, 70, 310, 100, lcd.RED)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.print('All players are now present.​',22,95,lcd.BLACK)
    time.sleep(2)
    lcd.print('starting the game​',75,115,lcd.BLACK)
    time.sleep(2)

    for i in range(3, 0, -1):  # 3から1までカウントダウン
        lcd.font(lcd.FONT_DejaVu24)
        lcd.fillRect(145,140,25,25,lcd.WHITE)
        lcd.print(+int(i), 152, 142, lcd.BLACK)  # 秒数を表示
        time.sleep(1)  # 1秒停止
        
connectting()