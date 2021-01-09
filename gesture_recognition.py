# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Gesture_Recognition():
    
    input_depth = -0.25
    old_input_state = False
    distance_threshold = 0.5
    
    ##-----AirTapに関する設定-----##
    airtap_len= 30
    airtap_z_threshold = 5.0
    airtap_distance_threshold = 0.25
    airtap_near_threshold = 0.1
    ##!!-----AirTapに関する設定-----!!##
    
    def __init__(self):
        #人差し指の時系列データ
        self.index_finger_list = []
        #親指の時系列データ
        self.thumb_list = []
        #AirTap認識のための、人差し指・親指の距離変位の遷移
        self.distance_list = []
            
    
    #入力もードの判定
    def is_input_mode2(self, position):
        flag = False
        #閾値より手前に指が存在すれば入力モード
        if position.z < self.input_depth:
            flag = True
        print("入力モード" + str(flag))
        print(position.z)
        return flag
    
    #文字入力モードか判定
    def is_input_mode(self, position, hand_pose_list):
        flag = False
        
        finger_list = []
        #中指
        finger = hand_pose_list[0].landmark[12]
        finger_list.append([finger.x, finger.y])
        #薬指
        finger = hand_pose_list[0].landmark[16]
        finger_list.append([finger.x, finger.y])
        #小指
        finger = hand_pose_list[0].landmark[20]
        finger_list.append([finger.x, finger.y])

        s = 0.0
        #人差し指と中指、薬指、小指の距離の総和を算出
        for finger in finger_list:
            s += abs(finger[1] - position.y)
        
      #  print(s)
        #人差し指と各指のy座標がある程度離れていると入力モード
        if s > self.distance_threshold:
            flag = True
        #print("入力モード" + str(flag))
        #print(position.z)
        return flag
    
    #距離計算
    def get_distance(self, point1, point2):
        temp = (point1[0] - point2[0]) ** 2  + (point1[1] - point2[1]) ** 2
        return temp ** (0.5)
    
    #AirTap判定評価
    def airtap_evaluation(self):
        flag = False

        #格納されているリストの数が一定数なかったら処理しない
        if len(self.index_finger_list) < self.airtap_len:
            return flag

        distance_sum = 0.0
        z_sum = 0.0
        #評価1　人差し指と親指の総和が閾値以上
        #評価2 2つの指のz方向の距離の変化の総和が閾値以内
        for i, (index_finger, thumb) in enumerate(zip(self.index_finger_list, self.thumb_list)):
            #評価1
           # distance_sum += self.get_distance(index_finger, thumb)
            self.distance_list.append(self.get_distance(index_finger, thumb))
            #評価2
            if i > 0:
                z_sum += abs(self.index_finger_list[i][2] - self.index_finger_list[i-1][2])
                z_sum += abs(self.thumb_list[i][2] - self.thumb_list[i-1][2])            
        
        #評価1の再算出
        for i in range(len(self.distance_list)-1):
           # print("距離遷移："+str(abs(self.distance_list[i+1] - self.distance_list[i])))
            distance_sum += abs(self.distance_list[i+1] - self.distance_list[i])
        
        print("距離 : " + str(distance_sum))
        print("z : " + str(z_sum))
        #評価1
        if distance_sum > self.airtap_distance_threshold:
            #評価2
            if z_sum < self.airtap_z_threshold:
                #評価3 最初と最後の人差し指と親指の位置の変化が少ない
                index_finger_diff = self.get_distance(self.index_finger_list[0], 
                                                      self.index_finger_list[self.airtap_len-1])
                thumb_diff = self.get_distance(self.thumb_list[0], 
                                                      self.thumb_list[self.airtap_len-1]) 
                print("人差し指の変異:" + str(index_finger_diff))
                print("親指の変異:" + str(thumb_diff))
                if index_finger_diff < self.airtap_near_threshold and thumb_diff < self.airtap_near_threshold:
                    flag = True
                    print("AirTap!!!!!!")
        self.clear_list()
                
        return flag
    
    
    #AirTap判定
    def is_airtap(self, hand_pose_list):
        #人差し指の追加
        index_finger = hand_pose_list[0].landmark[8]
        self.index_finger_list.append([index_finger.x, index_finger.y, index_finger.z])
        #親指の追加
        thumb = hand_pose_list[0].landmark[4]
        #データが溢れたら削除
        if len(self.index_finger_list) > self.airtap_len:
            self.index_finger_list.pop(0)
            self.thumb_list.pop(0)
            
        self.thumb_list.append([thumb.x, thumb.y, thumb.z])
        return self.airtap_evaluation()
        
    
    #AirTapの判定されたら初期化
    def clear_list(self):
        #人差し指の時系列データ
        self.index_finger_list.clear()
        #親指の時系列データ
        self.thumb_list.clear()
        self.distance_list.clear()
        
        