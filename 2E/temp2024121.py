from m5stack import *
from m5ui import *
from uiflow import *
import network
import time
import socket

    def Start_game(self):
        action_num=0
        action_list=0
        bet_flag=True
        Ipt=game.input_get()
        send_list={
            "action":self.action[action_list][action_num],
            "bet":10
        }
        if Ipt=="A":
            if action_num +1>= len(self.action[action_list]):
                action_num=0
            else:
                action_num+=1

            if self.action[action_list][action_num]=="Bet":
                bet_flag=True
            else:
                bet_flag=False

        elif Ipt=="B":
            if bet_flag==True:
                send_list["bet"]+=10                


        elif Ipt=="C":
            #send
            pass
        self.action[action_list][action_num]
        lcd.clear(self.bg_col)
        message=receive(self.tcp_client)
        card_info=message["card"]
        #print(card_info)
        d_card=card_decode(card_info)
        anime.drow_static_elements()
        anime.drow_all_card(d_card)