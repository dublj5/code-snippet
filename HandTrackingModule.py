#reading screenshot of top monitor
#import mss
import cv2
import time
import math
import mediapipe as mp
#import numpy as np

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionConfidence=1, trackingConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackingConfidence = trackingConfidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionConfidence, self.trackingConfidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIDs = [4,8,12,16,20,24,28,32,36,40]

    def findHands(self, img, mask, draw=True):
        HandsMask = mask
        RGBFrame = cv2.cvtColor(HandsMask, cv2.COLOR_BGR2RGB)    
        self.HandResult = self.hands.process(RGBFrame)
        counter = 0
        if self.HandResult.multi_hand_landmarks:        #Hand is found
            for handLandmarks in self.HandResult.multi_hand_landmarks:    #Loop for landmarks
                counter = counter + 1
                if draw:
                    self.mpDraw.draw_landmarks(HandsMask, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return img, counter

    def findPosition(self, img, newBox, radialX, radialY, maxRadX, maxRadY, handNumber=0, draw=True):
        self.lmList = []
        xList = []
        yList = []
        bbox = []
        if self.HandResult.multi_hand_landmarks:        #Hand is found
            for i in range(handNumber):
                myHand = self.HandResult.multi_hand_landmarks[i]
                for ID, LM in enumerate(myHand.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(LM.x * w), int(LM.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    self.lmList.append([ID, cx, cy])                
                    if draw:
                        cv2.circle(img, (cx,cy), 4, (255,0,255), cv2.FILLED)
    
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax
            
                if draw:
                    if newBox == True:
                        if radialX == 250 and radialY == 250:
                            radialX, radialY, maxRadX, maxRadY = xmin, ymin, xmax, ymax
                        cv2.rectangle(img, (radialX - 30, radialY - 30), (maxRadX + 30, maxRadY + 30), (255,255,0), 2)
                    else:
                        cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0,255,0), 2)
                        radialX, radialY = 250,250
                
                
        return self.lmList, bbox, newBox, radialX, radialY, maxRadX, maxRadY

    def findPositionTNL(self, img, newBox, radialX, radialY, maxRadX, maxRadY, handNumber=0, draw=True):
        self.lmList = []
        xList = []
        yList = []
        bbox = []
        if self.HandResult.multi_hand_landmarks:        #Hand is found
            for i in range(handNumber):
                myHand = self.HandResult.multi_hand_landmarks[i]
                for ID, LM in enumerate(myHand.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(LM.x * w), int(LM.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    self.lmList.append([ID, cx, cy])                
                    if draw:
                        cv2.circle(img, (cx,cy), 4, (255,0,255), cv2.FILLED)
    
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax
            
                if draw:
                    if newBox == True:
                        if radialX == 250 and radialY == 250:
                            radialX, radialY, maxRadX, maxRadY = xmin, ymin, xmax, ymax
                        cv2.rectangle(img, (radialX - 30, radialY - 30), (maxRadX + 30, maxRadY + 30), (255,255,0), 2)
                    else:
                        cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0,255,0), 2)
                        radialX, radialY = 250,250
                
                
        return self.lmList, bbox, newBox, radialX, radialY, maxRadX, maxRadY

    def fingerChecks(self, fingersList,want1,want2,want3,want4,want5):  #I want to list out the finger combination I want and return a bool
        wantsList = [want1, want2, want3, want4, want5]
        correctSignal = True
        for checks in range(0,5):
            if fingersList[checks] != wantsList[checks]:
                correctSignal = False
                break;
        return correctSignal

#######################################################################

    def fingersUp(self):
        #landmarks for 4, 8, 12, 16, 20 are fingertips, need to check if the tips are below their value - 2?
        fingers = []
        handSide = 0
        if self.lmList[1][1] > self.lmList[0][1]:                          #the left hand is raised     
            handSide = 6
            if self.lmList[self.tipIDs[0]][1] >= self.lmList[self.tipIDs[0]-1][1]:    #if the tip is X outward of the joint 1 iteration back, thumb is out
                fingers.append(1)
            else:
                fingers.append(0)
            
            for id in range(1,5):
                if self.lmList[self.tipIDs[id]][2] < self.lmList[self.tipIDs[id]-2][2]:    #if the tips are Y above the joint 2 iterations back, finger is up
                    fingers.append(1)
                else:
                    fingers.append(0)

        else:                                                   #the right hand is raised
            handSide = 0
            if self.lmList[self.tipIDs[0]][1] <= self.lmList[self.tipIDs[0]-1][1]:    #if the tip is X outward of the joint 1 iteration back, thumb is out
                fingers.append(1)
            else:
                fingers.append(0)
            
            for id in range(1,5):
                if self.lmList[self.tipIDs[id]][2] < self.lmList[self.tipIDs[id]-2][2]:    #if the tips are Y above the joint 2 iterations back, finger is up
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers, handSide

    def fingersUpTNL(self,numberOfHands):
        rightHandArray = []
        leftHandArray = []
        bothHandsArray = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        LRGauge = 0
        #print(self.lmList)

        if self.lmList[0][1] < 360:                          #the right hand is raised?
            LRGauge = 4
            if self.lmList[self.tipIDs[0]][1] >= self.lmList[self.tipIDs[0]-1][1]:    #if the tip is X outward of the joint 1 iteration back, thumb is out
                bothHandsArray[5] = 1
            else:
                bothHandsArray[5] = 0

            for id in range(1,5):
                if self.lmList[self.tipIDs[id]][2] < self.lmList[self.tipIDs[id]-2][2]:    #if the tips are Y above the joint 2 iterations back, finger is up
                    bothHandsArray[id+5] = 1
                else:
                    bothHandsArray[id+5] = 0

        elif self.lmList[0][1] > 360:                                                   #the left hand is raised?
            LRGauge = 5
            if self.lmList[self.tipIDs[0]][1] <= self.lmList[self.tipIDs[0]-1][1]:    #if the tip is X outward of the joint 1 iteration back, thumb is out
                bothHandsArray[0] = 1
            else:
                bothHandsArray[0] = 0

            for id in range(1,5):
                if self.lmList[self.tipIDs[id]][2] < self.lmList[self.tipIDs[id]-2][2]:    #if the tips are Y above the joint 2 iterations back, finger is up
                    bothHandsArray[id] = 1
                else:
                    bothHandsArray[id] = 0

#[4,8,12,16,20,25,29,33,37,41]

        if len(self.lmList) > 21:
            if self.lmList[self.tipIDs[5]][1] >= self.lmList[self.tipIDs[5]-1][1]:    #if the tip is X outward of the joint 1 iteration back, thumb is out
                bothHandsArray[LRGauge] = 1
            else:
                bothHandsArray[LRGauge] = 0

            for id in range(1,5):
                if self.lmList[self.tipIDs[LRGauge+id]][2] < self.lmList[self.tipIDs[LRGauge+id]-2][2]:    #if the tips are Y above the joint 2 iterations back, finger is up
                    bothHandsArray[LRGauge+id] = 1
                else:
                    bothHandsArray[LRGauge+id] = 0
                    #print("right down")

        return rightHandArray, leftHandArray, bothHandsArray

############################################################################################

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2,y2), (255,0,255), t)
            cv2.circle(img, (x1,y1),r,(255,0,255),cv2.FILLED)
            cv2.circle(img, (x2,y2),r,(255,0,255),cv2.FILLED)
            cv2.circle(img, (cx,cy),r,(0,0,255),cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

    
    #my more-templated findDistance that doesn't need an lmList
    def findDistanceShift(self, p1, p2, img, draw=True, r=10, t=3):
        x1, y1 = p1[0],p1[1]
        x2, y2 = p2[0],p2[1]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2,y2), (255,0,255), t)
            cv2.circle(img, (x1,y1),r,(255,0,255),cv2.FILLED)
            cv2.circle(img, (x2,y2),r,(255,0,255),cv2.FILLED)
            cv2.circle(img, (cx,cy),r,(0,0,255),cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

    def AngleBetween(self, centerX, centerY, middleX, middleY):
        changeInX = middleX - centerX
        changeInY = middleY - centerY     
        #print(math.degrees(math.atan2(changeInY, changeInX)))
        return math.degrees(math.atan2(changeInY, changeInX))
        

def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    pTime = 0
    cTime = 0
    detector = handDetector()
    
    while True:
        ret, frame = cap.read()
        frame = cv2.rotate(frame, 0)
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)

        #if len(lmList) != 0:
        #    print(lmList[0])
    
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (500,500), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    
        # Naming a window 
        cv2.namedWindow("default cam", cv2.WINDOW_NORMAL) 
      
        # Using resizeWindow() 
        cv2.resizeWindow("default cam", 360, 640)
        #cv2.imshow('RGB cam', RGBframe)
        cv2.imshow('default cam', frame)
            
        if cv2.waitKey (1) == 13: #13 is Enter Key
            print("Is this thing on?")
            break
    #Release camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

