#!/usr/bin/env python
# coding: utf-8

# In[1]:


#reading screenshot of top monitor
#import mss
import cv2
import time

import os
import math
#import numpy as np

import pydirectinput as PDI
#import pydirectinput-rgx
import mediapipe as mp
import HandTrackingModule as htm
import vgamepad as vg

SCAN_MIN = 0.75
SCAN_MAX = 1
LEFT_HAND = 0
RIGHT_HAND = 6
PDI.PAUSE = 0
#controller setup
XGamepad = vg.VX360Gamepad()
#XGamepad = vg.VDS4Gamepad()

#camera settings
#wCam, hCam = 640, 480
wCam, hCam = 1280, 720
frameReduction = 100
smoothening = 5
LEFT = 6
RIGHT = 0
handSide = 0
shouldDraw = True
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)

#variables
mphands = mp.solutions.hands
Hands = mphands.Hands(max_num_hands = 2, min_detection_confidence = 0.7, min_tracking_confidence = 0.6)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
readTime = 0         #to prevent false reads when first entering the bounding box, this breaks out if it's too early
scanTimer = 0.0
detector = htm.handDetector()
tipIDs = [4, 8, 12, 16, 20]
previousX, previousY = 0,0
centerX,centerY = -2.0,-2.0
radialX, radialY,maxRadX, maxRadY = 250,250,0,0
newBox = False
#currentX, currentY = 0,0

#image comparison list
#folderPath = "images/HandTemplates"
#myList = os.listdir(folderPath)
#overlayList = []
#for imgPath in myList:
#    image = cv2.imread(f'{folderPath}/{imgPath}')
#    overlayList.append(image)

def resetAllVariables():
    centerX, centerY = -2.0,-2.0
    #XGamepad.right_joystick_float(x_value_float = 0.0, y_value_float = 0.0)
    #XGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    #XGamepad.update()

