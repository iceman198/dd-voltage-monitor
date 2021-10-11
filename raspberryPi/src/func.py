import datetime;
import os;


logging_path = "/home/pi/share/";
log_file_name = "voltageMonitor.log";
voltage_log_name = "voltageLog.csv";

file_size_max_mb = 2;

def print_test():
    print('This is a test');

def log(myclass, service, text):
    verify_file(logging_path + log_file_name);
    update_file_if_needed(logging_path, log_file_name);
    f = open(logging_path + log_file_name, "a");
    now = datetime.datetime.now();
    mystring = str(now.strftime('%Y-%m-%d %H:%M:%S')) + ' *** ' + str(myclass) + ' *** ' + str(service) + '() ~ ' + str(text);
    print(mystring);
    f.write(mystring+'\r\n');
    f.close();

def log_voltage(v1, a1, v2, a2, v3, a3, v4, a4):
    verify_file(logging_path + voltage_log_name);
    update_file_if_needed(logging_path, voltage_log_name);
    f = open(logging_path + voltage_log_name, "a");
    now = datetime.datetime.now();
    mystring = str(now.strftime('%Y-%m-%d %H:%M:%S')) + ',' + str(v1) + ',' + str(a1) + ',' + str(v2) + ',' + str(a2) + ',' + str(v3) + ',' + str(a3) + ',' + str(v4) + ',' + str(a4);
    f.write(mystring+'\n');
    f.close();

def update_file_if_needed(filepath, oldfilename):
    file_size = os.path.getsize(filepath + oldfilename);
    size_in_mb = file_size/1024**2;
    if (size_in_mb > file_size_max_mb):
        now = datetime.datetime.now();
        new_file_name = oldfilename + str(now.strftime('%Y-%m-%d_%H%M%S'));
        os.rename(filepath + oldfilename, filepath + new_file_name);
        verify_file(filepath + oldfilename);

def verify_file(filewithpath):
    try:
        f = open(filewithpath);
        f.close();
    except FileNotFoundError:
        f = open(filewithpath,"a");
        f.close();

def get_history():
    #print('get_history start');
    n = 6000;
    lineskips = 60;
    myfilename = logging_path + voltage_log_name;
    newlines = [];
    file = open(myfilename,'r');
    lines = file.readlines();

    if (len(lines) > n):
        while(n > 0):
            newlines.append(lines[len(lines) - n]);
            n = n - lineskips;
        #print('get_history if return ' + str(newlines));
        return newlines;
    elif (len(lines) > lineskips):
        #print('get_history else return ' + str(lines));
        t = len(lines);
        while(t > 0):
            newlines.append(lines[len(lines) - t]);
            t = t - lineskips;
            print('get_history returned a line');
        return newlines;
    else :
        return lines;
