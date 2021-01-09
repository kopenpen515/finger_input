import cv2
import numpy as np


#hand_pose_listは、検出した各関節の位置が格納されたlandmarksのリスト
#hand_pose_listの中から、人差し指の位置を取得
def get_index_finger_position(hand_pose_list):
    return hand_pose_list[0].landmark[8]

#position：landmarkで、x座標を取り出すときはposition.x()で取り出す
#hand_img:指先を描画する画像
def get_draw_finger_img(position, hand_img):
    # 画像の大きさを取得
    height, width, channels = hand_img.shape[:3]
    x = int(position.x * width)
    y = int(position.y * height)
    cv2.circle(hand_img, (x, y) , 10, (255,0,0), thickness = -1)
    return hand_img
            
            
        
    
