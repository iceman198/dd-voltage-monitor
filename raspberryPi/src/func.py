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
    n = 12000;
    lineskips = 120;
    myfilename = logging_path + voltage_log_name;
    newlines = [];
    returnlines = [];
    file = open(myfilename,'r');
    lines = file.readlines(); #2021-10-11 13:34:28,13.032547808773282,566,13.078599214457993,568,23.555294007729803,1023,11.950339775182568,519

    if (len(lines) < n): n = len(lines);
    i = 0;
    line_avg_a1, line_avg_a2, line_avg_a3, line_avg_a4, line_avg_v1, line_avg_v2, line_avg_v3, line_avg_v4 = [0]*8;
    line_max_a1, line_max_a2, line_max_a3, line_max_a4, line_max_v1, line_max_v2, line_max_v3, line_max_v4 = [0]*8;
    line_min_a1, line_min_a2, line_min_a3, line_min_a4, line_min_v1, line_min_v2, line_min_v3, line_min_v4 = [1000]*8;
    while(n > 0):
        line = lines[len(lines) - n];
        lineArr = line.split(',');

        if (len(lineArr) < 6) : 
            n = n - 1;
            print('skipping on n: ' + str(n) + ' line-len= ' + str(len(lines)) + ' with line: ' + str(line));
            continue;

        #print('working on n: ' + str(n) + ' line-len= ' + str(len(lines)) + ' with line: ' + str(line));

        if float(lineArr[1]) > line_max_v1: line_max_v1 = float(lineArr[1]);
        if float(lineArr[1]) < line_min_v1: line_min_v1 = float(lineArr[1]);
        line_avg_v1 = line_avg_v1 + float(lineArr[1]);

        if float(lineArr[2]) > line_max_a1: line_max_a1 = float(lineArr[2]);
        if float(lineArr[2]) < line_min_a1: line_min_a1 = float(lineArr[2]);
        line_avg_a1 = line_avg_a1 + float(lineArr[2]);
        #print('line_avg_a1: ' + str(line_avg_a1) + ' ## lineArr2: ' + str(lineArr[2]));

        if float(lineArr[3]) > line_max_v2: line_max_v2 = float(lineArr[3]);
        if float(lineArr[3]) < line_min_v2: line_min_v2 = float(lineArr[3]);
        line_avg_v2 = line_avg_v2 + float(lineArr[3]);

        if float(lineArr[4]) > line_max_a2: line_max_a2 = float(lineArr[4]);
        if float(lineArr[4]) < line_min_a2: line_min_a2 = float(lineArr[4]);
        line_avg_a2 = line_avg_a2 + float(lineArr[4]);

        if float(lineArr[5]) > line_max_v3: line_max_v3 = float(lineArr[5]);
        if float(lineArr[5]) < line_min_v3: line_min_v3 = float(lineArr[5]);
        line_avg_v3 = line_avg_v3 + float(lineArr[5]);

        if float(lineArr[6]) > line_max_a3: line_max_a3 = float(lineArr[6]);
        if float(lineArr[6]) < line_min_a3: line_min_a3 = float(lineArr[6]);
        line_avg_a3 = line_avg_a2 + float(lineArr[6]);

        if float(lineArr[7]) > line_max_v4: line_max_v4 = float(lineArr[7]);
        if float(lineArr[7]) < line_min_v4: line_min_v4 = float(lineArr[7]);
        line_avg_v4 = line_avg_v4 + float(lineArr[7]);

        if float(lineArr[8]) > line_max_a4: line_max_a4 = float(lineArr[8]);
        if float(lineArr[8]) < line_min_a4: line_min_a4 = float(lineArr[8]);
        line_avg_a4 = line_avg_a4 + float(lineArr[8]);
        
        i = i + 1;
        if (i > lineskips | n <= 1):
            line_avg_a1 = line_avg_a1 / i;
            line_avg_a2 = line_avg_a2 / i;
            line_avg_a3 = line_avg_a3 / i;
            line_avg_a4 = line_avg_a4 / i;
            line_avg_v1 = line_avg_v1 / i;
            line_avg_v2 = line_avg_v2 / i;
            line_avg_v3 = line_avg_v3 / i;
            line_avg_v4 = line_avg_v4 / i;
            i = 0;
            returnlines.append({
                'timestamp': lineArr[0],
                'a1': {
                    'min': line_min_a1,
                    'max': line_max_a1,
                    'avg': line_avg_a1
                    },
                'a2': {
                    'min': line_min_a2,
                    'max': line_max_a2,
                    'avg': line_avg_a2
                    },
                'a3': {
                    'min': line_min_a3,
                    'max': line_max_a3,
                    'avg': line_avg_a3
                    },
                'a4': {
                    'min': line_min_a4,
                    'max': line_max_a4,
                    'avg': line_avg_a4
                    },
                'v1': {
                    'min': line_min_v1,
                    'max': line_max_v1,
                    'avg': line_avg_v1
                    },
                'v2': {
                    'min': line_min_v2,
                    'max': line_max_v2,
                    'avg': line_avg_v2
                    },
                'v3': {
                    'min': line_min_v3,
                    'max': line_max_v3,
                    'avg': line_avg_v3
                    },
                'v4': {
                    'min': line_min_v4,
                    'max': line_max_v4,
                    'avg': line_avg_v4
                    }
            });
            line_avg_a1, line_avg_a2, line_avg_a3, line_avg_a4, line_avg_v1, line_avg_v2, line_avg_v3, line_avg_v4 = [0]*8;
            line_max_a1, line_max_a2, line_max_a3, line_max_a4, line_max_v1, line_max_v2, line_max_v3, line_max_v4 = [0]*8;
            line_min_a1, line_min_a2, line_min_a3, line_min_a4, line_min_v1, line_min_v2, line_min_v3, line_min_v4 = [1000]*8;

        newlines.append(lines[len(lines) - n]);
        n = n - 1;

    return returnlines;

    #if (len(lines) > n):
    #    while(n > 0):
    #        newlines.append(lines[len(lines) - n]);
    #        n = n - lineskips;
    #    #print('get_history if return ' + str(newlines));
    #    return newlines;
    #elif (len(lines) > lineskips):
    #    #print('get_history else return ' + str(lines));
    #    t = len(lines);
    #    while(t > 0):
    #        newlines.append(lines[len(lines) - t]);
    #        t = t - lineskips;
    #        #print('get_history returned a line');
    #    return newlines;
    #else :
    #    return lines;
