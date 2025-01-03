import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from datetime import datetime
import seaborn as sns

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

def create_histogram():
    # Update the style setting
    sns.set_style("whitegrid")
    
    # Base directory for the logs
    base_dir = './data/quic-worst-case'
    
    # Create output directory
    output_dir = './data/graphs'
    os.makedirs(output_dir, exist_ok=True)

    # Set fixed x-axis limits and bins
    x_min = 0
    x_max = 500
    n_bins = 50  # Fixed number of bins
    bin_edges = np.linspace(x_min, x_max, n_bins + 1)  # Create fixed bin edges
    grid_step = 50
    grid_lines = np.arange(x_min, x_max + grid_step, grid_step)
    
    # Define colors and labels
    colors = {
        1: '#2ecc71',  # Industrial IoT = Green
        2: '#3498db',  # Process Automation = Blue
        3: '#e74c3c',  # Critical = Red
        4: '#9b59b6',  # Augmented Reality = Purple
    }

    labels = {
        1: 'Industrial IoT',
        2: 'Process Automation',
        3: 'Critical',
        4: 'Augmented Reality'
    }

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

        # Collect latencies from all files
        all_latencies = []
        for file in log_files:
            latencies = parse_log_file(file)
            if len(latencies) > 0:
                all_latencies.extend(latencies)

        if not all_latencies:
            continue

        all_latencies = np.array(all_latencies)
        
        # Create figure with two subplots sharing x-axis
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[1, 3], 
                                      sharex=True, facecolor='white')
        
        # Set the same x-axis grid for both plots
        grid_alpha = 0.3
        grid_color = 'gray'
        grid_linestyle = '--'
        
        # Plot boxplot on top
        color = colors[type_num]
        bp = ax1.boxplot(all_latencies, 
                        vert=False,      
                        patch_artist=True,
                        medianprops=dict(color="black", linewidth=1.5),
                        boxprops=dict(facecolor=color, alpha=0.7, 
                                    edgecolor='black', linewidth=1.5),
                        flierprops=dict(marker='.',          # Circle marker style
                                      markerfacecolor='none', # Transparent fill
                                      markeredgecolor='red',  # Red edge color
                                      markersize=4,          # Marker size
                                      alpha=0.1,             # Very transparent
                                      linewidth=1))          # Edge thickness
        
        # Style the whiskers and caps
        for whisker in bp['whiskers']:
            whisker.set_color('black')
            whisker.set_linewidth(1.5)
        for cap in bp['caps']:
            cap.set_color('black')
            cap.set_linewidth(1.5)
        
        ax1.set_yticks([])  # Hide y-axis ticks for boxplot
        
        # Plot histogram below
        n, bins, patches = ax2.hist(all_latencies, bins=bin_edges, color=color, alpha=0.7, 
                                  edgecolor='black', linewidth=1)
        
        # Add mean and median lines to both plots
        mean_latency = np.mean(all_latencies)
        median_latency = np.median(all_latencies)
        for ax in [ax1, ax2]:
            ax.axvline(mean_latency, color='red', linestyle='dashed', linewidth=2)
            ax.axvline(median_latency, color='green', linestyle='dashed', linewidth=2)
            
            # Update both axes to use fixed limits
            ax.set_xlim(x_min, x_max)
            ax.set_xticks(grid_lines)
            ax.grid(True, linestyle=grid_linestyle, alpha=grid_alpha, color=grid_color)
        
        # Add legend to boxplot
        mean_line = ax1.axvline(mean_latency, color='red', linestyle='dashed', linewidth=2, 
                              label=f'Mean: {mean_latency:.2f}ms')
        median_line = ax1.axvline(median_latency, color='green', linestyle='dashed', linewidth=2, 
                                label=f'Median: {median_latency:.2f}ms')
        ax1.legend(loc='upper right')
        
        # Set labels and title
        ax2.set_xlabel('Latency (ms)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        fig.suptitle(f'Latency Distribution - {labels[type_num]}', 
                    fontsize=14, fontweight='bold', y=0.95)
        
        # Add statistics text box
        stats_text = f'n: {len(all_latencies)}\n'
        stats_text += f'Mean: {mean_latency:.2f}ms\n'
        stats_text += f'Median: {median_latency:.2f}ms\n'
        stats_text += f'Std Dev: {np.std(all_latencies):.2f}ms'
        
        ax2.text(0.95, 0.95, stats_text,
                transform=ax2.transAxes,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'),
                verticalalignment='top',
                horizontalalignment='right')
        
        # Adjust spacing between plots
        plt.subplots_adjust(hspace=0)  # Remove space between plots
        
        # Save the figure
        plt.savefig(os.path.join(output_dir, f'quic_best_case_{type_num}_distribution.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    create_histogram()