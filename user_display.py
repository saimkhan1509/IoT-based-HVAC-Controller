from PyQt5 import QtCore, QtGui, QtWidgets
import paho.mqtt.client as mqttClient
import time
import random
import math
import sys

def on_connect(client,userdata, flags, rc):
	if rc == 0:
		print("Connect to broker")
		global Connected
		Connected = True
	else:
		print("Connection failed Return Code : ",rc)
		
def on_message(client, userdata, message):
    global ac
    global ventilation
    global heating
    global received_temp
    temp = [int(k) for k in message.payload.split() if k.isdigit()]
    ac = temp[0]
    heating = temp[1]
    ventilation = temp[2]
    received_temp = temp[3]


client_name = "user-display"
broker_address = "127.0.0.1"
broker_port = 1883
user = "admin"
password = "hivemq"

client = mqttClient.Client(client_name)
client.on_connect = on_connect
client.on_message = on_message
client.connect(host = broker_address, port = broker_port)
client.subscribe('location/Controller')

print(client_name)



client.loop_start()
	
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(753, 421)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 30, 211, 20))
        font = QtGui.QFont()
        font.setFamily("UnGraphic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 70, 851, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 160, 67, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 220, 81, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 280, 111, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(210, 160, 111, 17))
        self.label_5.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_5.setLineWidth(1)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(210, 220, 111, 17))
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(210, 280, 111, 17))
        self.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.label_7.setText("")
        self.label_7.setTextFormat(QtCore.Qt.PlainText)
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget,clicked = lambda: self.refresh_values())
        self.pushButton.setGeometry(QtCore.QRect(120, 340, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(30, 100, 141, 17))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(210, 100, 111, 17))
        self.label_9.setFrameShape(QtWidgets.QFrame.Box)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(460, 190, 251, 16))
        self.horizontalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalSlider.setMinimum(15)
        self.horizontalSlider.setMaximum(35)
        self.horizontalSlider.setPageStep(5)
        self.horizontalSlider.setTracking(False)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(self.updateLabel)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget,clicked = lambda: self.onchange())
        self.pushButton_2.setGeometry(QtCore.QRect(540, 330, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(570, 220, 31, 17))
        self.label_10.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(480, 150, 201, 17))
        self.label_11.setFrameShape(QtWidgets.QFrame.Box)
        self.label_11.setObjectName("label_11")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 753, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def updateLabel(self, value):
        self.label_10.setText(str(value))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "HVAAC CONTROLLER"))
        self.label_2.setText(_translate("MainWindow", "Heating"))
        self.label_3.setText(_translate("MainWindow", "Ventilation"))
        self.label_4.setText(_translate("MainWindow", "Air conditioning"))
        self.pushButton.setText(_translate("MainWindow", "Refresh"))
        self.label_8.setText(_translate("MainWindow", "Curr Received Temp"))
        self.pushButton_2.setText(_translate("MainWindow", "Update"))
        self.label_11.setText(_translate("MainWindow", "SET AMBIENT TEMPRATURE"))

    def onchange(self):
        client.publish('location/' + client_name, self.horizontalSlider.value())


    def refresh_values(self):
        self.label_5.setText(str(heating))
        self.label_6.setText(str(ventilation))
        self.label_7.setText(str(ac))
        self.label_9.setText(str(received_temp))


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
