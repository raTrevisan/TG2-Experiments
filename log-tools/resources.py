import pandas as pd
import matplotlib.pyplot as plt
import os

def split_cpu_usage(input_file, split_times):
    """Split CPU usage data at specified times and return segments."""
    # Read the combined CPU usage data
    df = pd.read_csv(input_file)
    
    # Ensure the timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create a list to hold the segments
    segments = []
    
    # Split the data at the specified times
    for i in range(len(split_times) - 1):
        start_time = pd.to_datetime(split_times[i])
        end_time = pd.to_datetime(split_times[i + 1])
        segment = df[(df['timestamp'] >= start_time) & (df['timestamp'] < end_time)]
        segments.append(segment)
    
    # Handle the last segment after the last split time
    last_segment = df[df['timestamp'] >= pd.to_datetime(split_times[-1])]
    segments.append(last_segment)
    
    return segments

def plot_cpu_usage(segment, output_file):
    """Plot CPU usage for a given segment."""
    plt.figure(figsize=(12, 7))
    plt.plot(segment['timestamp'], segment['value'], color='#3498db', linewidth=2, label='CPU Usage')
    
    # Customize the plot
    plt.xlabel('Time', fontsize=12, fontweight='bold')
    plt.ylabel('CPU Usage (%)', fontsize=12, fontweight='bold')
    plt.title('CPU Usage Over Time Segment', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved CPU usage graph to: {output_file}")
    plt.close()

if __name__ == "__main__":
    input_file = './data/combined_cpu_usage.csv'
    output_dir = './data/split_segments'
    os.makedirs(output_dir, exist_ok=True)
    
    # Define split times
    split_times = ['03:28:00', '05:08:00', '07:06:00']
    
    # Split the CPU usage data
    segments = split_cpu_usage(input_file, split_times)
    
    # Save each segment to a separate CSV file and plot
    for i, segment in enumerate(segments):
        segment_file = os.path.join(output_dir, f'cpu_usage_segment_{i + 1}.csv')
        segment.to_csv(segment_file, index=False)
        print(f"Saved segment {i + 1} to: {segment_file}")
        
        # Plot the segment
        plot_file = os.path.join(output_dir, f'cpu_usage_plot_segment_{i + 1}.png')
        plot_cpu_usage(segment, plot_file)