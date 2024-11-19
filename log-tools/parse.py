import sys
from os import listdir


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

def time_sec(time_1, time_2):

    time_1_hour = time_1[0:2]
    time_1_minute = time_1[3:5]
    time_1_second = time_1[6:14]

    time_2_hour = time_2[0:2]
    time_2_minute = time_2[3:5]
    time_2_second = time_2[6:14]

    time_1 = ((float(time_1_hour) * 60 + float(time_1_minute)) * 60 + float(time_1_second)) 
    time_2 = ((float(time_2_hour) * 60 + float(time_2_minute)) * 60 + float(time_2_second)) 

    return time_2 - time_1

def validate_files(files):
    valid_files = []
    for file in files:
        # Try to read the first message
        message = get_next_message(file)
        if message.strip() != "":  # Check if message is non-empty after removing whitespace
            # Reset file pointer to beginning before adding to valid files
            file.seek(0)
            valid_files.append(file)
    return valid_files

def get_time_rel(messages):
    i = 0
    delays = []
    for i in range(len(messages)):
        split = messages[i].split("sent")
        sent = split[1].split(" ")[2]
        recv = split[0].split(" ")[11]
        delays.append(time_sec(sent, recv))
    return i, delays


def get_time_abs(files, ref_time):
    pass


def write_to_file(valid_files):
    
    pass

def update_messages(n, messages, files):
    messages[n] = get_next_message(files[n])
    return messages

def parse_messages(files):
    messages = []
    hf = open("./hf.log", 'a+')


    for file in files:
        messages.append(get_next_message(file)) 
        print(messages)

    while True:
        #line_write = get_time_abs(messages,ref_time)
        hist_get = get_time_rel(messages)
        print(hist_get[1])
        hf.write(hist_get[1])
        messages[hist_get[0]] = get_next_message(files[hist_get[0]])

        
        #print(messages)


def parse():
    protocols = {"quic", "tcp"}
    exp_name = sys.argv[1]
    for protocol in protocols:
        files = [open("./data/" + exp_name + "/raw/" + protocol + "/" + file) for file in listdir("./data/" + exp_name + "/raw/" + protocol)]
        valid_files = validate_files(files)  # Add this line
        parse_messages(valid_files)  # Pass valid_files instead of files

if __name__ == "__main__" :
    parse()