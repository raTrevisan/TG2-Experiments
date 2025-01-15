import glob
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def parse_log_file(filename, max_latency):
    """Parse log file and count messages within latency threshold"""
    received_count = 0
    delayed_count = 0
    
    with open(filename, 'r') as f:
        for line in f:
            if 'Message received' not in line:
                continue
                
            try:
                # Split the line by 'at' and 'sent' to get the timestamps
                parts = line.split(' at ')
                if len(parts) != 2:
                    continue
                    
                # Get timestamps
                timestamp_parts = parts[1].split(' sent ')
                received_str = timestamp_parts[0]
                sent_str = timestamp_parts[1].strip()
                
                # Convert strings to datetime objects
                received_time = datetime.strptime(received_str, '%Y-%m-%d %H:%M:%S.%f')
                sent_time = datetime.strptime(sent_str, '%Y-%m-%d %H:%M:%S.%f')
                
                # Calculate latency in milliseconds
                latency = (received_time - sent_time).total_seconds() * 1000
                
                if latency <= max_latency:
                    received_count += 1
                else:
                    delayed_count += 1

            except Exception as e:
                continue
    
    return received_count, delayed_count

def analyze_critical_messages(base_dirs):
    """Analyze critical messages across different configurations"""
    expected_total = 3000  # Total expected critical messages
    max_latency = 50      # Maximum latency for critical messages (ms)
    results = {}
    
    # Process each configuration directory
    for dir_path in base_dirs:
        config_name = os.path.basename(dir_path).replace('quic-manager-', '')
        type_path = os.path.join(dir_path, 'type-3')  # Critical messages are type-3
        
        if not os.path.exists(type_path):
            print(f"Warning: Directory {type_path} does not exist.")
            continue
        
        received_total = 0
        delayed_total = 0
        
        # Process each subscriber
        for sub_num in range(3):
            log_file = os.path.join(type_path, f'mqtt-quic-type-3-sub-{sub_num}.log')
            
            if os.path.exists(log_file):
                received, delayed = parse_log_file(log_file, max_latency)
                received_total += received
                delayed_total += delayed
        
        results[config_name] = {
            'received': received_total,
            'delayed': delayed_total,
            'lost': expected_total - received_total - delayed_total
        }
    
    return results

def create_comparison_graph(results, output_dir):
    """Create bar graph comparing critical messages across configurations"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare data
    configs = list(results.keys())
    
    # Create more descriptive labels
    config_labels = {
        '16-inflight': 'Inflight 16',
        '32-inflight': 'Inflight 32',
        '1000-queue': 'Fila 1000',
        '5000-queue': 'Fila 5000'
    }
    
    # Calculate percentages
    total = 3000  # Expected total
    percentages = {config: {
        'received': (data['received'] / total) * 100,
        'delayed': (data['delayed'] / total) * 100,
        'lost': (data['lost'] / total) * 100
    } for config, data in results.items()}
    
    # Create figure
    plt.figure(figsize=(12, 7))
    
    # Set the positions of the bars
    x = np.arange(len(configs))
    width = 0.35
    
    # Create stacked bars
    bottoms = np.zeros(len(configs))
    
    # Plot received (green)
    received = [percentages[config]['received'] for config in configs]
    plt.bar(x, received, width, label='No Prazo', 
           color='#2ecc71', edgecolor='black')
    
    # Plot delayed (yellow)
    delayed = [percentages[config]['delayed'] for config in configs]
    plt.bar(x, delayed, width, bottom=received,
           label='Atrasadas', color='#f1c40f', edgecolor='black')
    
    # Plot lost (red)
    lost = [percentages[config]['lost'] for config in configs]
    plt.bar(x, lost, width, bottom=[r + d for r, d in zip(received, delayed)],
           label='Perdidas', color='#e74c3c', edgecolor='black')
    
    # Customize the plot
    plt.xlabel('Configuração', fontsize=12, fontweight='bold')
    plt.ylabel('Porcentagem de Mensagens (%)', fontsize=12, fontweight='bold')
    plt.title('Comparação de Mensagens Críticas por Configuração', 
             fontsize=14, fontweight='bold', pad=20)
    
    # Set y-axis to show percentages from 0 to 100
    plt.ylim(0, 110)
    
    # Set x-axis labels using the descriptive config_labels
    plt.xticks(x, [config_labels[config] for config in configs], rotation=45, ha='right')
    
    # Add legend outside the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add percentage labels
    for i, config in enumerate(configs):
        # On-time messages (green)
        if percentages[config]['received'] > 5:
            plt.text(i, percentages[config]['received']/2, 
                    f"{percentages[config]['received']:.1f}%", 
                    ha='center', va='center', color='black', fontweight='bold')
        
        # Delayed messages (yellow)
        if percentages[config]['delayed'] > 5:
            plt.text(i, percentages[config]['received'] + percentages[config]['delayed']/2, 
                    f"{percentages[config]['delayed']:.1f}%", 
                    ha='center', va='center', color='black', fontweight='bold')
        
        # Lost messages (red)
        if percentages[config]['lost'] > 5:
            plt.text(i, percentages[config]['received'] + percentages[config]['delayed'] + 
                    percentages[config]['lost']/2, 
                    f"{percentages[config]['lost']:.1f}%", 
                    ha='center', va='center', color='white', fontweight='bold')
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'critical_messages_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved comparison graph to: {output_path}")
    plt.close()

if __name__ == "__main__":
    # List of configuration directories to compare
    base_dirs = [
        './data/quic-manager-16-inflight',
        './data/quic-manager-32-inflight',
        './data/quic-manager-1000-queue',
        './data/quic-manager-5000-queue'
    ]
    
    # Analyze and create comparison
    results = analyze_critical_messages(base_dirs)
    
    # Print results
    print("\nComparação de Mensagens Críticas:")
    print("=" * 80)
    print(f"{'Configuração':<20} {'No Prazo':<12} {'Atrasadas':<12} {'Perdidas':<12} {'Total':<12}")
    print("-" * 80)
    
    config_labels = {
        '16-inflight': 'Inflight 16',
        '32-inflight': 'Inflight 32',
        '1000-queue': 'Queue 1000',
        '5000-queue': 'Queue 5000'
    }
    
    for config, data in results.items():
        print(f"{config_labels[config]:<20} {data['received']:<12} {data['delayed']:<12} "
              f"{data['lost']:<12} {3000:<12}")
    
    print("=" * 80)
    
    # Create comparison graph
    create_comparison_graph(results, './data/graphs')
