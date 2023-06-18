import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all imagesq

imgBat1 = cv2.imread("Pong1972/Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Pong1972/Resources/bat2.png", cv2.IMREAD_UNCHANGED)
imgGameOver = cv2.imread("Pong1972/Resources/gameOver.png")
imgBackground = []
imgBackground.append(cv2.imread("Pong1972/Resources/Background1.png"))
imgBackground.append(cv2.imread("Pong1972/Resources/Background2.png"))
imgBackground.append(cv2.imread("Pong1972/Resources/Background3.png"))
imgBackground.append(cv2.imread("Pong1972/Resources/Background4.png"))
imgBall = []
imgBall.append(cv2.imread("Pong1972/Resources/Ball1.png", cv2.IMREAD_UNCHANGED))
imgBall.append(cv2.imread("Pong1972/Resources/Ball2.png", cv2.IMREAD_UNCHANGED))
imgBall.append(cv2.imread("Pong1972/Resources/Ball3.png", cv2.IMREAD_UNCHANGED))
imgBall.append(cv2.imread("Pong1972/Resources/Ball4.png", cv2.IMREAD_UNCHANGED))


# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ibg = 0
ib = 2
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw
    # print(img.shape, imgBackground.shape)
    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground[ibg], 0.8, 0)

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

    # If game not over move the ball
    else:

        # Move the Ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        img = cvzone.overlayPNG(img, imgBall[ib], ballPos)

        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    cv2.imshow("Image", img)

    # check for keypessed
    key = cv2.waitKey(1)
    if key == ord('r'):
        ibg = 0
        ib = 2
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Pong1972/Resources/gameOver.png")

    if key == ord('v'):
        ibg = 0
    if key == ord('b'):
        ibg = 1
    if key == ord('n'):
        ibg = 2
    if key == ord('m'):
        ibg = 3
    if key == ord('f'):
        ib = 0
    if key == ord('g'):
        ib = 1
    if key == ord('h'):
        ib = 2
    if key == ord('j'):
        ib = 3
    if key == ord('q'):
        break
    
# Release the video capture and close windows    
cap.release()
cv2.destroyAllWindows()