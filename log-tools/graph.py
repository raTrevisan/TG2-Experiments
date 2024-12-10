import matplotlib.pyplot as plt
import numpy as np
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
                
                # Store timestamp (as seconds since start) and latency
                times.append(received_time.timestamp())
                latencies.append(latency)
                
            except (ValueError, IndexError) as e:
                print(f"Warning: Could not parse line in {filename}: {line.strip()}")
                continue
    
    return np.array(times), np.array(latencies)

def create_graphs():
    # Base directory for the logs
    base_dir = './data/quic-50-1'
    
    # Create a graph for each type
    for type_num in [1, 2, 3]:
        type_dir = f'type-{type_num}'
        type_path = os.path.join(base_dir, type_dir)
        
        if not os.path.exists(type_path):
            continue
            
        log_files = glob.glob(os.path.join(type_path, f'mqtt-quic-{type_dir}-sub-*.log'))
        log_files.sort()
        
        if not log_files:
            continue
            
        # Create two subplots: one for timestamps, one for latencies
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        colors = plt.cm.rainbow(np.linspace(0, 1, len(log_files)))
        
        # Collect all timestamps for combined plot
        all_times = []
        earliest_time = float('inf')
        
        # First pass to find earliest timestamp
        for file in log_files:
            times, _ = parse_log_file(file)
            if len(times) > 0:
                earliest_time = min(earliest_time, times[0])
        
        # Second pass to plot data
        for file, color in zip(log_files, colors):
            times, latencies = parse_log_file(file)
            if len(times) == 0:
                print(f"Warning: No valid data found in {file}")
                continue
            
            # Convert to relative times
            rel_times = times - earliest_time
            all_times.extend(times)
            
            # Plot latencies against time
            sub_num = file.split('-')[-1].replace('.log', '')
            label = f'Subscriber {sub_num}'
            ax2.plot(rel_times, latencies, '.', color=color, label=label, alpha=0.7, markersize=2)

        if all_times:
            # Sort all timestamps and create combined plot
            all_times = np.array(sorted(all_times))
            rel_times = all_times - earliest_time
            
            # Create message density plot (messages vs time)
            ax1.plot(rel_times, np.arange(len(all_times)), 'b-', label='All Messages', alpha=0.8)

        # Customize timestamp plot
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Cumulative Message Count')
        ax1.set_title(f'QUIC Message Delivery Progress - Type {type_num}')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=5)

        # Customize latency plot
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Latency (ms)')
        ax2.set_title(f'QUIC Message Latency by Subscriber - Type {type_num}')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=5)

        # Adjust layout to make room for legends
        plt.subplots_adjust(bottom=0.15, hspace=0.35)

        # Save the plot
        output_dir = './data/graphs'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, f'quic_50_clients_type_{type_num}_analysis.png'))
        plt.close()

if __name__ == "__main__":
    create_graphs()
