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
                print(f"Warning: Could not parse line in {filename}")
                continue
    
    return received_count, delayed_count

def create_loss_bar_graph(message_counts, delayed_counts, expected_totals, labels, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Creating graph in directory: {output_dir}")
    
    # Prepare data for plotting
    types = list(labels.values())
    
    # Calculate percentages including delayed as lost
    percentages_received = [(message_counts[i] / expected_totals[i]) * 100 for i in range(1, 6)]
    percentages_delayed = [(delayed_counts[i] / expected_totals[i]) * 100 for i in range(1, 6)]
    percentages_lost = [100 - p - d for p, d in zip(percentages_received, percentages_delayed)]
    
    # Create figure and axis with larger size and extra space for legend
    plt.figure(figsize=(14, 7))
    
    # Set the positions of the bars
    x = np.arange(len(types))
    width = 0.35
    
    # Create stacked bars
    plt.bar(x, percentages_received, width, label='No Prazo', 
           color='#2ecc71', edgecolor='black')  # Green
    plt.bar(x, percentages_delayed, width, bottom=percentages_received, 
           label='Atrasadas', color='#f1c40f', edgecolor='black')  # Yellow
    plt.bar(x, percentages_lost, width, 
           bottom=[r + d for r, d in zip(percentages_received, percentages_delayed)],
           label='Perdidas', color='#e74c3c', edgecolor='black')  # Red
    
    # Customize the plot
    plt.xlabel('Tipos de Mensagem', fontsize=12, fontweight='bold')
    plt.ylabel('Porcentagem de Mensagens (%)', fontsize=12, fontweight='bold')
    plt.title('Distribuição de Mensagens por Tipo - 5000 fila', 
             fontsize=14, fontweight='bold', pad=20)
    
    # Set y-axis to show percentages from 0 to 100
    plt.ylim(0, 110)
    
    # Rotate x-axis labels for better readability
    plt.xticks(x, types, rotation=45, ha='right')
    
    # Add legend outside the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add percentage labels
    for i in range(len(types)):
        # On-time messages (green)
        if percentages_received[i] > 5:
            plt.text(i, percentages_received[i]/2, 
                    f'{percentages_received[i]:.1f}%', 
                    ha='center', va='center', color='black', fontweight='bold')
        
        # Delayed messages (yellow)
        if percentages_delayed[i] > 5:
            plt.text(i, percentages_received[i] + percentages_delayed[i]/2, 
                    f'{percentages_delayed[i]:.1f}%', 
                    ha='center', va='center', color='black', fontweight='bold')
        
        # Lost messages (red)
        if percentages_lost[i] > 5:
            plt.text(i, percentages_received[i] + percentages_delayed[i] + percentages_lost[i]/2, 
                    f'{percentages_lost[i]:.1f}%', 
                    ha='center', va='center', color='white', fontweight='bold')
    
    plt.subplots_adjust(top=0.9)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'message_loss_distribution.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved graph to: {output_path}")
    plt.close()

def count_messages_by_type(base_dir):
    # Expected totals for each type
    expected_totals = {
        1: 30000,  # IoT Industrial
        2: 6000,   # Automação de Processos
        3: 3000,   # Mensagens Críticas
        4: 30000,  # Realidade Aumentada
        5: 30000   # Dados de Câmeras
    }
    
    # Maximum latency for each type (in ms)
    max_latencies = {
        1: 200,    # IoT Industrial
        2: 500,    # Automação de Processos
        3: 50,     # Mensagens Críticas
        4: 20,     # Realidade Aumentada
        5: 100     # Dados de Câmeras
    }
    
    # Dictionaries to store message counts
    message_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}  # Within latency threshold
    delayed_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}  # Beyond latency threshold
    
    labels = {
        1: 'IoT Industrial',
        2: 'Automação de Processos',
        3: 'Mensagens Críticas',
        4: 'Realidade Aumentada',
        5: 'Dados de Câmeras'
    }
    
    # Process each type
    for type_num in range(1, 6):
        type_dir = f'type-{type_num}'
        type_path = os.path.join(base_dir, type_dir)
        
        if not os.path.exists(type_path):
            print(f"Warning: Directory {type_path} does not exist.")
            continue
            
        for sub_num in range(3):
            log_file = os.path.join(type_path, f'mqtt-quic-{type_dir}-sub-{sub_num}.log')
            
            if os.path.exists(log_file):
                received, delayed = parse_log_file(log_file, max_latencies[type_num])
                message_counts[type_num] += received
                delayed_counts[type_num] += delayed
    
    # Print results
    print("\nRelatório de Mensagens:")
    print("=" * 80)
    print(f"{'Tipo':<25} {'No Prazo':<12} {'Atrasadas':<12} {'Perdidas':<12} {'Esperadas':<12}")
    print("-" * 80)
    
    for type_num in range(1, 6):
        received = message_counts[type_num]
        delayed = delayed_counts[type_num]
        expected = expected_totals[type_num]
        lost = expected - received - delayed
        
        print(f"{labels[type_num]:<25} {received:<12} {delayed:<12} {lost:<12} {expected:<12}")
    
    print("=" * 80)
    
    # Create and save the bar graph
    output_dir = os.path.join('data', 'graphs', '5000-queue')
    create_loss_bar_graph(message_counts, delayed_counts, expected_totals, labels, output_dir)

if __name__ == "__main__":
    base_dir = os.path.join('data', 'quic-manager-5000-queue')
    count_messages_by_type(base_dir)
