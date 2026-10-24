from m5stack import *
import network
import time
import socket
import random
#===============ログ============
class Log():
    def __init__(self):
        self.log = []
        self.log_num = 1
        self.display_range = 18
    def add_log(self, a_log):
        self.log.append(str(self.log_num) + " : " + str(a_log))
        self.log_num += 1

        len_log = len(self.log)
        log_str = ""  # 初期化

        if len_log <= self.display_range:
            for i in range(len_log):
                log_str += str(self.log[i]) + "\n"
        else:
            for i in range(self.display_range):
                log_str += str(self.log[-self.display_range + i]) + "\n"
        lcd.clear(lcd.BLACK)
        lcd.setCursor(0,0)
        lcd.print(log_str)

log=Log()
#=========サーバー準備======================
#-------AP設定--------
SSID = 'ka-ko-he'              # アクセスポイント名
PASS = 'kana-shin-mai'                # 接続パスワード
AUTH = network.AUTH_WPA_WPA2_PSK # セキュリティ設定
MYIP = '192.168.111.1'           # IPアドレス
MYNETMASK = '255.255.255.0'      # ネットマスク
MYGATEWAY = '192.168.111.1'      # ゲートウェイIPアドレス
MYDNS = '192.168.111.1'          # DNS
MYNETINFO = (MYIP, MYNETMASK, MYGATEWAY, MYDNS) # 整形
#-----サーバー設定------
server_ip = '192.168.111.1' # 待受アドレス
server_port = 8080      # 待受ポート
listen_num = 5          # 同時接続数
buffer_size = 1024      # バッファサイズ
#--------AP起動---------
wlan = network.WLAN(network.AP_IF)
wlan.config(essid=SSID, password=PASS, authmode=AUTH)
wlan.ifconfig(MYNETINFO)
wlan.active(False)
time.sleep_ms(100) # 0.1秒待機
wlan.active(True) 
while wlan.active() is False: # 起動するまで待機
    pass
srvip, srvnetmask, srvroute, srvdns = wlan.ifconfig() # ネットワーク設定取得
log.add_log('IP addr: {}'.format(srvip))
log.add_log('netmask: {}'.format(srvnetmask))
log.add_log('gateway: {}'.format(srvroute))
log.add_log('DNS: {}'.format(srvdns))
log.add_log('AccessPoint has been activated.')

#-------サーバー起動--------
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((server_ip, server_port))
tcp_server.listen(listen_num)
log.add_log("Server Started")

#===========通信で使用する関数==================
def encode_str(cards):
    cards_str_list=[]
    for c in cards:
        c_str=""
        c_num=c[1]
        if c_num==11:
            c_num="J"
        elif c_num==12:
            c_num="Q"
        elif c_num==13:
            c_num="K"
        elif c_num==14:
            c_num="A"
        else:
            c_num=str(c_num)
        c_str+=c[0]+"-"+c_num
        cards_str_list.append(c_str)
    return '^'.join(cards_str_list)
def dict_str(dictio_str,name,value):#送る型を生成
    return str(dictio_str)+"*"+str(name)+":"+str(value)
def decode_str(message):#受け取った文字列をディクショナリに治す
    dic={}
    #行動名:行動*掛け金:100のように
    ms_split=message.split("*")
    for j in ms_split:
        name,value=j.split(":")
        dic[name]=value
    return dic 
def card_str(community,hand):
    #テーブルのデータと自分の手札を合わせるて文字列にする
    com_str=encode_str(community)
    hand_str=encode_str(hand)
    return "card:"+com_str+"+"+hand_str

# エンコード・デコードしたデータを送る貰う
def send(client,message):
    byte_message=str(message).encode('utf-8') 
    client.send(byte_message)
def receive(client):
    data_str=client.recv(buffer_size).decode("utf-8")
    data_list=decode_str(data_str)
    return data_list

