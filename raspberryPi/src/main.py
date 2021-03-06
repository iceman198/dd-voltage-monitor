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
mydelay = 5.0;

serInput = serial.Serial('/dev/ttyUSB0',9600,timeout=0.1);
serInput.flushInput();

app = Flask(__name__);
time_updates = time.time();
CURRENT_VOLTAGE = "";

def check_for_notification():
    global CURRENT_VOLTAGE;
    #func.log('main.py', 'check_for_notification', 'start');
    rec_buff = '';
    resp = "";
    try:
        time.sleep(0.25);
        if serInput.inWaiting():
            time.sleep(0.01);
            rec_buff = serInput.read(serInput.inWaiting());
            resp = str(rec_buff.decode());

        if (len(resp) > 0):
            # example response should be: V1:5.41|analogVal:355,V2:5.63|analogVal:369,V2:5.52|analogVal:362,V2:5.12|analogVal:336
            #func.log('main.py', 'check_for_notification', 'resp: ' + resp);
            if ('\n' in resp):
                resp = resp.replace('\r', '');
                resp = resp.split('\n')[0];

            varr = resp.split(',');
            if (len(varr) > 1):# & ('\n' not in varr):
                #v1 = varr[0].split('|')[0].split(':')[1];
                a1 = varr[0].split('|')[1].split(':')[1];
                v1 = calculate_voltage(a1);
                #v2 = varr[1].split('|')[0].split(':')[1];
                a2 = varr[1].split('|')[1].split(':')[1];
                v2 = calculate_voltage(a2);
                #v3 = varr[2].split('|')[0].split(':')[1];
                a3 = varr[2].split('|')[1].split(':')[1];
                v3 = calculate_voltage(a3);
                #v4 = varr[3].split('|')[0].split(':')[1];
                a4 = varr[3].split('|')[1].split(':')[1];
                v4 = calculate_voltage(a4);

                #a2 = (float(varr[1].split('|')[1].split(':')[1]) / 4.5) / 10 ;

                CURRENT_VOLTAGE = {
                    'v1': v1,
                    'a1': a1,
                    'v2': v2,
                    'a2': a2,
                    'v3': v3,
                    'a3': a3,
                    'v4': v4,
                    'a4': a4
                };
                func.log_voltage(v1, a1, v2, a2, v3, a3, v4, a4);
                if "S" in resp:
                    vardummy = "";
                elif "H" in resp:
                    vardummy = "";
                else:
                    vardummy = "";
    except:
        func.log('main.py', 'check_for_notification', 'Exception (' + str(sys.exc_info()) + ') has been caught.');

    #func.log('main.py', 'check_for_notification', 'end');
    return resp;

def calculate_voltage(value):
    R1 = 27730.0;
    R2 = 7463.0;
    vOUT = (float(value) * 5.0) / 1024.0;
    vIN = vOUT / (R2/(R1+R2));
    return vIN;

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

@app.route('/getvoltage/')
def flask_getvoltage():
    global CURRENT_VOLTAGE;
    resp_obj = {
        'status': "SUCCESS",
        'voltage': CURRENT_VOLTAGE
        }
    return jsonify(resp_obj);

@app.route('/gethistory/')
def flask_gethistory():
    histArr = func.get_history();
    resp_obj = {
        'status': "SUCCESS",
        'history': histArr
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
