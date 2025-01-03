import numpy as np
from scipy import stats
import glob
import os
from datetime import datetime

def parse_log_file(filename):
    times = []
    latencies = []
    
    with open(filename, 'r') as f:
        for line in f:
            if 'Message received' not in line:
                continue
                
            try:
                # Extract received and sent timestamps
                received_str = line.split(' at ')[1].split(' sent ')[0]
                sent_str = line.split(' sent ')[1].strip()
                
                # Convert strings to datetime objects
                received_time = datetime.strptime(received_str, '%Y-%m-%d %H:%M:%S.%f')
                sent_time = datetime.strptime(sent_str, '%Y-%m-%d %H:%M:%S.%f')
                
                # Calculate latency in milliseconds
                latency = (received_time - sent_time).total_seconds() * 1000
                
                # Store timestamp and latency
                times.append(received_time.timestamp())
                latencies.append(latency)
                
            except (ValueError, IndexError) as e:
                print(f"Warning: Could not parse line in {filename}: {line.strip()}")
                continue
    
    return np.array(times), np.array(latencies)

def calculate_statistics():
    # Base directory for the logs
    base_dir = './data/tcp-extra-clients'
    
    # Process each type
    for type_num in [1, 2, 3, 4]:
        type_dir = f'type-{type_num}'
        type_path = os.path.join(base_dir, type_dir)
        
        if not os.path.exists(type_path):
            continue
            
        log_files = glob.glob(os.path.join(type_path, f'mqtt-quic-{type_dir}-sub-*.log'))
        log_files.sort()
        
        if not log_files:
            continue

        # Collect all timestamps and latencies
        all_times = []
        all_latencies = []
        earliest_time = float('inf')
        
        for file in log_files:
            times, latencies = parse_log_file(file)
            if len(times) > 0:
                earliest_time = min(earliest_time, times[0])
                all_times.extend(times)
                all_latencies.extend(latencies)

        if not all_times:
            print(f"No data found for type {type_num}")
            continue

        # Convert to numpy arrays
        all_times = np.array(all_times)
        all_latencies = np.array(all_latencies)
        rel_times = all_times - earliest_time

        # Calculate basic statistics
        total_messages = len(all_times)
        total_duration = rel_times[-1] - rel_times[0]
        avg_msgs_per_sec = total_messages / total_duration

        # Calculate latency statistics
        mean_latency = np.mean(all_latencies)
        median_latency = np.median(all_latencies)
        std_latency = np.std(all_latencies)
        
        # Calculate confidence intervals for latency
        ci_90 = stats.t.interval(0.90, len(all_latencies)-1, 
                               loc=mean_latency, 
                               scale=stats.sem(all_latencies))
        ci_95 = stats.t.interval(0.95, len(all_latencies)-1, 
                               loc=mean_latency, 
                               scale=stats.sem(all_latencies))
        ci_99 = stats.t.interval(0.99, len(all_latencies)-1, 
                               loc=mean_latency, 
                               scale=stats.sem(all_latencies))

        # Calculate percentiles
        percentiles = [50, 75, 90, 95, 99]
        latency_percentiles = np.percentile(all_latencies, percentiles)

        print(f"\nStatistics for Type {type_num}:")
        print(f"Number of subscribers: {len(log_files)}")
        print(f"Total messages: {total_messages}")
        print(f"Total duration: {total_duration:.2f} seconds")
        print(f"Average messages per second: {avg_msgs_per_sec:.2f}")
        print("\nLatency Statistics (ms):")
        print(f"  Mean: {mean_latency:.3f}")
        print(f"  Median: {median_latency:.3f}")
        print(f"  Std Dev: {std_latency:.3f}")
        print("\nConfidence Intervals (ms):")
        print(f"  90% CI: [{ci_90[0]:.3f}, {ci_90[1]:.3f}]")
        print(f"  95% CI: [{ci_95[0]:.3f}, {ci_95[1]:.3f}]")
        print(f"  99% CI: [{ci_99[0]:.3f}, {ci_99[1]:.3f}]")
        print("\nLatency Percentiles (ms):")
        for p, value in zip(percentiles, latency_percentiles):
            print(f"  {p}th: {value:.3f}")
        print("---")

if __name__ == "__main__":
    calculate_statistics()