#============ゲームで使用するクラス==============
#------------クラス-------------
class Card:
    def __init__(self):
        self.deck=[]#山札
        self.com_card=[]#コミュニティカード
        self.card_st=[]
        #[スペード，ハート，ダイヤ，クローバー]
        self.mark = ["S","H","D","C"]
        self.num  = [14,2,3,4,5,\
                    6,7,8,9,10,\
                    11,12,13
                ]
        for m in self.mark:
            for n in self.num:
                self.deck.append([m,n])
    def draw_card(self,t_list):
        while True:
            j=random.randint(0, len(self.deck)-1)
            if j in self.card_st:
                continue
            else:
                t_list.append(self.deck[j])
                self.card_st.append(j)
                break

class Player:
    def __init__(self,client,address,player_num):
        self.client    = client
        self.address   = address
        self.p_num     = player_num
        self.hand      = []
        self.stack     = 100#手持ちのチップ
        self.bet       = 15
        self.min_bet   = 10
        self.step      = 5


ROLE_RANKS = {
    "Royal Straight Flush" :10,
    "Straight Flush"       : 9,
    "Four of a Kind"       : 8,
    "Full House"           : 7,
    "Flush"                : 6,
    "Straight"             : 5,
    "Three of a Kind"      : 4,
    "Two Pair"             : 3,
    "One Pair"             : 2,
    "High Card"            : 1
}

def sort_cards(community,hand):
    """スート・数字の頻度を数える関数"""
    judge_cards = []  # 判別用リスト
    judge_cards.extend(community)
    judge_cards.extend(hand)
    suit_counts = [["S", 0], ["H", 0], ["D", 0], ["C", 0]]  # スートの頻度リスト
    num_counts = []  # 数字の頻度リスト

    # スートの頻度をカウント
    for c in judge_cards:
        num_list = [c[1] for c in judge_cards] # 数字のみをリスト化
        if c[0] == "S":
            suit_counts[0][1] += 1
        elif c[0] == "H":
            suit_counts[1][1] += 1
        elif c[0] == "D":
            suit_counts[2][1] += 1
        elif c[0] == "C":
            suit_counts[3][1] += 1

    # 数字の頻度をカウント
    for n in set(num_list):  # 重複を除く
        count = num_list.count(n)  # 各数字の出現回数
        num_counts.append([n, count])  # 数字とその頻度を追加
    num_counts = sorted(num_counts, key=lambda x: x[0], reverse=True)  # 数字の降順でソート

    return judge_cards, suit_counts, num_counts

