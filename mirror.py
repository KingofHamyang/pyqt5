# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets #pip install pyqt5(pip install python3-pyqt5)
from PyQt5.Qt import Qt

from PyQt5.QtCore import Qt ,QUrl, pyqtSlot
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineSettings


from PyQt5.QtWidgets import QApplication,QWidget
from urllib import request
from bs4 import BeautifulSoup
import yapi #pip install yapi [https://github.com/ahmetkotan/yapi]
import feedparser #pip install feedparser [News api] [http://w3devlabs.net/wp/?p=16964]
import datetime 
from time import sleep
import threading
import tkinter as tk #this can't pip install
import requests
import json
import cv2
from PyQt5.QtGui import QPixmap, QImage   
#import pafy #pip install pafy , pip install youtube_dl
from PyQt5.QtWidgets import QGraphicsOpacityEffect
import pygame
import time

#==================================================================================================
#==============UI_MAIN==============================================================================
#==================================================================================================

def time_cal(hour):
    ampm="오후 "
    if hour>=24:
        hour=hour-24

    if hour>=12:
        if hour>=13:
            hour=hour%12
    else:
        ampm="오전 "

    result=ampm+str(hour)+'시'
    
    return result

def weather_icon_cal(weather):
    if weather=="맑음":
        pixmap=QPixmap("sunny.png")
    elif weather=="구름조금":
        pixmap=QPixmap("partlycloudy.png")
    elif weather=="흐림" or "구름많음":
        pixmap=QPixmap("cloudy.png")
    elif weather=="구름많고 비" or "흐리고 비":
        pixmap=QPixmap("rainy.png")
    elif weather=="구름많고 비/눈" or "구름많고 눈/비" or "흐리고 비/눈" or "흐리고 눈/비":
        pixmap=QPixmap("rainsnow.png")
    elif weather=="구름많고 눈" or "흐리고 눈":
        pixmap=QPixmap("snowy.png")   
    return pixmap 

def weekday_cal(weekday):
    if weekday%7==0:
        return "월요일"
    elif weekday%7==1:
        return "화요일"
    elif weekday%7==2:
        return "수요일"
    elif weekday%7==3:
        return "목요일"
    elif weekday%7==4:
        return "금요일"
    elif weekday%7==5:
        return "토요일"
    elif weekday%7==6:
        return "일요일"



