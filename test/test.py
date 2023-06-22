import cv2
import mediapipe as mp
from playsound import playsound

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    
    def positionFinder(self,image, handNo=0, draw=False):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
            if draw:
                cv2.circle(image,(lmlist[8][1],lmlist[8][2]), 15 , (255,0,255), cv2.FILLED)
                # cv2.circle(image,(lmlist[20][1],lmlist[20][2]), 15 , (255,0,255), cv2.FILLED)

        return lmlist


def main():
    cap = cv2.VideoCapture(0)
    tracker = handTracker()
    x=500
    y=375
    while True:
        success,image = cap.read()
        image = cv2.resize(image, (1000, 750))

        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)
        # if len(lmList) != 0:
        #     print(lmList[4])
        if len(lmList) != 0:
            dif12 = abs(((lmList[4][1] - lmList[8][1])**2 + (lmList[4][2] - lmList[8][2]))**0.5)
            dif23 = abs(((lmList[12][1] - lmList[8][1])**2 + (lmList[12][2] - lmList[8][2]))**0.5)
            ind_f = abs(((lmList[8][1] - lmList[5][1])**2 + (lmList[5][2] - lmList[8][2]))**0.5)
            print(dif23)

            if dif12 < 20 and dif23 > 80:
                cv2.putText(image,
            text='ok',
            org=(100, 300),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            
            fontScale=1.0,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)
                
            elif dif12 > 43 and ind_f < 20 and dif23 < 40:
                cv2.putText(image,
            text='hai',
            org=(100, 300),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.0,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)
                

            elif dif12 < 30 and ind_f < 20 and dif23 < 40:
                cv2.putText(image,
            text='baibai',
            org=(100, 300),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.0,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)
            
            



        cv2.imshow("Video",image)
        key = cv2.waitKey(1)
        if key == 27:
            break
if __name__ == "__main__":
    main()