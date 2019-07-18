import sys

from workalendar.asia import SouthKorea
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QCalendarWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate, Qt
from datetime import datetime, timedelta

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat(QCalendarWidget.NoVerticalHeader))
        cal.clicked[QDate].connect(self.showDate)

        # 한국 공휴일 캘린더 객체 생성 후 올해 기준으로 휴일을 3년간 Q캘린터에 표시
        wcal = SouthKorea()
        date = QDate.currentDate()

        # 해당 연도의 공휴일을 리스트로 반환
        # print(wcal.holidays(date.year()))

        # 공휴일 표시 서식 설정
        fm = QTextCharFormat()
        fm.setForeground(Qt.red)
        # fm.setBackground(Qt.yellow)

        # 올해 기준 전년, 올해, 다음해까지 공휴일 표시
        for one in wcal.holidays(date.year()-1):
            print(one[0])
            cal.setDateTextFormat(one[0], fm)

        for one in wcal.holidays(date.year()):
            print(one[0])
            cal.setDateTextFormat(one[0], fm)

        for one in wcal.holidays(date.year()+1):
            print(one[0])
            cal.setDateTextFormat(one[0], fm)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())

        self.lblmsg = QLabel(self)
        self.lblmsg.setText("강의 일정 계산")
        self.showDate(date)

        vbox = QVBoxLayout()
        vbox.addWidget(cal)
        vbox.addWidget(self.lbl)
        vbox.addWidget(self.lblmsg)

        self.setLayout(vbox)

        self.setWindowTitle('종강일 계산기')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def showDate(self, date):
        self.lbl.setText(date.toString())
        selectDate = date.toPyDate()
        # print(selectDate)
        to_wday = selectDate.weekday()

        # Weekday return value: 0~6(월~토요일)
        if to_wday == 1 or to_wday == 3:
            msgEnd = self.calculate_date('tue', selectDate)
        elif to_wday == 0 or to_wday == 2:
            msgEnd = self.calculate_date('mon', selectDate)
        else:
            msgEnd = "개강 할 수 없습니다."

        self.lblmsg.setText(msgEnd)

    def calculate_date(self, start, selectDate):
        cnt = 0
        day_cnt = 0

        # workalendar 나라 설정
        kcal = SouthKorea()

        # 개강일이 월, 화인지 설정
        if start == 'mon': sd = 0
        if start == 'tue': sd = 1

        # 정규반 종강일 checkday 계산
        while cnt != 8:
            checkday = selectDate + timedelta(days=day_cnt)
            if checkday.weekday() == sd or checkday.weekday() == sd + 2:
                # print(cnt, checkday, checkday.weekday())
                if kcal.is_working_day(checkday):
                    cnt += 1
            day_cnt += 1

        # 속성반 종강일 fastcheckday 계산
        cnt = 0
        day_cnt = 0
        while cnt != 16:
            fastcheckday = selectDate + timedelta(days=day_cnt)
            # 월요일부터 목요일까지 계산 (0~3)
            if fastcheckday.weekday() >= 0 and fastcheckday.weekday() < 4:
                if kcal.is_working_day(fastcheckday):
                    cnt += 1
            day_cnt += 1

        msgEnd = "정규반 %s수강 시 종강일은 %s입니다." % (selectDate.strftime("%m-%d"), checkday.strftime("%m-%d"))
        msgEnd += "\n속성반 %s수강 시 종강일은 %s입니다." % (selectDate.strftime("%m-%d"), fastcheckday.strftime("%m-%d"))

        return msgEnd

if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())