def role_judge(cards, suits, nums):
    """役の判定を行う関数、役の名前と該当するカードを返す"""
    def is_straight(): # ストレートの判定関数
        # 5枚連続しているか確認
        for i in range(len(nums) - 4):
            if nums[i][0] - nums[i + 4][0] == 4:
                straight_n = [nums[i + j][0] for j in range(5)]
                straight_c = [c for c in cards if c[1] in straight_n]
                straight_c = sorted(straight_c, key=lambda x: x[1], reverse=True)
                return True, straight_c
        # ローボールストレート (A, 2, 3, 4, 5)
        if {14, 5, 4, 3, 2}.issubset(n[0] for n in nums):
            straight_c = [c for c in cards if c[1] in {14, 5, 4, 3, 2}]
            straight_c = sorted(straight_c, key=lambda x: x[1], reverse=True)
            return True, straight_c
        return False, []

    def is_flush(): # フラッシュの判定関数
        for s in suits:
            if s[1] >= 5:
                flush_c = (c for c in cards if c[0] == s[0])
                flush_c = sorted(flush_c, key=lambda x: x[1], reverse=True)
                return True, flush_c
        return False, None

    straight, straight_cards = is_straight()
    flush, flush_cards = is_flush()

    """以下、役の判定と抽出"""
    # ロイヤルストレートフラッシュまたはストレートフラッシュ
    if straight and flush:
        # フラッシュのカードとストレートのカードが一致しているか確認
        straight_flush_cards = [fc for fc in flush_cards if fc in straight_cards]
        if len(straight_flush_cards) == 5:
            if straight_cards[0] == 14:
                return "Royal Straight Flush", straight_flush_cards
            elif {5, 4, 3, 2, 14}.issubset(n[0] for n in straight_flush_cards): # ローボールストレート (A, 2, 3, 4, 5)
                straight_flush_cards.append(straight_flush_cards[0])
                straight_flush_cards.pop(0)
            return "Straight Flush", straight_flush_cards

    # フォーカード
    for n in nums:
        if n[1] == 4:
            four_cards = [c for c in cards if c[1] == n[0]]
            return "Four of a Kind", four_cards

    # 同じ数字が3枚,2枚ある数字の抜き出し
    trio = sorted((n[0] for n in nums if n[1] == 3), reverse=True)
    duo = sorted((n[0] for n in nums if n[1] == 2), reverse=True)

    # フルハウス
    if (trio and duo) or len(trio) == 2:
        if len(trio) == 2:
            full_house_cards = [c for c in cards if c[1] == trio[0]]
            full_house_cards.extend(c for c in cards if c[1] == trio[1])
        else:
            full_house_cards = [c for c in cards if c[1] == trio[0]]
            full_house_cards.extend([c for c in cards if c[1] == duo[0]])
        return "Full House", full_house_cards[:5]
    
    # フラッシュ
    if flush:
        return "Flush", flush_cards[:5]

    # ストレート
    if straight:
        if {14, 5, 4, 3, 2}.issubset(n[0] for n in straight_cards): # ローボールストレート (A, 2, 3, 4, 5)
                straight_cards.append(straight_cards[0])
                straight_cards.pop(0)
        straight_cards = [straight_cards[n] for n in range(len(straight_cards)) if straight_cards[n][1] != straight_cards[n-1][1]]
        return "Straight", straight_cards

    # スリーカード
    if trio:
        three_cards = [c for c in cards if c[1] == trio[0]]
        return "Three of a Kind", three_cards

    # ツーペア
    if len(duo) >= 2:
        two_pair_cards = (c for c in cards if c[1] in duo[:2])
        two_pair_cards = sorted(two_pair_cards, key=lambda x: x[1], reverse=True)
        kicker = max([c for c in cards if c not in two_pair_cards], key=lambda x: x[1])
        return "Two Pair", two_pair_cards + [kicker]

    # ワンペア
    if duo:
        one_pair_cards = [c for c in cards if c[1] == duo[0]]
        kicker = sorted([c for c in cards if c not in one_pair_cards], key=lambda x: x[1], reverse=True)[:3]
        return "One Pair", one_pair_cards + kicker

    # ハイカード
    high_card = sorted(cards, key=lambda x: x[1], reverse=True)
    return "High Card", high_card[:5]

def role_compare(player_roles):
    """複数プレイヤーの役を比較し勝者を決定する関数"""
    # プレイヤーごとの役の強さとカードの強さを計算
    sorted_roles = []
    for player_name, (role_name, cards) in player_roles:
        role_rank = ROLE_RANKS[role_name]  # 役の強さを取得
        sorted_cards = sorted(cards, key=lambda c: c[1], reverse=True)  # カードを強さ順にソート
        role_num = [c[1] for c in sorted_cards]  # 数字リストを作成
        sorted_roles.append((player_name, role_rank, role_num, role_name, cards))

    # 役の強さとカードの強さでソート
    sorted_roles = sorted(sorted_roles, key=lambda x: x[1], reverse=True)
    
    #### 動作確認 ##############
    for i in reversed(sorted_roles): # 一応全プレイヤーの役を出してみてる
        print(i,"\n")
    ###########################

    # 最強の役を持つプレイヤーを選択
    best_rank = sorted_roles[0][1]
    winners = [sorted_roles[0]]  # 最初のプレイヤーを勝者リストに追加

    # 他プレイヤーと同じ役か確認してカードで比較
    for player in sorted_roles[1:]:
        if player[1] < best_rank:  # これ以降の役は弱いため処理終了
            break
        if player[2] == winners[0][2]:  # 数字が完全一致
            winners.append(player)
        elif player[1] == best_rank:  # 役が同じならカード比較
            for w, p in zip(winners[0][2], player[2]):  # キッカーまで比較
                if w > p:
                    break
                elif w < p:
                    winners = [player]
                    break

    # 結果の処理
    if len(winners) == 1:
        winner = winners[0]
        return winner[0], winner[3], winner[4]  # プレイヤー名、役名、カードリスト
    else:
        return "Draw", [winner[0] for winner in winners], None  # 引き分けの場合、プレイヤー名リストを返す