def handPatternValidation(frame, fingers, lmList, handSide):
    if readTime < 1:        
        return
    global wCam, hCam, frameReduction, centerX, centerY, newBox
    global previousX, previousY, scanTimer, shouldDraw
    currentX, currentY, finalDirection = 0, 0, 0
    wristX, wristY = lmList[0][1:]
    indexX, indexY = lmList[8][1:]
    middleX, middleY = lmList[12][1:]
    pinkyX, pinkyY = lmList[20][1:]

    #if fingers[1] == 1 and fingers[2] == 1:
    #8. Find distance between fingers
        #length, frame, _ = detector.findDistanceShift((x1,y1),(x2,y2),frame)
       # if length < 40:
            #cv2.circle(frame, (x1,y1), 15, (0,255,0), cv2.FILLED)
       #9: click if distance is short

    if handSide == RIGHT_HAND:
        if fingers.count(1) == 0:                          #closed fist
            newBox = True
            PDI.keyDown('q')
            #XGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            if centerX == -2.0 and centerY == -2.0:    #center should be where the middle finger is when fist starts
                centerX, centerY = wristX, wristY
            length, frame, _ = detector.findDistanceShift((wristX,wristY), (centerX,centerY),frame, draw=shouldDraw)    #draws the line between middle tip and origin
            testDist = [wristX - centerX, wristY - centerY]
            testNorm = math.sqrt(testDist[0] ** 2 + testDist[1] ** 2)
            menuAngle = detector.AngleBetween(centerX, centerY, wristX, wristY)
            #print(menuAngle) #this prints 0,0 as to the right, this MIGHT be because my webcam is flipped on its side so

            radialMouseX, radialMouseY = PDI.position()
            #starting from the right of radial, going clockwise
            if menuAngle > -13 and menuAngle <= 13:
                if radialMouseX != 641 and radialMouseY != 496:
                    PDI.moveTo(641,496)
            elif menuAngle > 13 and menuAngle <= 40:
                if radialMouseX != 657 and radialMouseY != 655:
                    PDI.moveTo(657,655)
            elif menuAngle > 40 and menuAngle <= 67:
                if radialMouseX != 748 and radialMouseY != 788:
                    PDI.moveTo(748,788)
                    
            elif menuAngle > 67 and menuAngle <= 90:
                if radialMouseX != 881 and radialMouseY != 849:
                    PDI.moveTo(881,849)                    
            elif menuAngle > 90 and menuAngle <= 113:
                if radialMouseX != 1060 and radialMouseY != 850:
                    PDI.moveTo(1060,850)
                    
            elif menuAngle > 113 and menuAngle <= 140:
                if radialMouseX != 1175 and radialMouseY != 775:
                    PDI.moveTo(1175,775)            
            elif menuAngle > 140 and menuAngle <= 167:
                if radialMouseX != 1267 and radialMouseY != 655:
                    PDI.moveTo(1267,655)
                    
           #far left of screen, this is where 180 degrees is and it flips to =/- 179 degrees         
            elif (menuAngle > 167 and menuAngle <= 180) or (menuAngle > -179.9 and menuAngle <= -167):
                if radialMouseX != 1294 and radialMouseY != 497:
                    PDI.moveTo(1294,497)
                    
            elif menuAngle > -167 and menuAngle <= -133:
                if radialMouseX != 1235 and radialMouseY != 350:
                    PDI.moveTo(1235,350)
            elif menuAngle > -133 and menuAngle <= -103:
                if radialMouseX != 1110 and radialMouseY != 250:
                    PDI.moveTo(1110,258)
            elif menuAngle > -103 and menuAngle <= -73:
                if radialMouseX != 960 and radialMouseY != 225:
                    PDI.moveTo(960,225)
            elif menuAngle > -73 and menuAngle <= -43:
                if radialMouseX != 808 and radialMouseY != 249:
                    PDI.moveTo(808,257)
            elif menuAngle > -43 and menuAngle <= -13:
                if radialMouseX != 690 and radialMouseY != 349:
                    PDI.moveTo(690,349)
            
            #if testNorm > 0.0:
                #finalDirection = [testDist[0]/testNorm, testDist[1]/testNorm]
                #XGamepad.right_joystick_float(x_value_float = finalDirection[0], y_value_float = finalDirection[1] * -1)  #move joystick
            cv2.circle(frame, (centerX,centerY), 7, (255,0,255), cv2.FILLED)    
            
        elif detector.fingerChecks(fingers, 0,1,0,0,1): #index and pinky
            #distance between fingers
            length, frame, _ = detector.findDistanceShift((indexX,indexY),(pinkyX,pinkyY),frame, draw=shouldDraw)
            if length < 30:
                PDI.keyDown('esc')
                scanTimer = 0
            elif length >= 30:
                PDI.keyUp('esc')
        elif detector.fingerChecks(fingers,0,0,0,0,1):      #pinky 3
            if scanTimer > SCAN_MIN and scanTimer < SCAN_MAX:
                PDI.keyDown('s')
            elif scanTimer > 1.25:
                PDI.keyUp('s')
                scanTimer = 0
        elif detector.fingerChecks(fingers,1,1,0,0,0):      #index and thumb
            if scanTimer > SCAN_MIN and scanTimer < SCAN_MAX:
                PDI.keyDown('u')
            #elif scanTimer > 1.25:
                #PDI.keyUp('u')
                #scanTimer = 0

        else:
            #XGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            #XGamepad.right_joystick_float(x_value_float = 0.0, y_value_float = 0.0)
            PDI.keyUp('q')
            PDI.keyUp('s')
            PDI.keyUp('u')
            scanTimer = 0
            PDI.click()
            centerX, centerY = -2.0,-2.0
            newBox = False
    elif handSide == LEFT_HAND:
        newBox = False
        if detector.fingerChecks(fingers,0,1,0,0,0):      #index 1
            if scanTimer > SCAN_MIN and scanTimer < SCAN_MAX:
                PDI.keyDown('t')
            elif scanTimer > 1.25:
                PDI.keyUp('t')
                scanTimer = 0
        elif detector.fingerChecks(fingers,0,1,1,0,0):      #index+middle 2
            if scanTimer > SCAN_MIN and scanTimer < SCAN_MAX:
                PDI.keyDown('g')
            elif scanTimer > 1.25:
                PDI.keyUp('g')
                scanTimer = 0
        elif detector.fingerChecks(fingers,0,0,0,0,1):      #pinky 3
            if scanTimer > SCAN_MIN and scanTimer < SCAN_MAX:
                PDI.keyDown('f')
            elif scanTimer > 1.25:
                PDI.keyUp('f')
                scanTimer = 0
        elif detector.fingerChecks(fingers,1,0,0,0,0):      #only thumb 4
            if scanTimer > SCAN_MIN and scanTimer < SCAN_MAX:
                PDI.keyDown('h')
            elif scanTimer > 1.25:
                PDI.keyUp('h')
                scanTimer = 0
        elif detector.fingerChecks(fingers,1,0,0,1,0):      #thumb and ring finger out
            if scanTimer > SCAN_MIN:
                shouldDraw = not shouldDraw
                scanTimer = 0
        elif detector.fingerChecks(fingers,1,1,0,0,1):      #thumb, index, and ring finger out
            if scanTimer > SCAN_MIN and scanTimer < SCAN_MAX:
                PDI.keyDown('enter')
            elif scanTimer > 1.25:
                PDI.keyUp('enter')
                scanTimer = 0
        #elif fingers[0] == 0:
        #    PDI.keyDown('alt')
        #    if detector.fingerChecks(fingers,0,1,1,0,1):   #|.||.
        #        if scanTimer >= 0.5:
        #            PDI.press('tab')
        #            scanTimer = 0
        else:
            PDI.keyUp('alt')
            PDI.keyUp('t')
            PDI.keyUp('f')
            PDI.keyUp('g')
            PDI.keyUp('h')
        
    #XGamepad.update()

