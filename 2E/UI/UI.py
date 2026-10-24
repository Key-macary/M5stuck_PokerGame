from m5stack import *
from m5ui import *
from uiflow import *
import random
import time

#カードデータ
community_card = [[["S", 9], ["H", 6], ["S", 8], ["S", 4], ["C", 4]],\
                  [["S", 6], ["D", 8], ["S", 4]]]

# プレイヤーデータ
players = [["P1", 123], ["P2", 456], ["P3", 789]]
total_score = "1898"
your_tip = 99999
current_bet = 10





def drow_card(x,y,i):
    # カードを描画
    lcd.fillRect(x, y, 40, 60, lcd.WHITE)
    lcd.rect(x, y, 40, 60, lcd.BLUE)
    if  i[0]== "H" or i[0]=="D":
        color = lcd.RED
    else:
        color = lcd.BLACK
    
    lcd.font(lcd.FONT_DejaVu18)
    lcd.print(i[0],x + 14, y + 5, color)
    lcd.print(i[1],x + 14, y + 40, color)


def drow_all_card(l):
    #テーブルカードを表示
    x = 70
    y = 40
    for i in l[0]:
        drow_card(x,y,i)
        x += 50

    x = 70
    y = 125
    for i in l[1]:
        drow_card(x,y,i)
        x += 50

def drow_static_elements():
    #基本描写
    lcd.clear(0x006400)
    lcd.fillRect(0,0,60, 200, lcd.BLACK)
    lcd.fillRect(0,200,106, 40, 0xb22222)
    lcd.fillRect(106,200,112,40, lcd.BLACK)
    lcd.fillRect(218,200,110, 40, 0xb22222)
    lcd.fillRect(273,6,42,20,0xdaa520)
    lcd.rect(273,6,42,20,0xdc143c)
    lcd.line(0,200,320,200,lcd.BLACK)
    lcd.line(60,0,60,200,lcd.BLACK)
    
    
    # プレイヤー情報の表示
    y = 10
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(lcd.WHITE)
    for player in players:
        lcd.print(player[0], 3, y)
        lcd.print(str(player[1]), 5, y+20)
        y += 50

    # 合計表示
    lcd.print("Total", 3, y)
    lcd.print(total_score, 5, y+20)

    # ヒント表示
    lcd.print("Your tip : " + str(your_tip), 70, 10)
    lcd.print("info", 275, 10, 0xdc143c)

    # ボタンラベル
    lcd.font(lcd.FONT_DejaVu24)
    lcd.print("Call", 32, 210)
    lcd.print("Bet:" + str(current_bet), 124, 210)
    lcd.print("OK", 250, 210)


# 描画
drow_static_elements()
drow_all_card(community_card)