#from m5stack import *
import _thread
import time
import random
import ujson

class InputObserver:#ボタン入力を監視 (オブサーバ)
    def __init__(self):
        self.ipt = 0
    def ButtonCheck(self):
        while True:#ボタンが押されたときに特定の文字列を返す
            
            
            if btnA.wasPressed():#<
                self.ipt = 1
            elif btnB.wasPressed():#>
                self.ipt = 2
            elif btnC.wasPressed():
                self.ipt = 3
            elif toch.read():
                self.ipt = 4
            else:
                self.ipt = 0

            #self.ipt=random.randint(0, 2)
            time.sleep(self.spf) 
    def GetIpt(self):# user_inputの値を取得し、取得後にリセット
        output = self.ipt
        #print("output:"+str(output))
        self.ipt = 0  # リセット
        #print("output2:"+str(output))
        return output


def 



def main():
    #---基本パラメータ設定-----
    
    Ipt=InputObserver()
    _thread.start_new_thread(Ipt.ButtonCheck,())
    
    #print(n)
    #sliced_map=[]
    for h in range(500):
    #while True:
        p=Ipt.GetIpt()
        
#------------実行------------



