"""NOTE PLS USE THE FOLLOWING COMMANDS FOR SETTING UP THE REQUIRED MODULES USED IN THIS PROGRAM
1) OPEN CMD -> TYPE {python --version} -> {pip install opencv} after the installation is complete again type {pip install cvzone}, DONT TYPE {} ALONG WITH THE COMMANDS
2) CAMERA APP SHOULDN'T BE OPENED BEFOREHAND RUNNING THIS PROGRAM AS IT MAY CAUSE RUN_TIME_ERROR"""



# Respected Invigilator here I shall explain you the working of the project pary by part
# I have used multiple modules as the project had a varietry of requirements which could only be satisfied via using external libraries and modules
# cv2 is a module which is used for image recgonition in pythn it comes with a variety of readymade tools which makes it hassleless
# for us to create a program utilizing Image recgonition without the use of any neural network or deep learning.
# cvzone is just like cv2 only differnce it that it helps in the processing and translation of data so that python can serve the required
# purpose. Numpy is used for error free mathematical coordination between different numerical vales used in the program like score adn coordinates 
# of the in game figures such as the slider of pong game and the position of ball which varies with time.

# Contols : Move hands to move sliders, press q to quit and r to replay when game is over


import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

#Player_Profile
name = str(input("Enter name : "))
lst = []
lst.append(name)

cap = cv2.VideoCapture(0) # giving access to camera to use live video via webcam
cap.set(3, 1280) # setting pixel ratio of camera window
cap.set(4, 720)

# Importing all images that would be used along in the project
imgBackground = cv2.imread(r"C:\Users\sulph\Desktop\OPENCV\1280x720-gaming-0yhvmfxag0yu5r34-ink.jpeg")
imgGameOver = cv2.imread(r"C:\Users\sulph\Desktop\OPENCV\gameOver.png")
imgBall = cv2.imread(r"C:\Users\sulph\Desktop\OPENCV\Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread(r"C:\Users\sulph\Desktop\OPENCV\bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread(r"C:\Users\sulph\Desktop\OPENCV\bat2.png", cv2.IMREAD_UNCHANGED)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2) # comes with built-in library

# Variables
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw

    # Overlaying the background image
    img = cv2.addWeighted(img, 0, imgBackground, 0.8, 0)

# Main Game Logic Starts Here :

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    # Game Over
    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver
        cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200, 0, 200), 5)
        
        if score[1]+score[0] not in lst :
            lst.append(score[1]+score[0])

    # If game not over move the ball
    else:

        # Move the Ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Drawing the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        

    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread(r"C:\Users\sulph\Desktop\OPENCV\gameOver.png")
    if key==ord('q'):
        break
print(lst)