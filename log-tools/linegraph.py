import sys
from os import listdir

def get_next_message(file) :
    cond = True
    while cond :
        line = file.readline()
        split = line.split("from")
        if len(split) == 2 :
            cond = False
        if line == (""):
            cond = False
    return line

def get_ref_time(path, folder):
    f = open( path +  folder + "twin-" + folder +"-stateful-0.log")
    message = get_next_message(f).split(" at ")[1][11:30]
    f.close()
    return message

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

def compare_time(message, ref_time):
    time = [None] * len(message)
    lowest = 1000000
    for f in range(len(message)):
        if message[f] != "":
            #print(message[f])
            time[f] = to_sec(message[f].split(" at ")[1][11:30], ref_time)
            if time[f] < lowest:
                lowest = time[f]
                pos = f
    message_tuple = (lowest,pos)
    return message_tuple

def file_write(curr_time, path ,folder, curr_message):
        
        pfile = open(path + "parsed_" + folder + ".log","a")

        pfile.write(str(curr_time[0]))
        pfile.write(",")
        pfile.write(str(curr_message))
        pfile.write(",")
        pfile.write(" from file ")
        pfile.write(str(curr_time[1]))
        pfile.write("\n")

def check_empty(curr):
    finished = 0
    for x in range(len(curr)):
        if curr[x] == "" :
            finished += 1
    if finished == len(curr):
        return 1
    return 0


def parse() :

    for i in range(1,6):
        path = " ./logs_test_10" + "/"
        for folder in "well", "mc",:
            
            print(path + folder)
            print(path)
            m = 0
            run = True
            ref_time = get_ref_time(path , folder)
            f_lists = listdir(path + folder)
            files = [open(path + folder + "/" + x,'r') for x in f_lists]
            curr = [None] * len(files)

            # initializes files_vector
            for f in range(len(files)):
                curr[f] = get_next_message(files[f])
                #print(curr[f])

            while run == True :
                curr_time = compare_time(curr, ref_time)
                file_write(curr_time, path, folder, m)
                m = m + 50
                curr[curr_time[1]] = get_next_message(files[curr_time[1]])
                if check_empty(curr) :
                    run = False



if __name__ == "__main__" :
    parse()