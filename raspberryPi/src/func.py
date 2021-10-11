import datetime;
import os;


logging_path = "/home/pi/share/";
log_file_name = "voltageMonitor.log";
voltage_log_name = "voltageLog.csv";

file_size_max_mb = 2;

def print_test():
    print('This is a test');

def log(myclass, service, text):
    update_file_if_needed(logging_path, log_file_name);
    f = open(logging_path + log_file_name, "a");
    now = datetime.datetime.now();
    mystring = str(now.strftime('%Y-%m-%d %H:%M:%S')) + ' *** ' + str(myclass) + ' *** ' + str(service) + '() ~ ' + str(text);
    print(mystring);
    f.write(mystring+'\r\n');

def log_voltage(v1, a1, v2, a2, v3, a3, v4, a4):
    update_file_if_needed(logging_path, voltage_log_name);
    f = open(logging_path + voltage_log_name, "a");
    now = datetime.datetime.now();
    mystring = str(now.strftime('%Y-%m-%d %H:%M:%S')) + ',' + str(v1) + ',' + str(a1) + ',' + str(v2) + ',' + str(a2) + ',' + str(v3) + ',' + str(a3) + ',' + str(v4) + ',' + str(a4);
    f.write(mystring+'\n');

def update_file_if_needed(filepath, oldfilename):
    file_size = os.path.getsize(filepath + oldfilename);
    size_in_mb = file_size/1024**2;
    if (size_in_mb > file_size_max_mb):
        now = datetime.datetime.now();
        new_file_name = oldfilename + str(now.strftime('%Y-%m-%d_%H%M%S'));
        os.rename(filepath + oldfilename, filepath + new_file_name);

def get_history():
    print('get_history start');
    n = 2000;
    myfilename = logging_path + voltage_log_name;
    newlines = [];
    file = open(myfilename,'r');
    lines = file.readlines();

    if (len(lines) > n):
        while(n > 0):
            newlines.push(lines[len(lines) - n]);
            n = n - 1;
        print('get_history if return');
        return newlines;
    else:
        print('get_history else return ' + str(lines));
        return lines;
