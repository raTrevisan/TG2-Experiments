import sys
from os import listdir

def is_valid_message(line):
    """Check if line contains a valid message with sent and received times"""
    return "sent" in line

def get_next_message(file):
    """Read lines until a valid message is found or EOF"""
    while True:
        line = file.readline()
        if not line:  # EOF
            return ""
        if is_valid_message(line):
            return line

def get_time_from_message(message, ref_time):
    """Extract and convert time from message to seconds from reference"""
    try:
        time_str = message.split(" at ")[1][11:30]
        
        # Convert times to seconds, handling potential format issues
        def safe_float_convert(time_part):
            try:
                # First try normal float conversion
                return float(time_part)
            except ValueError:
                # If fails, extract numbers and pad with zeros
                numbers = ''.join(c for c in time_part if c.isdigit())
                if '.' in time_part:
                    # Handle decimal numbers
                    whole, decimal = time_part.split('.')
                    whole_nums = ''.join(c for c in whole if c.isdigit())
                    decimal_nums = ''.join(c for c in decimal if c.isdigit())
                    return float(f"{whole_nums}.{decimal_nums:0<6}")
                else:
                    # Handle whole numbers
                    return float(numbers)

        # Split and convert times
        ref_h, ref_m, ref_s = ref_time[0:2], ref_time[3:5], ref_time[6:14]
        time_h, time_m, time_s = time_str[0:2], time_str[3:5], time_str[6:14]
        
        # Convert each part safely
        seconds = safe_float_convert(time_s) - safe_float_convert(ref_s)
        minutes = safe_float_convert(time_m) - safe_float_convert(ref_m)
        hours = safe_float_convert(time_h) - safe_float_convert(ref_h)
        
        return seconds + (60 * minutes) + (3600 * hours)
    except Exception as e:
        print(f"Error processing time from message: {e}")
        print(f"Problematic message: {message}")
        return None

def parse():
    protocols = {"quic", "tcp"}
    
    for protocol in protocols:
        print(f"\nProcessing {protocol} files...")
        
        try:
            # Setup paths
            raw_dir = f"./data/{sys.argv[1]}/raw/{protocol}/"
            
            # Get list of valid files (ending in number)
            valid_files = [f for f in listdir(raw_dir) if f[-5].isdigit()]
            if not valid_files:
                print(f"No valid files found for {protocol}")
                continue
                
            print(f"Found {len(valid_files)} valid files")
            
            # Get reference time from file-0
            ref_file = next((f for f in valid_files if f.endswith("-0.log")), None)
            if not ref_file:
                print(f"No reference file (ending in -0) found for {protocol}")
                continue
                
            with open(raw_dir + ref_file) as f:
                ref_msg = get_next_message(f)
                if not ref_msg:
                    print(f"Reference file empty for {protocol}")
                    continue
                ref_time = ref_msg.split(" at ")[1][11:30]
            
            # Process all files and write to history file
            msg_count = 0
            with open(f"./data/{protocol}_hf.log", 'w') as hf:
                # Open all files
                files = [open(raw_dir + f, 'r') for f in valid_files]
                curr_msgs = [None] * len(files)
                
                # Get first message from each file
                for i, f in enumerate(files):
                    curr_msgs[i] = get_next_message(f)
                    if not curr_msgs[i]:
                        print(f"Warning: No messages in {valid_files[i]}")
                
                # Process all messages
                while any(msg != "" for msg in curr_msgs):
                    # Find earliest message
                    valid_times = []
                    for i, msg in enumerate(curr_msgs):
                        if msg:
                            time = get_time_from_message(msg, ref_time)
                            if time is not None:
                                valid_times.append((time, i))
                    
                    if not valid_times:
                        break
                        
                    # Get earliest message
                    curr_time, idx = min(valid_times)
                    
                    # Write to history file and get next message
                    hf.write(f"{curr_time}\n")
                    curr_msgs[idx] = get_next_message(files[idx])
                    msg_count += 1
                
                # Close all files
                for f in files:
                    f.close()
            
            print(f"Successfully processed {msg_count} messages for {protocol}")
            
        except Exception as e:
            print(f"Error processing {protocol}: {str(e)}")
            continue

if __name__ == "__main__":
    parse()