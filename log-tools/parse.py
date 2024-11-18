import sys
from os import listdir
from os import stat


def get_next_message(file) :
    cond = True
    while cond :
        line = file.readline()
        split = line.split("sent")
        if len(split) == 2 :
            cond = False
        if line == (""):
            cond = False
    return line

def to_sec(time_string, ref_time):
    #print(ref_time)
    ref_hour = ref_time[0:2]
    ref_minute = ref_time[3:5]
    ref_second = ref_time[6:14]
    #print(ref_hour, ref_minute, ref_second)
    #print(time_string)
    time_hour = time_string[0:2]
    time_minute = time_string[3:5]
    time_second = time_string[6:14]
    #print(time_hour, time_minute, time_second)
    seconds = float(time_second) - float(ref_second)   #clock algebra 
    minutes = float(time_minute) - float(ref_minute)
    hours = float(time_hour) - float(ref_hour)
    return (seconds + 60 * (minutes + (60 * hours)))


def validate_files(files):
    valid_files = []
    for file in files:
        message = get_next_message(file) #primeira mensagem de cada file
        #print(message)
        if message != "" :
            valid_files.append(file)
            print(message)
    print(valid_files)
    return files

def write_to_file

def parse_messages(files):
    valid_files = validate_files(files)
    write_to_file(valid_files)

def parse():
    protocols = {"quic", "tcp"}
    exp_name = sys.argv[1]
    for protocol in protocols:
        files = [open("./data/" + exp_name + "/raw/" + protocol + "/" + file) for file in listdir("./data/" + exp_name + "/raw/" + protocol)]
        parse_messages(files)

if __name__ == "__main__" :
    parse()