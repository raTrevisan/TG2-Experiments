import os
import pandas as pd  # Import pandas for datetime handling
import matplotlib.pyplot as plt
import numpy as np

def extract_latencies(log_file):
    latencies = []
    with open(log_file, 'r') as f:
        for line in f:
            if "Message received on topic" in line and "sent" in line:
                try:
                    # Extracting the received and sent timestamps
                    received_time_str = line.split("at ")[1].split(" sent")[0].strip()
                    sent_time_str = line.split("sent ")[1].strip()

                    # Convert timestamps to seconds since epoch
                    received_time = pd.to_datetime(received_time_str).timestamp()
                    sent_time = pd.to_datetime(sent_time_str).timestamp()
                    
                    # Calculate latency
                    latency = received_time - sent_time
                    latencies.append(latency)
                except (ValueError, IndexError):
                    continue  # Skip lines that don't have valid times
    return latencies

def main():
    log_directory = './data/quicxtcp/tcp_10c_2b/raw/tcp/'  # Update this path as needed
    log_files = [f for f in os.listdir(log_directory) if f.endswith('.log')]
    
    all_latencies = []
    
    for log_file in log_files:
        latencies = extract_latencies(os.path.join(log_directory, log_file))
        all_latencies.extend(latencies)
    
    # Calculate summary statistics
    mean_latency = np.mean(all_latencies)
    median_latency = np.median(all_latencies)
    std_latency = np.std(all_latencies)

    # Create histogram
    plt.figure(figsize=(12, 8))
    plt.hist(all_latencies, bins=50, range=(0, 0.02), color='red', alpha=0.7, edgecolor='black')
    plt.title('Histogram of Latencies TCP', fontsize=16)
    plt.xlabel('Latency (seconds)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.axvline(mean_latency, color='purple', linestyle='dashed', linewidth=1, label=f'Mean: {mean_latency:.4f} s')
    plt.axvline(median_latency, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_latency:.4f} s')
    plt.legend()
    plt.grid(True)
    
    # Save the histogram as a PNG file
    plt.savefig('latency_histogram_tcp.png')  
    plt.show()  # Display the histogram

    # Print summary statistics
    print(f"Mean Latency: {mean_latency:.4f} seconds")
    print(f"Median Latency: {median_latency:.4f} seconds")
    print(f"Standard Deviation: {std_latency:.4f} seconds")

if __name__ == "__main__":
    main()