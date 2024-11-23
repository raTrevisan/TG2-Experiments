import matplotlib.pyplot as plt
import numpy as np
from os import listdir

def get_next_message(file):
    cond = True
    while cond:
        line = file.readline()
        split = line.split("sent")
        if len(split) == 2:
            cond = False
        if line == "":
            cond = False
    return line

def extract_times(message):
    if message == "":
        return None
    try:
        # Extract sent and received times
        parts = message.split("sent at ")[1].split(" received at ")
        sent_time = parts[0][11:30]  # Extract HH:MM:SS.xxxxx
        received_time = parts[1][11:30]
        return sent_time, received_time
    except:
        return None

def to_sec(time_string, ref_time):
    ref_hour = ref_time[0:2]
    ref_minute = ref_time[3:5]
    ref_second = ref_time[6:14]
    
    time_hour = time_string[0:2]
    time_minute = time_string[3:5]
    time_second = time_string[6:14]
    
    seconds = float(time_second) - float(ref_second)
    minutes = float(time_minute) - float(ref_minute)
    hours = float(time_hour) - float(ref_hour)
    return (seconds + 60 * (minutes + (60 * hours)))

def create_histogram():
    path = "./data/"
    protocols = {"tcp-test/raw/tcp": "TCP", "quic-test/raw/quic": "QUIC"}
    latencies = {protocol: [] for protocol in protocols.values()}
    
    for protocol_path, protocol_name in protocols.items():
        full_path = path + protocol_path
        files = listdir(full_path)
        
        for filename in files:
            with open(f"{full_path}/{filename}", 'r') as f:
                while True:
                    message = get_next_message(f)
                    if message == "":
                        break
                        
                    times = extract_times(message)
                    if times:
                        sent_time, received_time = times
                        # Calculate latency
                        latency = to_sec(received_time, sent_time)
                        if 0 <= latency < 1:  # Filter out unreasonable values
                            latencies[protocol_name].append(latency)

    # Create the histogram
    plt.figure(figsize=(12, 6))
    
    # Plot histograms
    plt.hist(latencies['TCP'], bins=50, alpha=0.5, label='TCP', color='blue')
    plt.hist(latencies['QUIC'], bins=50, alpha=0.5, label='QUIC', color='red')
    
    # Customize the plot
    plt.xlabel('Latency (seconds)')
    plt.ylabel('Number of Messages')
    plt.title('Distribution of Message Latencies: TCP vs QUIC')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Print statistics
    for protocol in protocols.values():
        lat = np.array(latencies[protocol])
        print(f"\n{protocol} Statistics:")
        print(f"Average latency: {np.mean(lat):.6f} seconds")
        print(f"Median latency: {np.median(lat):.6f} seconds")
        print(f"Standard deviation: {np.std(lat):.6f} seconds")
        print(f"Number of messages: {len(lat)}")

    # Save the plot
    plt.savefig('./data/latency_histogram.png')
    plt.close()

if __name__ == "__main__":
    create_histogram() 