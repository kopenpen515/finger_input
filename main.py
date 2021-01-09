# -*- coding: utf-8 -*-

from hand_tracking import Hand_Tracking
from finger_tracking import *
from write_finger_character import Write_Finger_Character
from gesture_recognition import Gesture_Recognition
import copy

ht = Hand_Tracking()
wfc = Write_Finger_Character()
gs = Gesture_Recognition()

cap = cv2.VideoCapture(0)
while cap.isOpened():
    _, image = cap.read()

    
    #手の位置姿勢推定
    hand_pose_list, hand_img = ht.get_hand_pose_list(image)
    
    #手が検出されている場合に処理を行う
    if hand_pose_list != None:
        #人差し指の位置を取得
        index_finger_position = get_index_finger_position(hand_pose_list)
        
        #image = copy.deepcopy(index_finger_img)
        #入力状態の取得
        input_state = gs.is_input_mode(index_finger_position, hand_pose_list) 
        image, char_img = wfc.get_images(index_finger_position, hand_img, input_state)
        
        #AirTap判定
        if gs.is_airtap(hand_pose_list) == True:
            wfc.clear_all()
        
        
        cv2.imshow('Character', char_img)
        
        
    #検出されなかった場合
    else :
        #左右反転
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        #RGB2BGR変換
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break


cap.release()