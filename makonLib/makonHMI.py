from aboutViewer import *
import aboutme_rc
from PyQt5 import QtWidgets, uic
import sys
import serial
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QMenu,QInputDialog, QLineEdit, QFileDialog,QWidget,QMessageBox,QApplication,QAbstractItemView
import makon_rc
class Makon(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
         super(Makon, self).__init__(*args, **kwargs)
         #Load the UI Page
         uic.loadUi('makonHMI.ui', self)
         self.valveID='S1'
         self.val=0
         self.ramp=0
         self.state=0
         self.ser=0;
         self.index=0;
         self.container=[0,0,0,0,0]
         
         

         #my codes starts here
         self.closeBtn.clicked.connect(self.close)
         self.S1.toggled.connect(self.valvePicker)
         self.S2.toggled.connect(self.valvePicker)
         self.S3.toggled.connect(self.valvePicker)
         self.S4.toggled.connect(self.valvePicker)
         self.S5.toggled.connect(self.valvePicker)
         self.dst.toggled.connect(self.valvePicker)
         self.dial.valueChanged.connect(self.getDialValue)
         self.ren.toggled.connect(self.rampToggle)
         self.rdis.toggled.connect(self.rampToggle)
         self.sendBtn.clicked.connect(self.sendData)
         self.fo.clicked.connect(self.changeState)
         self.fc.clicked.connect(self.changeState)
         self.connect.clicked.connect(self.connectArduino)
         self.help.clicked.connect(self.aboutDeveloper)
         self.sendBtn.setStyleSheet("QPushButton::hover"
                                    "{"
                                    "background-color: rgb(255, 0, 127);"
                                    "}")

    def aboutDeveloper(self):
        self.info=abt()
        self.info.show()
    def connectArduino(self):
        com=self.comtxt.text();
        baud=self.baudtxt.currentText()
        if len(com)>0:
            self.ser = serial.Serial(com, baud,timeout=1)
            if self.ser.isOpen():
                self.ser.close()
                state="closed" if not self.ser.isOpen() else "open"
                print("Closing serial port.... : "+state)
                self.ser.open()
                state="closed" if not self.ser.isOpen() else "open"
                print("now openning... : "+state)
                print("connected to: " + self.ser.portstr)
                self.constatus.setText("Connected to "+self.ser.portstr);
            else:
                self.ser.open()
                self.constatus.setText("Connected to "+self.ser.portstr);

                
    def changeState(self):
        sender=self.sender().objectName()
        if sender=="fo":
            self.state=1
            self.sender().setText(str(self.state))
            self.sender().setStyleSheet("background-color:green;border-radius:10px;")
            self.fc.setStyleSheet("border-radius:10px;background-color: rgb(139, 205, 241);")
        else:
            self.state=0
            self.sender().setStyleSheet("background-color:red;border-radius:10px;")
            self.fo.setStyleSheet("border-radius:10px;background-color: rgb(139, 205, 241);")

                            
    def sendData(self):
        try:
            if self.valveID=="dst":
                data="D"+str(self.state)
                self.ser.write(data.encode())
            else:
                data=str(self.valveID)+"V"+str(self.val)+"R"+str(self.ramp)
                self.container[self.index]=self.val;
                self.ser.write(data.encode())
        except Exception as e:
            self.constatus.setText("Connection Failed! Configure COMPORT fist");
            
    def rampToggle(self,s):
        sender=self.sender().objectName()
        if(sender=='ren' and s==1):
            self.ramp=1
        elif(sender=='rdis' and s==1):
            self.ramp=0
            
    def getDialValue(self,v):
        self.val=v
        
    def valvePicker(self,s):
        if s:
            self.valveID=self.sender().objectName()
            
            if self.valveID=='dst':
                self.dialFrame.setEnabled(False);
                self.ren.setEnabled(False);
                self.rdis.setEnabled(False);
            else:
                self.index=int(self.valveID[1:])-1
                self.dialFrame.setEnabled(True);
                self.dial.setValue(self.container[self.index]);
                self.ren.setEnabled(True);
                self.rdis.setEnabled(True);

            

    





         
def main():
       app = QApplication(sys.argv)
       main = Makon()
       main.show()
       sys.exit(app.exec_())
if __name__ == '__main__':
    main()
