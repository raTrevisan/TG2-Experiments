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

def get_ref_time(path, folder):
    # Get list of files in the folder
    files = listdir(path + folder)
    if not files:
        raise Exception(f"No files found in {path + folder}")
    
    # Find the file ending with -0
    ref_file = None
    for file in files:
        if file.endswith("-0.log"):
            ref_file = file
            break
    
    if ref_file is None:
        raise Exception(f"No reference file ending with '-0' found in {path + folder}")
    
    # Open reference file and get first message time
    with open(path + folder + "/" + ref_file) as f:
        message = get_next_message(f)
        print(f)
        if message == "":
            raise Exception("Reference file is empty")
        
        # Extract time from message
        try:
            time = message.split(" at ")[1][11:30]
            return time
        except IndexError:
            raise Exception("Invalid message format")
        

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


def parse():
    protocols = {"quic", "tcp"}
    for protocol in protocols:
        print(f"Processing {protocol} files...")
        
        try:
            # Write history file to main data directory
            with open(f"./data/" + sys.argv[1] + "-" + protocol + "_hf.log", 'w') as hf:
                try:
                    # Still read from test-specific directories
                    test_dir = f"./data/" + sys.argv[1] + "/raw/"
                    ref_time = get_ref_time(test_dir, protocol)
                except Exception as e:
                    print(f"Skipping {protocol}: {str(e)}")
                    continue
                
                f_lists = listdir(test_dir + protocol)
                files = [open(test_dir + protocol + "/" + x, 'r') for x in f_lists]
                curr = [None] * len(files)

                for f in range(len(files)):
                    curr[f] = get_next_message(files[f])
                
                if all(msg == "" for msg in curr):
                    print(f"Skipping {protocol}: All files are empty")
                    for f in files:
                        f.close()
                    continue

                while not check_empty(curr):
                    curr_time = compare_time(curr, ref_time)
                    hf.write(f"{curr_time[0]}\n")
                    curr[curr_time[1]] = get_next_message(files[curr_time[1]])

                for f in files:
                    f.close()
                    
        except Exception as e:
            print(f"Error processing {protocol}: {str(e)}")
            continue


if __name__ == "__main__" :
    parse()