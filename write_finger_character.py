# -*- coding: utf-8 -*-
#https://google.github.io/mediapipe/solutions/hands.html

import cv2
import numpy as np
from finger_tracking import get_draw_finger_img

class Write_Finger_Character():
    img_size = 200
    input_depth = -0.25
    old_input_state = False
    distance_threshold = 0.5

    def __init__(self):
        #一指し指の軌跡
        self.x_list = []
        self.y_list = []
        self.z_list = []
        #画像
        self.char_img = np.zeros((self.img_size, self.img_size))
        self.char_img += 255


    #現在の位置を格納
    def get_images(self, position, hand_img, state):
        if state == True:
            self.x_list.append(position.x)
            self.y_list.append(position.y)
            self.z_list.append(position.z)
            hand_img = get_draw_finger_img(position, hand_img)
            self.draw_char_img()
        #過去の入力モード更新
        self.old_input_state = state
        return hand_img, self.char_img
            
        
        
    #文字描画
    def draw_char_img(self):
        #前の状態を見て、入力モードじゃなかったら新たなストロークとする
        if self.old_input_state == False:
            self.clear_list()
            
        index = len(self.x_list)
        #過去のデータが存在しなければ未実行
        if(index == 0):
            return self.char_img
        
        ##-----座標を求める-----##
        index -= 1
        #一個過去の座標
        old_x = int(self.x_list[index-1]*self.img_size)
        old_y = int(self.y_list[index-1]*self.img_size)
        #今の座標
        new_x = int(self.x_list[index]*self.img_size)
        new_y = int(self.y_list[index]*self.img_size)
        ##!!-----座標を求める-----##
        #線描画
        self.char_img = cv2.line(self.char_img,(old_x, old_y)
                                 ,(new_x, new_y),(0,0,0),2)
        return self.char_img

    
    #初期化（AirTapすると呼ばれる）
    def clear_all(self):
        #一指し指の軌跡
        self.x_list.clear()
        self.y_list.clear()
        self.z_list.clear()
        #画像
        self.char_img = np.zeros((self.img_size, self.img_size))
        self.char_img += 255
        
    #リストのみ初期化
    def clear_list(self):
        #一指し指の軌跡
        self.x_list.clear()
        self.y_list.clear()
        self.z_list.clear()
