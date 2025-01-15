import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from datetime import datetime
import seaborn as sns
from tqdm import tqdm  # Import tqdm for progress meter

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

def create_graphs():
    # Set style using seaborn
    sns.set_style("whitegrid")
    
    # Define colors with labels
    type_order = [3, 4, 2, 1, 5]  # Critical, AR, Process Auto, Industrial IoT
    colors = ['#e74c3c', '#9b59b6', '#3498db', '#2ecc71', '#f1c40f']  # Added fifth color
    labels = {
        1: 'IoT Industrial',
        2: 'Automação de Processos',
        3: 'Mensagens Cíticas',
        4: 'Realidade Aumentada',
        5: 'Dados de Câmeras'
    }

    # Base directory for the logs
    base_dir = './data/quic-manager-5000-queue'
    
    # Create output directory
    output_dir = './data/graphs'
    os.makedirs(output_dir, exist_ok=True)

    # Collect latencies and labels only for existing data
    all_latencies = []
    type_labels = []
    valid_colors = []
    
    # Process each type in the specified order
    for type_num in type_order:
        type_dir = f'type-{type_num}'
        type_path = os.path.join(base_dir, type_dir)
        
        if not os.path.exists(type_path):
            continue
            
        log_files = glob.glob(os.path.join(type_path, f'mqtt-quic-{type_dir}-sub-*.log'))
        log_files.sort()
        
        if not log_files:
            continue

        # Collect latencies from all files for this type
        type_latencies = []
        
        # Add progress meter for log file processing
        for file in tqdm(log_files, desc=f'Processing type {type_num}', unit='file'):
            _, latencies = parse_log_file(file)
            if len(latencies) > 0:
                type_latencies.extend(latencies)

        if type_latencies:
            all_latencies.append(type_latencies)
            type_labels.append(labels[type_num])
            valid_colors.append(colors[type_order.index(type_num)])

    # Create figure with white background
    plt.figure(figsize=(10, 6), facecolor='white')
    
    # Create boxplot with only the valid data
    bp = plt.boxplot(all_latencies, 
                    labels=type_labels,
                    showfliers=False,
                    patch_artist=True,
                    medianprops=dict(color="black", linewidth=1.5),
                    boxprops=dict(alpha=0.7))

    # Color the boxes using only valid colors
    for box, color in zip(bp['boxes'], valid_colors):
        box.set_facecolor(color)
        box.set_edgecolor('black')
        box.set_linewidth(1.5)

    # Style the whiskers and caps
    for whisker in bp['whiskers']:
        whisker.set_color('black')
        whisker.set_linewidth(1.5)
    
    for cap in bp['caps']:
        cap.set_color('black')
        cap.set_linewidth(1.5)

    # Customize the plot
    plt.ylabel('Latencia (ms)', fontsize=12, fontweight='bold')
    plt.xlabel('Tipo de Serviço', fontsize=12, fontweight='bold')
    plt.title('Escalando com fila em 5000', fontsize=14, fontweight='bold', pad=20)
    
    # Customize grid
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Add some padding to y-axis
    plt.margins(y=0.1)
    
    # Customize ticks
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10)
    
    # Set y-axis limit
    plt.ylim(0, 500)
    
    # Customize grid with appropriate steps
    plt.yticks(np.arange(0, 501, 100))  # Create ticks every 100ms up to 1500
    
    # Save the plot with tight layout and high DPI
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'quic_5000q_boxplot.png'), 
                dpi=300, 
                bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_graphs()
