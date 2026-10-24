from m5stack import *
from m5stack import lcd
from m5ui import *
from uiflow import *
import network
import time
import socket

lcd.clear() # 画面の初期化
#=========接続処理==============================
#---------接続設定-----------
SSID = 'ka-ko-he'
PASS = 'kana-shin-mai'
target_ip = '192.168.111.1' # 接続先サーバのアドレス
target_port = 8080          # 接続先サーバのポート
buffer_size = 16384          # バッファサイズ
#---------接続処理-----------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    lcd.print('Connecting WiFi: {}'.format(SSID) )
    wlan.connect(SSID, PASS)
    time.sleep_ms(100)
    while not wlan.isconnected():
        lcd.print('.')
        time.sleep_ms(200)
lcd.print('\nConnected!\n')
rssi = wlan.status('rssi') # 電波強度確認
myip, mynetmask, myroute, mydns = wlan.ifconfig() # ネットワーク設定取得
lcd.print('IP addr: {}\n'.format(myip))
lcd.print('netmask: {}\n'.format(mynetmask))
lcd.print('gateway: {}\n'.format(myroute))
lcd.print('DNS: {}\n'.format(mydns))
lcd.print('RSSI: {} dBm\n'.format(rssi))


#======プレイヤークラス====
class Player():
    def __init__(self,p_num):
        self.p_num=""
        self.action    = [["bet","check","fold"],# まだ誰も賭けていない時（賭けるbet、様子見check、降りるfold）
                          ["call","raise","fold"],# すでに賭けられている時（同じ額を賭けるbet、より多くの額を賭けるraise、降りるfold）
                          ]
    def p_name(self):
        return "Player"+str(self.p_num)

#====アニメーションクラス====
class Animation:
    def __init__(self):
        self.color=lcd.BLUE
    
    #画面1
    def connectting(self):

        lcd.font(lcd.FONT_DejaVu18)
        time.sleep(1)
        lcd.print('connecting the game​​',60,105,lcd.BLACK)
    
        while True:
            x = 270 
            y = 120
        
            # 黒点を3回連続で表示
            for i in range(3):
                lcd.fillCircle(x, y, 2, lcd.BLACK)  # 黒点を表示
                time.sleep(0.5)  # 0.5秒待つ
                x += 10  # 次の点のX座標を移動

            # X座標をリセット
            x = 270

            # 黒点を3回連続で消す
            for i in range(3):
                lcd.fillCircle(x, y, 2, self.color)  # 点を白で上書きして消す
                time.sleep(0.5)  # 0.5秒待つ
                x += 10  # 次の点のX座標を移動

            # X座標をリセット
            x = 270

    #画面2
    def waiting(self):
        lcd.font(lcd.FONT_DejaVu18)
        time.sleep(1)
        lcd.print('You joined the game​',60,95,lcd.BLACK)
        time.sleep(2)
        lcd.print('waiting for player2​',60,115,lcd.BLACK)
    
        while True:
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
                lcd.fillCircle(x, y, 2, self.color)  # 点を白で上書きして消す
                time.sleep(0.5)  # 0.5秒待つ
                x += 10  # 次の点のX座標を移動

            # X座標をリセット
            x = 200

    #画面3
    def starting(self):
        lcd.font(lcd.FONT_DejaVu18)
        time.sleep(1)
        lcd.print('All players are now present.​',22,95,lcd.BLACK)
        time.sleep(2)
        lcd.print('starting the game​',75,115,lcd.BLACK)

        for i in range(3, 0, -1):  # 3から1までカウントダウン
            lcd.fillRect(160,135,30,30,color)
            lcd.print(+int(i), 160, 135, lcd.BLACK)  # 秒数を表示
            time.sleep(1)  # 1秒停止
    
    #勝敗画面
    def result(self,bet_num,game_win):
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
                    lcd.print('Touch to continue', 70, 205, lcd.BLACK)
                    time.sleep(0.5)
                    lcd.fillRect(70, 205, 180, 20,0x006400)
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
    def drow_card(self,x,y,i):
        # カードを描画
        lcd.fillRect(x, y, 40, 60, lcd.WHITE)
        lcd.rect(x, y, 40, 60, lcd.BLUE)
        if  i[0]== "H" or i[0]=="D":
            color = lcd.RED
        else:
            color = lcd.BLACK
        
        lcd.font(lcd.FONT_DejaVu18)
        print(i)
        lcd.print(i[0],x + 14, y + 5, color)
        lcd.print(i[1],x + 14, y + 40, color)

    def drow_all_card(self,l):
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

    def drow_static_elements(self):
        #基本描写
        lcd.clear(0x006400)
        lcd.line(0,200,320,200,lcd.BLACK)
        lcd.line(60,0,60,200,lcd.BLACK)
        
        # プレイヤー情報の表示
        y = 10
        lcd.font(lcd.FONT_DejaVu18)
        for player in players:
            lcd.print(player[0], 3, y, lcd.BLACK)
            lcd.print(str(player[1]), 5, y+20, lcd.BLACK)
            y += 50

        # 合計表示
        lcd.print("Total", 3, y, lcd.BLACK)
        lcd.print(total_score, 5, y+20, lcd.BLACK)

        # ヒント表示
        lcd.print("Your tip : " + str(your_tip), 70, 10, lcd.BLACK)
        lcd.print("info", 275, 10, lcd.BLACK)

        # ボタンラベル
        lcd.font(lcd.FONT_DejaVu24)
        lcd.print("Call", 32, 210, lcd.BLACK)
        lcd.print("Bet:" + str(current_bet), 124, 210, lcd.BLACK)
        lcd.print("OK", 250, 210, lcd.BLACK)
anime = Animation()#もうここで使えるようにする

# プレイヤーデータ
players = [["P1", 123], ["P2", 456], ["P3", 789]]
total_score = "1898"
your_tip = 99999
current_bet = 10
bet_num=100

game_win=0
change_num=200





#===========通信で使用する関数==================
def decode_str(c_str):
    message = {}
    msg_list = c_str.split("*")
    for c_str in msg_list:
        name, value = c_str.split(":")
        message[name] = value
    return message
def card_decode(card_str):
    com_hands = card_str.split("+")
    all_cards = []
    for hand in com_hands:
        card_list = hand.split("^")
        cards = []
        for card in card_list:
            cards.append(card.split("-"))
        all_cards.append(cards)
    return all_cards
def send(client,message):
    byte_message=bytes(message,"utf-8")
    client.send(byte_message)
def receive(client):
    data_str=client.recv(buffer_size).decode("utf-8")
    return decode_str(data_str)
class Game():
    def __init__(self):
        self.p_num=0
        self.bg_col=0x006400
    def set_input(self,ipt):
        self.button=ipt
    def input_get(self):
        Ipt=self.button
        self.button  = ""
        return Ipt
    def Connect_Server(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.connect((target_ip,target_port))
    def Start_game(self):
        lcd.clear(self.bg_col)
        message=receive(self.tcp_client)
        card_info=message["card"]
        #print(card_info)
        d_card=card_decode(card_info)
        anime.drow_static_elements()
        anime.drow_all_card(d_card)
#=======実行関数==============
def main():
    
    game  = Game()

    btnA.wasPressed(lambda:game.input_set("A"))
    btnB.wasPressed(lambda:game.input_set("B"))
    btnC.wasPressed(lambda:game.input_set("C"))
    #サーバーに接続
    game.Connect_Server()
    game.Start_game()




    #drow_all_card(d_card)

    
    #anime.connectting()



    # 描画


    #anime.result(bet_num,game_win)

#=======実行==================
main()