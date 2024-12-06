import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

def extract_timestamps(log_file):
    timestamps = []
    with open(log_file, 'r') as f:
        for line in f:
            if "Message received on topic" in line:
                try:
                    # Extract the timestamp from the log entry
                    # The timestamp is located after the last 'sent' in the line
                    timestamp_str = line.split("sent ")[0].strip().split("at ")[1]
                    # Convert the timestamp string to a datetime object
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                    timestamps.append(timestamp)
                except (ValueError, IndexError):
                    continue  # Skip lines that don't have valid timestamps
    return timestamps

def analyze_messages_per_second(log_directory):
    all_timestamps = []
    
    # Read all log files in the specified directory
    log_files = [f for f in os.listdir(log_directory) if f.endswith('.log')]
    
    if not log_files:
        print("No log files found in the specified directory.")
        return
    
    for log_file in log_files:
        timestamps = extract_timestamps(os.path.join(log_directory, log_file))
        all_timestamps.extend(timestamps)
    
    # Check if any timestamps were extracted
    if not all_timestamps:
        print("No timestamps extracted from log files.")
        return
    
    # Create a DataFrame to count messages per second
    df = pd.DataFrame(all_timestamps, columns=['timestamp'])
    
    # Ensure the 'timestamp' column is of datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  # Use errors='coerce' to handle invalid parsing
    
    # Check for any NaT values after conversion
    if df['timestamp'].isnull().any():
        print("Warning: Some timestamps could not be converted to datetime.")
        print(df[df['timestamp'].isnull()])  # Print rows with NaT values

    # Round down to the nearest second
    df['second'] = df['timestamp'].dt.floor('S')
    
    # Count messages per second
    messages_per_second = df.groupby('second').size()

    # Check if there are any messages to plot
    if messages_per_second.empty:
        print("No messages received per second to plot.")
        return

    # Print the results
    print("Messages received per second:")
    print(messages_per_second)

    # Plotting the results
    plt.figure(figsize=(12, 6))
    messages_per_second.plot(kind='line', marker='o', color='red')
    plt.title('Messages Received Per Second (TCP)', fontsize=16)
    plt.xlabel('Time (seconds)', fontsize=14)
    plt.ylabel('Number of Messages', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels
    plt.savefig('messages_per_second.png')  # Save the plot as a PNG file
    plt.show()  # Display the plot

def main():
    log_directory = './data/quicxtcp/tcp_10c_2b/raw/tcp/'  # Updated path to the new log directory
    analyze_messages_per_second(log_directory)

if __name__ == "__main__":
    main()