import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from datetime import datetime
import seaborn as sns
from tqdm import tqdm

def parse_log_file(filename):
    latencies = []
    
    with open(filename, 'r') as f:
        for line in f:
            if 'Message received' not in line:
                continue
                
            try:
                # Split the line by 'at' and 'sent' to get the timestamps
                parts = line.split(' at ')
                if len(parts) != 2:
                    continue
                    
                # Get the topic part
                topic_part = parts[0].split('topic: ')[1].split(' with')[0]  # e.g., 'type-2/0'
                message_type = int(topic_part.split('-')[1].split('/')[0])  # Get the type number (2)
                
                # Get timestamps
                timestamp_parts = parts[1].split(' sent ')
                received_str = timestamp_parts[0]
                sent_str = timestamp_parts[1].strip()
                
                # Try parsing with microseconds first, then without if it fails
                try:
                    received_time = datetime.strptime(received_str, '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    # If no microseconds, add .000000
                    received_time = datetime.strptime(received_str + '.000000', '%Y-%m-%d %H:%M:%S.%f')
                
                try:
                    sent_time = datetime.strptime(sent_str, '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    # If no microseconds, add .000000
                    sent_time = datetime.strptime(sent_str + '.000000', '%Y-%m-%d %H:%M:%S.%f')
                
                # Calculate latency in milliseconds
                latency = (received_time - sent_time).total_seconds() * 1000
                latencies.append((message_type, latency))  # Store tuple of (type, latency)

            except Exception as e:
                print(f"Warning: Could not parse line in {filename}")
                print(f"Line: {line.strip()}")
                print(f"Error: {str(e)}")
                continue
                
    return latencies

def calculate_statistics(latencies):
    """Calculate various statistics for the latencies."""
    if not latencies:
        return None
    
    stats = {
        'count': len(latencies),
        'mean': np.mean(latencies),
        'median': np.median(latencies),
        'std': np.std(latencies),
        'min': np.min(latencies),
        'max': np.max(latencies),
        'p95': np.percentile(latencies, 95),
        'p99': np.percentile(latencies, 99)
    }
    return stats

def plot_histogram_with_stats(data, bins, color, label, ax, is_critical=False):
    """Plot histogram with statistical markers."""
    stats = calculate_statistics(data)
    if not stats:
        return None
    
    # Plot the histogram with weights to scale the y-axis and fixed number of bins
    weights = np.ones_like(data) * (100.0/len(data))  # This will make the total area = 100
    n, bins, patches = ax.hist(data, bins=50, color=color, alpha=0.7,  # Fixed 50 bins
                              weights=weights,
                              label=label,
                              edgecolor='black', linewidth=1)
    
    # Set y-axis limit to 50%
    ax.set_ylim(0, 50)
    
    # Line style based on whether it's critical messages
    line_style = '-' if is_critical else '--'
    
    # Add vertical lines for statistics with Portuguese labels
    ax.axvline(stats['mean'], color='red', linestyle=line_style, alpha=0.8, 
               label=f"Média: {stats['mean']:.2f}ms")
    ax.axvline(stats['median'], color='green', linestyle=line_style, alpha=0.8, 
               label=f"Mediana: {stats['median']:.2f}ms")
    ax.axvline(stats['p95'], color='purple', linestyle=line_style, alpha=0.8, 
               label=f"Percentil 95: {stats['p95']:.2f}ms")
    ax.axvline(stats['p99'], color='orange', linestyle=line_style, alpha=0.8, 
               label=f"Percentil 99: {stats['p99']:.2f}ms")
    
    # Add 50ms threshold line for all histograms
    ax.axvline(50, color='black', linestyle=':', alpha=0.8, linewidth=2,
               label="Limite Crítico: 50ms")
    
    # Update y-axis label to reflect percentage
    ax.set_ylabel('Frequência (%)', fontsize=12, fontweight='bold')
    
    return stats

def create_histograms():
    sns.set_style("whitegrid")
    base_dir = './data/quic-manager-16-inflight'
    output_dir = './data/graphs/16i'
    os.makedirs(output_dir, exist_ok=True)

    x_min = 0
    x_max = 500
    n_bins = 50
    bin_edges = np.linspace(x_min, x_max, n_bins + 1)
    
    colors = ['#e74c3c', '#9b59b6', '#3498db', '#2ecc71', '#f1c40f']
    labels = {
        1: 'IoT Industrial',
        2: 'Automação de Processos',
        3: 'Mensagens Críticas',
        4: 'Realidade Aumentada',
        5: 'Dados de Câmeras'
    }

    all_latencies = {1: [], 2: [], 3: [], 4: [], 5: []}
    all_stats = {}

    # Process each type
    for type_num in range(1, 6):
        type_dir = f'type-{type_num}'
        type_path = os.path.join(base_dir, type_dir)
        
        if not os.path.exists(type_path):
            print(f"Warning: Directory {type_path} does not exist.")
            continue
            
        for sub_num in range(3):
            log_file_pattern = os.path.join(type_path, f'mqtt-quic-{type_dir}-sub-{sub_num}.log')
            log_files = glob.glob(log_file_pattern)
            
            for file in tqdm(log_files, desc=f'Processing {labels[type_num]} sub-{sub_num}', unit='file'):
                latencies = parse_log_file(file)
                for message_type, latency in latencies:
                    if message_type in all_latencies:
                        all_latencies[message_type].append(latency)

        # Create individual histograms for each type
        if all_latencies[type_num]:
            fig, ax = plt.subplots(figsize=(12, 7))
            
            # Create the label based on the type
            if type_num == 3:
                type_label = 'Mensagens Críticas'
            else:
                type_label = f'Tipo {type_num}'
            
            # Plot histogram with statistics using fixed bins
            stats = plot_histogram_with_stats(all_latencies[type_num], 
                                           bins=50,
                                           color='#3498db', 
                                           label=type_label,
                                           ax=ax,
                                           is_critical=(type_num == 3))
            
            plt.xlabel('Latência (ms)', fontsize=12, fontweight='bold')
            plt.title(f'Distribuição de Latência - {labels[type_num]}', 
                     fontsize=14, fontweight='bold')
            plt.legend(title='Estatísticas', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Save the plot
            plt.savefig(os.path.join(output_dir, f'quic_latency_distribution_type_{type_num}.png'), 
                       dpi=300, bbox_inches='tight')
            plt.close()

    # Create combined histogram comparing Type 3 vs Others
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Combine latencies for types 1, 2, 4, and 5
    other_types_latencies = []
    for type_num in [1, 2, 4, 5]:
        other_types_latencies.extend(all_latencies[type_num])
    
    # Plot Type 3 and combined others
    stats_others = None
    stats_type3 = None
    
    if other_types_latencies:
        stats_others = plot_histogram_with_stats(other_types_latencies, bin_edges, 
                                               '#a8a8a8', 'Outros Tipos', ax, 
                                               is_critical=False)
    if all_latencies[3]:
        stats_type3 = plot_histogram_with_stats(all_latencies[3], bin_edges, 
                                              '#e31a1c', 'Mensagens Críticas', ax, 
                                              is_critical=True)

    plt.xlabel('Latência (ms)', fontsize=12, fontweight='bold')
    plt.ylabel('Frequência', fontsize=12, fontweight='bold')
    plt.title('Distribuição de Latência - Mensagens Críticas vs Outros (Inflight 16)', fontsize=14, fontweight='bold')
    plt.legend(title='Tipos de Mensagem', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'quic_latency_distribution_combined_comparison.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

    # Print comparison statistics with Portuguese headers
    print("\nEstatísticas de Comparação (em milissegundos):")
    print("=" * 80)
    print(f"{'Tipo':<15} {'Total':<10} {'Média':<10} {'Mediana':<10} {'DesvPad':<10} {'Mín':<10} {'Máx':<10} {'Perc.95':<10} {'Perc.99':<10}")
    print("-" * 80)
    if stats_type3:
        print(f"{'Mens.Críticas':<15} {stats_type3['count']:<10.0f} {stats_type3['mean']:<10.2f} {stats_type3['median']:<10.2f} "
              f"{stats_type3['std']:<10.2f} {stats_type3['min']:<10.2f} {stats_type3['max']:<10.2f} {stats_type3['p95']:<10.2f} "
              f"{stats_type3['p99']:<10.2f}")
    if stats_others:
        print(f"{'Outros Tipos':<15} {stats_others['count']:<10.0f} {stats_others['mean']:<10.2f} {stats_others['median']:<10.2f} "
              f"{stats_others['std']:<10.2f} {stats_others['min']:<10.2f} {stats_others['max']:<10.2f} {stats_others['p95']:<10.2f} "
              f"{stats_others['p99']:<10.2f}")
    print("=" * 80)

if __name__ == "__main__":
    create_histograms()