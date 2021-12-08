
import RPi.GPIO as GPIO
import threading
import time
from tkinter import *  
import spidev
from flask import Flask, request
from flask import render_template

app = Flask(__name__)


TRIG = 23
ECHO = 24

# 불필요한 warning 제거, GPIO핀의 번호 모드 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Trig와 Echo 핀의 출력/입력 설정 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

#Trig핀의 신호를 0으로 출력 
GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)

@app.route("/")
def home():
    return render_template('final.html')

@app.route("/dis")    
def dis():                                  
    try:
        GPIO.output(TRIG, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
        time.sleep(0.00001)       # 10µs 딜레이 
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            start = time.time()	 # Echo 핀 상승 시간 
        while GPIO.input(ECHO)==1:
            stop= time.time()	 # Echo 핀 하강 시간 
            
        check_time = stop - start
        distance = check_time * 34300 / 2

        return "%.14f cm" % distance

        
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        return "fail"





if __name__ == "__main__":
    app.run(host="0.0.0.0")