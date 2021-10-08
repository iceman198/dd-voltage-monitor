#!/usr/bin/python
import sys;
import os;
import time;
import signal;
import serial;

from flask import Flask, jsonify, render_template;
from threading import Thread;

import func;

doLoop = True;
mydelay = 0.5;

serInput = serial.Serial('/dev/ttyUSB0',9600,timeout=0.1);
serInput.flushInput();

app = Flask(__name__);
time_updates = time.time();


def check_for_notification():
    func.log('main.py', 'check_for_notification', 'start');
    rec_buff = '';
    resp = "";
    try:
        time.sleep(0.25);
        if serInput.inWaiting():
            time.sleep(0.01);
            rec_buff = serInput.read(serInput.inWaiting());
        resp = str(rec_buff.decode());

        if len(resp) > 0:
            if "S" in rec_buff.decode():
                vardummy = "";
            elif "H" in rec_buff.decode():
                vardummy = "";
            else:
                vardummy = "";
            func.log('main.py', 'check_for_notification', 'rec_buff: ' + rec_buff.decode());
    except:
        func.log('main.py', 'check_for_notification', 'Exception (' + str(sys.exc_info()) + ') has been caught.');

    func.log('main.py', 'check_for_notification', 'end');
    return resp;

def shutdown():
    currentLine1 = "Shutting down...";
    time.sleep(5);
    os.system("sudo shutdown now");

@app.route('/')
def index():
    #disp.display_text("Index hit");
    return render_template('index.html');

@app.route('/shutdown/')
def flask_shutdown():
    shutdown();
    mybody = "Shutdown initiated";
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return jsonify(resp_obj);

@app.route('/service/jsontest/')
def flask_jsontest():
    mybody = "This is my json test";
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return jsonify(resp_obj);

def main_loop():
    global doLoop, time_updates;
    while doLoop:
        try:
            timediff = time.time() - time_updates;
            #func.log('main.py', 'myloop', 'Current time ' + str(time.time()) + ' with a timediff of ' + str(timediff));
            if (timediff > mydelay):
                check_for_notification();
                time_updates = time.time();
        except:
            func.log('main.py', 'main_loop', 'Exception: ' + str(sys.exc_info()));

def start_flask():
    try:
        func.log('main.py', 'start_flask', 'Flask running');
        app.run(debug=False, host='0.0.0.0');
    except:
        func.log('main.py', 'start_flask', 'Exception: ' + str(sys.exc_info()));

if __name__ == '__main__':
    try:
        thread1 = Thread(target=main_loop);
        thread2 = Thread(target=start_flask);
        thread1.start();
        thread2.start();
        thread1.join();
        thread2.join();
    except :
        func.log('main.py', '__main__', 'Exception (ID: {}) has been caught. Cleaning up...'.format(signal));
        exit(0);
