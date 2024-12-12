import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from datetime import datetime

def parse_log_file(filename):
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
                latencies.append(latency)
                
            except (ValueError, IndexError) as e:
                print(f"Warning: Could not parse line in {filename}: {line.strip()}")
                continue
    
    return np.array(latencies)

def create_histograms():
    # Base directory for the logs
    base_dir = './data/quic-40-1-manager-fix'
    
    # Create a histogram for each type
    for type_num in [1, 2, 3]:
        type_dir = f'type-{type_num}'
        type_path = os.path.join(base_dir, type_dir)
        
        if not os.path.exists(type_path):
            continue
            
        log_files = glob.glob(os.path.join(type_path, f'mqtt-quic-{type_dir}-sub-*.log'))
        log_files.sort()
        
        if not log_files:
            continue
            
        # Create figure
        plt.figure(figsize=(12, 6))
        
        # Collect all latencies
        all_latencies = []
        
        for file in log_files:
            latencies = parse_log_file(file)
            all_latencies.extend(latencies)

        if all_latencies:
            all_latencies = np.array(all_latencies)
            
            # Create histogram
            plt.hist(all_latencies, bins=50, alpha=0.7, color='blue', edgecolor='black')
            
            # Calculate statistics
            mean_latency = np.mean(all_latencies)
            median_latency = np.median(all_latencies)
            p95_latency = np.percentile(all_latencies, 95)
            p99_latency = np.percentile(all_latencies, 99)
            
            # Add vertical lines for statistics
            plt.axvline(mean_latency, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_latency:.2f}ms')
            plt.axvline(median_latency, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median_latency:.2f}ms')
            plt.axvline(p95_latency, color='orange', linestyle='dashed', linewidth=2, label=f'95th: {p95_latency:.2f}ms')
            plt.axvline(p99_latency, color='purple', linestyle='dashed', linewidth=2, label=f'99th: {p99_latency:.2f}ms')
            
            # Add 50ms threshold line and percentage for type 3
            if type_num == 3:
                plt.axvline(50, color='black', linestyle='dotted', linewidth=2, label='50ms threshold')
                under_50ms = all_latencies[all_latencies <= 50]
                percent_under_50 = (len(under_50ms) / len(all_latencies)) * 100
                plt.text(0.98, 0.95, f'{percent_under_50:.1f}% ≤ 50ms', 
                        transform=plt.gca().transAxes, 
                        horizontalalignment='right',
                        verticalalignment='top',
                        bbox=dict(facecolor='white', alpha=0.8))

        # Customize plot
        plt.xlabel('Latency (ms)')
        plt.ylabel('Frequency')
        plt.title(f'QUIC Message Latency Distribution - Type {type_num}')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=5 if type_num == 3 else 4)

        # Adjust layout
        plt.subplots_adjust(bottom=0.2)

        # Save the plot
        output_dir = './data/graphs'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, f'quic_40_clients_type_{type_num}_histogram.png'))
        plt.close()

if __name__ == "__main__":
    create_histograms()