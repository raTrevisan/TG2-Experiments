import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def parse_cluster_log(filename):
    """Parse cluster manager log and extract node count over time"""
    timestamps = []
    node_counts = []
    
    # Regular expression for the metrics line
    metrics_pattern = re.compile(
        r'date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+) \|Cluster size: (\d+)'
    )
    
    with open(filename, 'r') as f:
        for line in f:
            match = metrics_pattern.search(line)
            if match:
                # Extract timestamp and cluster size
                timestamp_str = match.group(1)
                cluster_size = int(match.group(2))
                
                # Convert timestamp string to datetime
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                
                timestamps.append(timestamp)
                node_counts.append(cluster_size)
    
    return timestamps, node_counts

def create_node_count_graph(base_dirs, output_dir):
    """Create graph comparing node counts across different configurations"""
    plt.figure(figsize=(12, 7))
    
    # Colors for different configurations
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f']
    
    # Config labels
    config_labels = {
        'quic-manager-16-inflight': 'Inflight 16',
        'quic-manager-32-inflight': 'Inflight 32',
        'quic-manager-1000-queue': 'Fila 1000',
        'quic-manager-5000-queue': 'Fila 5000'
    }
    
    # Track the shortest experiment duration
    min_duration = float('inf')
    
    # First pass to find the shortest duration
    for base_dir in base_dirs:
        log_file = os.path.join(base_dir, 'cluster-manager.log')
        if not os.path.exists(log_file):
            print(f"Warning: {log_file} not found")
            continue
            
        # Parse log file
        timestamps, _ = parse_cluster_log(log_file)
        
        if timestamps:
            duration = (max(timestamps) - min(timestamps)).total_seconds()
            min_duration = min(min_duration, duration)
    
    # Second pass to plot with consistent x-axis
    for base_dir, color in zip(base_dirs, colors):
        log_file = os.path.join(base_dir, 'cluster-manager.log')
        if not os.path.exists(log_file):
            continue
            
        # Parse log file
        timestamps, node_counts = parse_cluster_log(log_file)
        
        if not timestamps:
            continue
            
        # Convert timestamps to seconds from start
        start_time = min(timestamps)
        time_seconds = [(t - start_time).total_seconds() for t in timestamps]
        
        # Plot this configuration
        config_name = os.path.basename(base_dir)
        plt.plot(time_seconds, node_counts, color=color, linewidth=2, 
                label=config_labels[config_name])
    
    # Customize the plot
    plt.xlabel('Tempo (segundos)', fontsize=12, fontweight='bold')
    plt.ylabel('Número de Nós', fontsize=12, fontweight='bold')
    plt.title('Evolução do Número de Nós por Configuração', 
             fontsize=14, fontweight='bold')
    
    # Set x-axis limit to shortest experiment duration
    plt.xlim(0, min_duration)
    
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Ensure y-axis starts at 0
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    
    # Save the plot
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'node_count_evolution.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved node count evolution graph to: {output_path}")
    plt.close()

if __name__ == "__main__":
    base_dirs = [
        './data/quic-manager-16-inflight',
        './data/quic-manager-32-inflight',
        './data/quic-manager-1000-queue',
        './data/quic-manager-5000-queue'
    ]
    
    output_dir = './data/graphs'
    create_node_count_graph(base_dirs, output_dir) 