import cv2
import mediapipe as mp
import numpy as np

class Hand_Tracking():
    
    #文字領域の人差し指の位置の遷移をリストで保持
    finger_position_list = []
    
    ##-----mediapipeの設定-----##
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
    ##!!-----mediapipeの設定-----!!##

    def __init__(self):
        pass
    
    def get_hand_pose_list(self, img):
        hand_pose_list, hand_img = self.hand_tracking(img)
        return hand_pose_list, hand_img 
    
    def hand_tracking(self, img):
        image = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = self.hands.process(image)
          
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
        return results.multi_hand_landmarks, image

        
            
        