class Ui_MainWindow(QWidget):
    '''
    hello_world = 0
    '''

    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    
    News_url_Economy = "https://www.mk.co.kr/rss/30100041/"
    News_url_Politics = "https://www.mk.co.kr/rss/30200030/"
    News_url_Social = "https://www.mk.co.kr/rss/50400012/"
    News_url_Entertain = "https://www.mk.co.kr/rss/30000023/"
    News_url_Sports = "https://www.mk.co.kr/rss/71000001/"

    Weather_url="http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=109"

    start_or_stop=False
    start=True
    '''
    def __init__(self):
        super().__init__()
        self.setupUi(MainWindow)
    '''


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

        MainWindow.setPalette(palette)
        MainWindow.showFullScreen()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.main = QtWidgets.QLabel(self.centralwidget)
        self.main.setGeometry(QtCore.QRect(self.width-1500, self.height-800, 1000,500))
        self.main.setObjectName("main")
        self.main.setFont(QtGui.QFont("Times New Roman",100))
        
        self.weather = QtWidgets.QLabel(self.centralwidget)
        self.weather.setGeometry(QtCore.QRect(self.width-690, self.height-295, 1000,300))
        self.weather.setObjectName("weather")
        
        self.temperature = QtWidgets.QLabel(self.centralwidget)
        self.temperature.setGeometry(QtCore.QRect(self.width-1000, self.height-200, 1500,130))
        self.temperature.setObjectName("temperature")
        self.temperature.setFont(QtGui.QFont("맑은 고딕",20))

        #================================================================================
        self.clock = QtWidgets.QLabel(self.centralwidget)
        self.clock.setGeometry(QtCore.QRect(200,300,100,50))
        self.clock.setObjectName("clock")

        self.ampm = QtWidgets.QLabel(self.centralwidget)
        self.ampm.setGeometry(QtCore.QRect(self.width-1750,self.height-200,800,70))
        self.ampm.setObjectName("ampm")
        self.ampm.setFont(QtGui.QFont("맑은 고딕",50))         

        self.time = QtWidgets.QLabel(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(self.width-1650,self.height-310,800,200))
        self.time.setObjectName("time")
        self.time.setFont(QtGui.QFont("맑은 고딕",150)) 

        self.time2 = QtWidgets.QLabel(self.centralwidget)
        self.time2.setGeometry(QtCore.QRect(self.width-1460,self.height-325,800,200))
        self.time2.setObjectName("time")
        self.time2.setFont(QtGui.QFont("맑은 고딕",150)) 
        
        self.time3 = QtWidgets.QLabel(self.centralwidget)
        self.time3.setGeometry(QtCore.QRect(self.width-1350,self.height-325,800,200))
        self.time3.setObjectName("time")
        self.time3.setFont(QtGui.QFont("맑은 고딕",150)) 
        

        self.date = QtWidgets.QLabel(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(self.width-1750,self.height-100,300,50))
        self.date.setObjectName("date")
        self.date.setFont(QtGui.QFont("맑은 고딕",20))
        #===============================================================================
        #clock_button 이라는 이름으로 버튼을 생성 [쓰레드가 잘 작동하는지 확인]
        # self.clock_button = QtWidgets.QPushButton(self.centralwidget)
        # self.clock_button.setGeometry(QtCore.QRect(200, 280, 75, 23))
        # self.clock_button.setObjectName("clock_button")
        
        # self.youtube_button = QtWidgets.QPushButton(self.centralwidget)
        # self.youtube_button.setGeometry(QtCore.QRect(1500, 450, 75, 23))
        # self.youtube_button.setObjectName("youtube_button")
        #===================================================================
        self.news = QtWidgets.QLabel(self.centralwidget)
        self.news.setGeometry(QtCore.QRect(self.width-350,self.height-700,500,45))
        self.news.setText("실시간 뉴스")
        self.news.setFont(QtGui.QFont("맑은 고딕",15))        
        
        self.pol = QtWidgets.QLabel(self.centralwidget)
        self.pol.setGeometry(QtCore.QRect(self.width-500,self.height-670,500,45))
        self.pol.setText("경제")
        self.pol.setFont(QtGui.QFont("맑은 고딕",13))
        
        self.news1 = QtWidgets.QLabel(self.centralwidget)
        self.news1.setGeometry(QtCore.QRect(self.width-500,self.height-640,500,45))
        self.news1.setObjectName("news1")
        self.news1.setFont(QtGui.QFont("맑은 고딕",11))

        self.news2 = QtWidgets.QLabel(self.centralwidget)
        self.news2.setGeometry(QtCore.QRect(self.width-500,self.height-610,500,50))
        self.news2.setObjectName("news2")
        self.news2.setFont(QtGui.QFont("맑은 고딕",11))

        self.news3 = QtWidgets.QLabel(self.centralwidget)
        self.news3.setGeometry(QtCore.QRect(self.width-500,self.height-580,500,50))
        self.news3.setObjectName("news3")
        self.news3.setFont(QtGui.QFont("맑은 고딕",11))

        self.eco = QtWidgets.QLabel(self.centralwidget)
        self.eco.setGeometry(QtCore.QRect(self.width-500,self.height-550,500,50))
        self.eco.setText("정치")
        self.eco.setFont(QtGui.QFont("맑은 고딕",13))

        self.news4 = QtWidgets.QLabel(self.centralwidget)
        self.news4.setGeometry(QtCore.QRect(self.width-500,self.height-520,500,50))
        self.news4.setObjectName("news4")
        self.news4.setFont(QtGui.QFont("맑은 고딕",11))

        self.news5 = QtWidgets.QLabel(self.centralwidget)
        self.news5.setGeometry(QtCore.QRect(self.width-500,self.height-490,500,50))
        self.news5.setObjectName("news5")
        self.news5.setFont(QtGui.QFont("맑은 고딕",11))

        self.news6 = QtWidgets.QLabel(self.centralwidget)
        self.news6.setGeometry(QtCore.QRect(self.width-500,self.height-460,500,50))
        self.news6.setObjectName("news6")
        self.news6.setFont(QtGui.QFont("맑은 고딕",11))

        self.social = QtWidgets.QLabel(self.centralwidget)
        self.social.setGeometry(QtCore.QRect(self.width-500,self.height-430,500,50))
        self.social.setText("사회")
        self.social.setFont(QtGui.QFont("맑은 고딕",13))

        self.news7 = QtWidgets.QLabel(self.centralwidget)
        self.news7.setGeometry(QtCore.QRect(self.width-500,self.height-400,500,50))
        self.news7.setObjectName("news7")
        self.news7.setFont(QtGui.QFont("맑은 고딕",11))

        self.news8 = QtWidgets.QLabel(self.centralwidget)
        self.news8.setGeometry(QtCore.QRect(self.width-500,self.height-370,500,50))
        self.news8.setObjectName("news8")
        self.news8.setFont(QtGui.QFont("맑은 고딕",11))
        
        self.news9 = QtWidgets.QLabel(self.centralwidget)
        self.news9.setGeometry(QtCore.QRect(self.width-500,self.height-340,500,50))
        self.news9.setObjectName("news9")
        self.news9.setFont(QtGui.QFont("맑은 고딕",11))
        
        self.Entertain = QtWidgets.QLabel(self.centralwidget)
        self.Entertain.setGeometry(QtCore.QRect(self.width-500,self.height-310,500,50))
        self.Entertain.setText("문화/연예")
        self.Entertain.setFont(QtGui.QFont("맑은 고딕",13))

        self.news10 = QtWidgets.QLabel(self.centralwidget)
        self.news10.setGeometry(QtCore.QRect(self.width-500,self.height-280,500,50))
        self.news10.setObjectName("news10")
        self.news10.setFont(QtGui.QFont("맑은 고딕",11))

        self.news11 = QtWidgets.QLabel(self.centralwidget)
        self.news11.setGeometry(QtCore.QRect(self.width-500,self.height-250,500,50))
        self.news11.setObjectName("news11")
        self.news11.setFont(QtGui.QFont("맑은 고딕",11))
        
        self.news12 = QtWidgets.QLabel(self.centralwidget)
        self.news12.setGeometry(QtCore.QRect(self.width-500,self.height-220,500,50))
        self.news12.setObjectName("news12")
        self.news12.setFont(QtGui.QFont("맑은 고딕",11))
        
        self.Sports = QtWidgets.QLabel(self.centralwidget)
        self.Sports.setGeometry(QtCore.QRect(self.width-500,self.height-190,500,50))
        self.Sports.setText("스포츠")
        self.Sports.setFont(QtGui.QFont("맑은 고딕",13))

        self.news13 = QtWidgets.QLabel(self.centralwidget)
        self.news13.setGeometry(QtCore.QRect(self.width-500,self.height-160,500,50))
        self.news13.setObjectName("news13")
        self.news13.setFont(QtGui.QFont("맑은 고딕",11))

        self.news14 = QtWidgets.QLabel(self.centralwidget)
        self.news14.setGeometry(QtCore.QRect(self.width-500,self.height-130,500,50))
        self.news14.setObjectName("news14")
        self.news14.setFont(QtGui.QFont("맑은 고딕",11))
        
        self.news15 = QtWidgets.QLabel(self.centralwidget)
        self.news15.setGeometry(QtCore.QRect(self.width-500,self.height-100,500,50))
        self.news15.setObjectName("news15")
        self.news15.setFont(QtGui.QFont("맑은 고딕",11))

        #====================================================================
        #                            2번째 화면(날씨)
        self.two_time = QtWidgets.QLabel(self.centralwidget)
        self.two_time.setGeometry(QtCore.QRect(self.width-1900,self.height-1100,2000,100))
        self.two_time.setObjectName("two_time")
        self.two_time.setFont(QtGui.QFont("맑은 고딕",25))

        self.two_weather_1 = QtWidgets.QLabel(self.centralwidget)
        self.two_weather_1.setGeometry(QtCore.QRect(self.width-1800,self.height-1020,500,100))
        self.two_weather_1.setObjectName("two_weather")

        self.two_weather_2 = QtWidgets.QLabel(self.centralwidget)
        self.two_weather_2.setGeometry(QtCore.QRect(self.width-1585,self.height-1020,500,100))
        self.two_weather_2.setObjectName("two_weather")

        self.two_weather_3 = QtWidgets.QLabel(self.centralwidget)
        self.two_weather_3.setGeometry(QtCore.QRect(self.width-1355,self.height-1020,500,100))
        self.two_weather_3.setObjectName("two_weather")

        self.two_weather_4 = QtWidgets.QLabel(self.centralwidget)
        self.two_weather_4.setGeometry(QtCore.QRect(self.width-1125,self.height-1020,500,100))
        self.two_weather_4.setObjectName("two_weather")

        self.two_weather_5 = QtWidgets.QLabel(self.centralwidget)
        self.two_weather_5.setGeometry(QtCore.QRect(self.width-895,self.height-1020,500,100))
        self.two_weather_5.setObjectName("two_weather")

        self.two_weather_6 = QtWidgets.QLabel(self.centralwidget)
        self.two_weather_6.setGeometry(QtCore.QRect(self.width-665,self.height-1020,500,100))
        self.two_weather_6.setObjectName("two_weather")

        self.two_weather_7 = QtWidgets.QLabel(self.centralwidget)
        self.two_weather_7.setGeometry(QtCore.QRect(self.width-435,self.height-1020,500,100))
        self.two_weather_7.setObjectName("two_weather")
        
        self.two_weather_8 = QtWidgets.QLabel(self.centralwidget)
        self.two_weather_8.setGeometry(QtCore.QRect(self.width-205,self.height-1020,500,100))
        self.two_weather_8.setObjectName("two_weather")

        self.two_temp = QtWidgets.QLabel(self.centralwidget)
        self.two_temp.setGeometry(QtCore.QRect(self.width-1932,self.height-900,2000,700))
        self.two_temp.setObjectName("two_temp")
        self.two_temp.setFont(QtGui.QFont("맑은 고딕",20))       

        self.two_weatherinfo = QtWidgets.QLabel(self.centralwidget)
        self.two_weatherinfo.setGeometry(QtCore.QRect(self.width-1000,self.height-900,2000,700))
        self.two_weatherinfo.setObjectName("two_temp")
        self.two_weatherinfo.setFont(QtGui.QFont("맑은 고딕",18))     

        #====================================================================

        #====================================================================

        #====================================================================

        #====================================================================

        # 3번째화면

        self.calendar_component = QtWidgets.QWidget(self.centralwidget)
        self.calendar_component.setGeometry(QtCore.QRect(2, 100, 500, 300))

        self.calendar_component.setObjectName("three_calendar")
        self.three_calendar = QtWebEngineWidgets.QWebEngineView(self.calendar_component)
        self.three_calendar.setUrl(QUrl("https://calendar.google.com/calendar/embed?src=bbteng4%40gmail.com&ctz=Asia%2FSeoul"))
        self.three_calendar.setGeometry(0,0,500,300)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SmartMirror"))
        # self.clock_button.setText(_translate("MainWindow", "PushButton"))
        # self.youtube_button.setText(_translate("MainWindow", "Youtube"))

    def set_transparent_time(self, is_trans, MainWindow):
        if is_trans == True :
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.time2.setGraphicsEffect(opacity_effect)
        else:
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.time2.setGraphicsEffect(opacity_effect)

    def set_transparent_time2(self, is_trans, MainWindow):
        if is_trans == True :
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.time3.setGraphicsEffect(opacity_effect)
        else:
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.time3.setGraphicsEffect(opacity_effect)

    def set_transparent_main(self, is_trans, MainWindow):
        if is_trans == True:
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.main.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.weather.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.temperature.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.pol.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.eco.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.social.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.Entertain.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.Sports.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news1.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news2.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news3.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news4.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news5.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news6.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news7.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news8.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news9.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news10.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news11.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news12.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news13.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news14.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.news15.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_time.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_temp.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weather_1.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weather_2.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weather_3.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weather_4.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weather_5.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weather_6.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weather_7.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weather_8.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.two_weatherinfo.setGraphicsEffect(opacity_effect)

        else:
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.main.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.weather.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.temperature.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.pol.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.eco.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.social.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.Entertain.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.Sports.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news1.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news2.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news3.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news4.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news5.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news6.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news7.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news8.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news9.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news10.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news11.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news12.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news13.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news14.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1.0)
            self.news15.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_time.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_temp.setGraphicsEffect(opacity_effect) 

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weather_1.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weather_2.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weather_3.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weather_4.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weather_5.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weather_6.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weather_7.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weather_8.setGraphicsEffect(opacity_effect)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.0)
            self.two_weatherinfo.setGraphicsEffect(opacity_effect)

            
    
    #시간을 알려주는 함수 메인 화면에 생성
    # now.(year,month,day,hour,minute,second)
    def set_time(self,MainWindow):
        EvenOrAfter = "오전"
        k = 1
        k2 = 1
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_time.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_temp.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weather_1.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weather_2.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weather_3.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weather_4.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weather_5.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weather_6.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weather_7.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weather_8.setGraphicsEffect(opacity_effect)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        self.two_weatherinfo.setGraphicsEffect(opacity_effect)

        while True:
            now=datetime.datetime.now() #현재 시각을 시스템에서 가져옴
            hour=now.hour
            rawminute=now.minute
            weekday=weekday_cal(now.weekday())

            if(now.hour>=12):
                EvenOrAfter="오후"
                hour=now.hour%12

                if(now.hour==12):
                    hour=12

            else:
                EvenOrAfter="오전"

            if hour>=10:
                if k == 1:
                    self.set_transparent_time2(True, MainWindow)
                    self.set_transparent_time(True,MainWindow)
                    k = 0
                else:
                    self.set_transparent_time2(False, MainWindow)
                    k = 1       
            else:
                if k2 == 1:
                    self.set_transparent_time(True, MainWindow)
                    self.set_transparent_time2(True,MainWindow)
                    k2 = 0    
                else:
                    self.set_transparent_time(False, MainWindow)
                    k2 = 1                                            


                
                
            if(rawminute<10):
                minute=str(0)+str(rawminute)
            else:
                minute = rawminute
                
            self.date.setText("%s년 %s월 %s일 %s"%(now.year,now.month,now.day,weekday))
            self.time.setText(" %s %2s" %(hour,minute))
            self.time2.setText(":")
            self.time3.setText(":")
            self.ampm.setText("%s"%EvenOrAfter)
            self.main.setText("안녕하세요!")
            sleep(1)
            
    def weather_icon(self,MainWindow):
        while True:
 
            target=request.urlopen("http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=109")
            soup=BeautifulSoup(target,"html.parser")
            
            # 중기예보: 맑음, 구름조금, 구름많음, 구름많고 비, 구름많고 비/눈, 구름많고 눈/비, 구름많고 눈, 흐림, 흐리고 비, 흐리고 비/눈, 흐리고 눈/비, 흐리고 눈

            for location in soup.select("location"):
                city=location.select_one("city").string
                if city=="수원":
                    temp_min=location.select_one("tmn").string
                    temp_max=location.select_one("tmx").string
                    weather=location.select_one("wf").string
                    self.temperature.setText("%s  %s℃/%s℃  %s"%(city,temp_min,temp_max,weather))
                   
                    '''
                    if weather=="맑음":
                        pixmap=QPixmap("sunny.png")
                    elif weather=="구름조금":
                        pixmap=QPixmap("partlycloudy.png")
                    elif weather=="흐림" or "구름많음":
                        pixmap=QPixmap("cloudy.png")
                    elif weather=="구름많고 비" or "흐리고 비":
                        pixmap=QPixmap("rainy.png")
                    elif weather=="구름많고 비/눈" or "구름많고 눈/비" or "흐리고 비/눈" or "흐리고 눈/비":
                        pixmap=QPixmap("rainsnow.png")
                    elif weather=="구름많고 눈" or "흐리고 눈":
                        pixmap=QPixmap("snowy.png")    
                    
                    self.weather.setPixmap(QPixmap(pixmap))
                    '''
                    sleep(1000)
                    
    def two_weather_icon(self,MainWindow):
        while True:
            now=datetime.datetime.now()

            hour=now.hour
            hour2=hour+3
            hour3=hour2+3
            hour4=hour3+3
            hour5=hour4+3
            hour6=hour5+3
            hour7=hour6+3
            hour8=hour7+3

            hour_1=time_cal(hour)
            hour_2=time_cal(hour2)           
            hour_3=time_cal(hour3)
            hour_4=time_cal(hour4)
            hour_5=time_cal(hour5)
            hour_6=time_cal(hour6)
            hour_7=time_cal(hour7)   
            hour_8=time_cal(hour8)   

            self.two_time.setText("%13s%13s%13s%13s%13s%13s%13s%13s"%(hour_1,hour_2,hour_3,hour_4,hour_5,hour_6,hour_7,hour_8))

            target=request.urlopen("http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4111156600")
            soup=BeautifulSoup(target,"html.parser")
            target2=request.urlopen("http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=109")
            soup2=BeautifulSoup(target2,"html.parser")
            
            # 동네예보: 맑음, 구름 조금, 구름 많음, 흐림, 비, 눈/비, 눈
            temp_hour_3,temp_hour_6,temp_hour_9,temp_hour_12,temp_hour_15,temp_hour_18,temp_hour_21,temp_hour_24=0,0,0,0,0,0,0,0
            temp_hour_3=soup.select("temp")[0].text
            temp_hour_6=soup.select("temp")[1].text
            temp_hour_9=soup.select("temp")[2].text
            temp_hour_12=soup.select("temp")[3].text
            temp_hour_15=soup.select("temp")[4].text
            temp_hour_18=soup.select("temp")[5].text
            temp_hour_21=soup.select("temp")[6].text
            temp_hour_24=soup.select("temp")[7].text

            weekday1=weekday_cal(now.weekday())
            weekday2=weekday_cal(now.weekday()+1)
            weekday3=weekday_cal(now.weekday()+2)
            weekday4=weekday_cal(now.weekday()+3)
            weekday5=weekday_cal(now.weekday()+4)
            weekday6=weekday_cal(now.weekday()+5)

            for location in soup2.select("location"):
                city=location.select_one("city").string
                if city=="수원":
                    weekweather1=soup2.select("wf")[27].text
                    weekweather2=soup2.select("wf")[29].text
                    weekweather3=soup2.select("wf")[31].text
                    weekweather4=soup2.select("wf")[33].text
                    weekweather5=soup2.select("wf")[35].text
                    weekweather6=soup2.select("wf")[37].text

                    weektempmin1=soup2.select("tmn")[27].text
                    weektempmin2=soup2.select("tmn")[29].text
                    weektempmin3=soup2.select("tmn")[31].text
                    weektempmin4=soup2.select("tmn")[33].text
                    weektempmin5=soup2.select("tmn")[35].text
                    weektempmin6=soup2.select("tmn")[37].text

                    weektempmax1=soup2.select("tmx")[27].text
                    weektempmax2=soup2.select("tmx")[29].text
                    weektempmax3=soup2.select("tmx")[31].text
                    weektempmax4=soup2.select("tmx")[33].text
                    weektempmax5=soup2.select("tmx")[35].text
                    weektempmax6=soup2.select("tmx")[37].text

                    weatherinfo=soup2.select("wf")[0].text

                    weatherinfo=weatherinfo.replace("<br />","\n")
                    

                    j=0
                    for i in range (0,len(weatherinfo)):
                        j=j+1
                        if weatherinfo[i]=="\n":
                            j=0
                        if j>50:
                            j=0
                            weatherinfo=weatherinfo[:i]+"\n"+weatherinfo[i:]
                    

            self.two_temp.setText("%21s℃%21s℃%21s℃%21s℃%21s℃%21s℃%21s℃%21s℃ \
                                  \n\n\n%21s     %s   %s℃ / %s℃\n\n%21s     %s   %s℃ / %s℃ \
                                  \n\n%21s     %s   %s℃ / %s℃\n\n%21s     %s   %s℃ / %s℃ \
                                  \n\n%21s     %s   %s℃ / %s℃\n\n%21s     %s   %s℃ / %s℃ \
                                  \n\n" \
                                  %(temp_hour_3,temp_hour_6,temp_hour_9,temp_hour_12,
                                  temp_hour_15,temp_hour_18,temp_hour_21,temp_hour_24,
                                  weekday1,weekweather1,weektempmin1,weektempmax1,
                                  weekday2,weekweather2,weektempmin2,weektempmax2,
                                  weekday3,weekweather3,weektempmin3,weektempmax3,
                                  weekday4,weekweather4,weektempmin4,weektempmax4,
                                  weekday5,weekweather5,weektempmin5,weektempmax5,
                                  weekday6,weekweather6,weektempmin6,weektempmax6,))
            self.two_weatherinfo.setText("%s"%weatherinfo)
                    
            weather_3=soup.select("wfKor")[0].text
            weather_6=soup.select("wfKor")[1].text
            weather_9=soup.select("wfKor")[2].text
            weather_12=soup.select("wfKor")[3].text
            weather_15=soup.select("wfKor")[4].text
            weather_18=soup.select("wfKor")[5].text
            weather_21=soup.select("wfKor")[6].text
            weather_24=soup.select("wfKor")[7].text
            
            pixmap1=weather_icon_cal(weather_3)
            pixmap2=weather_icon_cal(weather_6)
            pixmap3=weather_icon_cal(weather_9)
            pixmap4=weather_icon_cal(weather_12)
            pixmap5=weather_icon_cal(weather_15)
            pixmap6=weather_icon_cal(weather_18)
            pixmap7=weather_icon_cal(weather_21)
            pixmap8=weather_icon_cal(weather_24)

            self.two_weather_1.setPixmap(QPixmap(pixmap1))
            self.two_weather_2.setPixmap(QPixmap(pixmap2))
            self.two_weather_3.setPixmap(QPixmap(pixmap3))
            self.two_weather_4.setPixmap(QPixmap(pixmap4))
            self.two_weather_5.setPixmap(QPixmap(pixmap5))
            self.two_weather_6.setPixmap(QPixmap(pixmap6))
            self.two_weather_7.setPixmap(QPixmap(pixmap7))
            self.two_weather_8.setPixmap(QPixmap(pixmap8))
            sleep(1000)
    
    #News (타이틀&기사 출력)
    def News_Eco(self,MainWindow) :
        d = feedparser.parse(self.News_url_Economy)
        while True :
            num = 1
            for e in d.entries :
                if num==16:
                    num=0
                elif num%3==1:
                    self.news1.setText("[%d] %s"%(num,e.title))
                elif num%3==2:
                    self.news2.setText("[%d] %s"%(num,e.title))
                elif num%3==0:
                    self.news3.setText("[%d] %s"%(num,e.title))
                    sleep(10)
                num=num+1
    
    def News_Pol(self,MainWindow) :
        d = feedparser.parse(self.News_url_Politics)
        while True :
            num = 1
            for e in d.entries :
                if num==16:
                    num=0
                elif num%3==1:
                    self.news4.setText("[%d] %s"%(num,e.title))
                elif num%3==2:
                    self.news5.setText("[%d] %s"%(num,e.title))
                elif num%3==0:
                    self.news6.setText("[%d] %s"%(num,e.title))
                    sleep(10)
                num=num+1
                
    def News_Soc(self,MainWindow) :
        d = feedparser.parse(self.News_url_Social)
        while True :
            num = 1
            for e in d.entries :
                if num==16:
                    num=0
                elif num%3==1:
                    self.news7.setText("[%d] %s"%(num,e.title))
                elif num%3==2:
                    self.news8.setText("[%d] %s"%(num,e.title))
                elif num%3==0:
                    self.news9.setText("[%d] %s"%(num,e.title))
                    sleep(10)
                num=num+1
                
    def News_Ent(self,MainWindow) :
        d = feedparser.parse(self.News_url_Entertain)
        while True :
            num = 1
            for e in d.entries :
                if num==16:
                    num=0
                elif num%3==1:
                    self.news10.setText("[%d] %s"%(num,e.title))
                elif num%3==2:
                    self.news11.setText("[%d] %s"%(num,e.title))
                elif num%3==0:
                    self.news12.setText("[%d] %s"%(num,e.title))
                    sleep(10)
                num=num+1
                
    def News_Spo(self,MainWindow) :
        d = feedparser.parse(self.News_url_Sports)
        while True :
            num = 1
            for e in d.entries :
                if num==16:
                    num=0
                elif num%3==1:
                    self.news13.setText("[%d] %s"%(num,e.title))
                elif num%3==2:
                    self.news14.setText("[%d] %s"%(num,e.title))
                elif num%3==0:
                    self.news15.setText("[%d] %s"%(num,e.title))
                    sleep(10)
                num=num+1

    

    #----------------------------------------------------------------------------------------------------
    #------------------------ 쓰레드 ---------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------

    #Set_time을 쓰레드로 사용
    def time_start(self,MainWindow):
        thread=threading.Thread(target=self.set_time,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()
    
    #weather_icon을 쓰레드로 사용
    def weather_start(self,MainWindow):
        thread=threading.Thread(target=self.weather_icon,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()
    
    #News를 쓰레드로 사용
    def News_Pol_start(self,MainWindow):
        thread=threading.Thread(target=self.News_Pol,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()
        
    def News_Eco_start(self,MainWindow):
        thread=threading.Thread(target=self.News_Eco,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()
        
    def News_Soc_start(self,MainWindow):
        thread=threading.Thread(target=self.News_Soc,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()
        
    def News_Ent_start(self,MainWindow):
        thread=threading.Thread(target=self.News_Ent,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()
        
    def News_Spo_start(self,MainWindow):
        thread=threading.Thread(target=self.News_Spo,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

    def two_weather_start(self,MainWindow):
        thread=threading.Thread(target=self.two_weather_icon,args=(self,))
        thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()
        
class Window(QtWidgets.QMainWindow):
    music_list=["music.wav","music2.mp3"]
    pygame.mixer.init()
    pygame.mixer.music.load(music_list[0])
    

    def __init__(self):
        super(Window,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.time_start(MainWindow) #time thread
    
        self.ui.weather_start(MainWindow) #weather thread

        self.ui.News_Pol_start(MainWindow) #news thread
        self.ui.News_Eco_start(MainWindow) #news thread
        self.ui.News_Soc_start(MainWindow) #news thread
        self.ui.News_Ent_start(MainWindow) #news thread
        self.ui.News_Spo_start(MainWindow) #news thread

        self.ui.two_weather_start(MainWindow) #weather thread        



    
    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()    
        if e.key() == Qt.Key_F1: # 메인화면
            self.ui.set_transparent_main(False,MainWindow)
        if e.key() == Qt.Key_F2: # 날씨 보여주기
            self.ui.set_transparent_main(True,MainWindow)
        if ((e.key() == Qt.Key_F3) or (e.key() == Qt.Key_F4)): # 노래 틀기 / 다음노래 틀기
            if pygame.mixer.music.get_busy()==False:
                pygame.mixer.music.play()
            else:
                if pygame.mixer.music.get_busy()==True:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("music2.mp3")
                    pygame.mixer.music.play()
        if e.key() == Qt.Key_F5: # 노래 끄기
            pygame.mixer.music.stop()


    

    
    

#-------------메인---------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

if __name__=="__main__":
    import sys


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Window()

    #ui.setupUi(MainWindow)
    # ui.button(MainWindow)

    


    MainWindow.show()



    sys.exit(app.exec_())


