import datetime;

def print_test():
    print('This is a test');

def log(file, service, text):
    f = open("/home/pi/share/voltageMonitor.log", "a");
    now = datetime.datetime.now();
    mystring = str(now.strftime('%Y-%m-%d %H:%M:%S')) + ' *** ' + str(file) + ' *** ' + str(service) + '() ~ ' + str(text);
    print(mystring);
    f.write(mystring+'\r\n');

def log_voltage(v1, v2, v3, v4):
    f = open("/home/pi/share/volageLog.csv", "a");
    now = datetime.datetime.now();
    mystring = str(now.strftime('%Y-%m-%d %H:%M:%S')) + ',' + str(v1) + ',' + str(v2) + ',' + str(v3) + ',' + str(v4);
    f.write(mystring+'\r\n');