def showdown(com_card, player_hand,num_people):
    """判定から勝敗までの流れを実行する関数、勝敗を返す"""
    player_roles = []
    for i in range(num_people):
        sort = sort_cards(com_card, player_hand[i])
        role = [["P"+str(i+1), role_judge(sort[0], sort[1], sort[2])]]
        player_roles.extend(role)

    result = role_compare(player_roles)

    #### 動作確認 ##############
    print("結果：", result)
    ###########################
    return result

class Game(Card):
    def __init__(self):
        super().__init__()
        self.p_max=2
        self.p_now=2
        self.turn=1
        self.players=[Player(0,0,0)]#Player0はDealer 引き分けのときの掛け金を保持
        self.continue_flag=True

    def Player_waiting(self):#起動～開始直前
        #プレイヤーが２人来るまで待つ。
        for p in range(1,self.p_max+1):
            client,address = tcp_server.accept()
            player=Player(client=client,address=address,player_num=p)
            self.players.append(player)
            #send(player.client,"connect_info:connect")#リスト番号がそれぞれPlayer番号を振る。
            log.add_log("Player"+str(p)+" joined(IP:"+"{}".format(address)+")")
        log.add_log("All players are seated.")

    def Start_game(self):#ゲーム開始～1ターン目終了
        #まずDealerが3枚引く
        for i in range(3):
            self.draw_card(self.com_card)
        #プレイヤーが2枚引く
        for i in range(1,self.p_max+1):#プレイヤー数
            for n in range(2):
                self.draw_card(self.players[i].hand)
            message=card_str(self.com_card,self.players[i].hand)
            message=dict_str(message,"player_num",i)
            print(message)
            send(self.players[i].client,message=message)

        #プレイヤー1の行動はは特に何も待たずに受け取る
        rcv_lst = receive(self.players[1].client)
        self.players[1].bet    = rcv_lst['bet']
        self.players[1].stack -= rcv_lst['bet']
        #==
        #ここでrcv_lstを使用して掛け金の操作*画面を反映
        #==
        for i in range(2,4):
            rcv_lst = receive(self.players[i].client)
            #また画面に反映
            
    def Mid_game1(self):#2ターン目
        self.draw_card(self.com_card)

    def Mid_game2(self):#勝者が決まるまで
        self.draw_card(self.com_card)
        players_hand = [self.players[i].hand for i in range(self.p_now)] # プレイヤーの手札だけをリストに
        showdown(self.com_card, players_hand,self.p_now)

    def End_game(self):#終了後ゲームを持ち金(stack)一回最初からやるかを判定
        for i in range(1,self.p_max+1):
            if self.players[i].stack==0:
                self.continue_flag=False
                log.add_log("Player"+i+"'s stack is 0.")
                break
        #この後にself.continue_flagを確認して続けるかの分岐をする
#===========ゲーム開始===============
def main():
    while True:
        game=Game()
        
        game.Player_waiting()
        game.Start_game()
        if game.p_now!=1:
            game.Mid_game1()
        if game.p_now!=1:
            game.Mid_game2()
        game.End_game()
        if not game.continue_flag:
            log.add_log("finish game")
            break
        #----------------------
        break
        # 8.接続を終了させる
        #client.close()
        #---------------------------

#===========実行=================
main()