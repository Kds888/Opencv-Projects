from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import cv2
import winsound

ui,_=loadUiType(r'D:\opencv\[TutsNode.net] - Build Complete Webcam Security Camera  Python OpenCv & Pyqt\5. Download user interface file\1.1 pyqt-security-cam.ui') # Getting the ui for the project 

class MainApp(QMainWindow,ui):
    volume = 500
    def __init__(self):
        QMainWindow.__init__(self) # initializing the qmain window
        self.setupUi(self) # Passing the ui through the class object
        # Controling the views in the given pyqt UI. they all get connected togther as theuy are a part of Qmain window
        self.MONITORING.clicked.connect(self.start_monitoring)
        self.VOLUME.clicked.connect(self.set_volume)
        self.EXIT.clicked.connect(self.close_window) 
        self.VOLUMESLIDER.setVisible(False)
        self.VOLUMESLIDER.valueChanged.connect(self.set_volume_level)
# making the code such that we can record teh video
    def start_monitoring(self):
        print("Start monitoring button clicked") # basically when we start the recording of the data 
        webcam = cv2.VideoCapture(0) # using the video capture from the opencv
        while True:
            _,im1 = webcam.read()
            _,im2 = webcam.read()
            diff = cv2.absdiff(im1,im2)
            gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            _,thresh = cv2.threshold(blur, 20,255,cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh,None,iterations=3)
            countours,_=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for c in countours:
                if cv2.contourArea(c) <5000:
                    continue
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(im1,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.imwrite('captured.jpg',im1)
                image = QImage('captured.jpg')
                pm = QPixmap.fromImage(image)
                self.CAMWINDOW.setPixmap(pm)
                winsound.Beep(self.volume,100)
            cv2.imshow("Opencv-Security-Camera",im1)
            
            key = cv2.waitKey(10)
            if key == 27:
                break
        webcam.release() 
        cv2.destroyAllWindows()   

    def set_volume(self):
        self.VOLUMESLIDER.setVisible(True)
        print("Set volume button clicked")

    def close_window(self):
        self.close()
# volume function when ever an object is detected 
    def set_volume_level(self):
        self.VOLUMELEVEL.setText(str(self.VOLUMESLIDER.value()//10))
        self.volume = self.VOLUMESLIDER.value() * 10
        cv2.waitKey(1000)
        self.VOLUMESLIDER.setVisible(False)

def main():
    app = QApplication(sys.argv)
    window = MainApp() # where we have all the code saved
    window.show() # basically connected window we get this as displayed
    app.exec_()# to run the application
if __name__ == '__main__':
    main()   # run the main appp 