#################################################################################################################################

while True:
    ret, frame = cap.read()
    frame = cv2.rotate(frame, 0)
    image_frame = frame
    cTime = time.time()

    #if scanTimer >= 3:
        #print("reset Timer")
        #activateCondition = True
        #scanTimer = 0

    #if activateCondition == True:
        #print("activate ready, set false")
        #acivateCondition = False
    
    #cv2.rectangle(frame, (0, 0), (100, 100), 255, 3)
    #1. Find hand landmarks
    ######## get the rectangle and send it to findHands and findPosition instead of the entire image
    upper_left = (0, 1)
    bottom_right = (upper_left[0]+250, upper_left[1]+350) #550, 600
    #Center Rectangle marker
    #TLRect = cv2.rectangle(image_frame, (0,0), (170,170), (0, 0, 200), 5)
    #TRRect = cv2.rectangle(image_frame, (550,0), (720,170), (200, 0, 0), 5)
    center_rect_img = image_frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]
    #TL_rect_img = image_frame[170 : 0, 170 : 0]
    #TR_rect_img = image_frame[0 : 170, 550 : 720]
    frame, numHands = detector.findHands(frame,center_rect_img,draw=shouldDraw)
    #frame = detector.findHands(frame,TL_rect_img)
    #frame = detector.findHands(frame,TR_rect_img)

    #Create list of landmarks detected
    lmList, bbox, newBox, radialX, radialY, maxRadX, maxRadY = detector.findPosition(center_rect_img, newBox, radialX, radialY, maxRadX, maxRadY, numHands, draw=shouldDraw)

    #landmarks for 4, 8, 12, 16, 20 are fingertips, need to check if the tips are below their value - 2?
    #2. get tip of index and middle fingers
    if len(lmList) != 0:
        if pTime != 0:
            readTime = readTime + (cTime - pTime)
        #3. Check which fingers are up
        fingers,handSide = detector.fingersUp()
        handPatternValidation(frame, fingers, lmList, handSide)
    else:
        readTime = 0
        #7. If index and middle fingers are up, click
        #if fingers[1] == 1 and fingers[2] == 1:
            #8. Find distance between fingers
            #length, frame, _ = detector.findDistance(8,12,frame)
            #if length < 40:
                #cv2.circle(frame, (x1,y1), 15, (0,255,0), cv2.FILLED)
                #9: click if distance is short
                #PDI.click()        

    #this shows the images it's seeing, the fingers up are what are expected, removing for now
        #totalFingers = fingers.count(1)    #count how many "1"'s there are
        #h, w, c = overlayList[totalFingers-1].shape
        #frame[0:h, 0:w] = overlayList[totalFingers-1]     
    
    #cv2.rectangle(frame, (20,225), (170, 425), (0,255,0), cv2.FILLED)
    #cv2.putText(frame, str(totalFingers), (45,375), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 25)    
    #RGBFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Naming a window 
    #cv2.namedWindow("default cam", cv2.WINDOW_NORMAL)  
    # Using resizeWindow() 
    #cv2.resizeWindow("default cam", 360, 640)

    #10. FPS and Display

    if pTime != 0:
        scanTimer = scanTimer + (cTime-pTime)
        
    fps = 1/(cTime-pTime)

    pTime = cTime
    if shouldDraw:
        centerRect = cv2.rectangle(image_frame, upper_left, bottom_right, (100, 50, 200), 5)
        cv2.putText(frame, f'FPS: {int(fps)}', (0,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3)
    cv2.imshow('default cam', frame)
        
    if cv2.waitKey (1) == 13: #13 is Enter Key
        print("Is this thing on?")
        break

#Release camera and close all windows
cap.release()
cv2.destroyAllWindows()

