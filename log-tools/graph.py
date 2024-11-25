import matplotlib.pyplot as plt
import numpy as np

def read_history_file(filename):
    times = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                times.append(float(line.strip()))
            except ValueError:
                continue
    return np.array(times)

import matplotlib.pyplot as plt
import numpy as np

def read_history_file(filename):
    times = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                times.append(float(line.strip()))
            except ValueError:
                continue
    return np.array(times)

def create_graph():
    # Read only the relevant data files
    tcp_times = read_history_file('./data/tcp-big-tcp_hf.log')
    quic_times = read_history_file('./data/quic-big-quic_hf.log')

    # Create message indices (x-axis)
    tcp_indices = np.arange(len(tcp_times))
    quic_indices = np.arange(len(quic_times))

    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Plot lines
    plt.plot(tcp_indices, tcp_times, 'b-', label='TCP', alpha=0.7)
    plt.plot(quic_indices, quic_times, 'r-', label='QUIC', alpha=0.7)

    # Customize the plot
    plt.xlabel('Message Number')
    plt.ylabel('Time (seconds)')
    plt.title('TCP vs QUIC Performance Comparison')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Save the plot
    plt.savefig('./data/comparison_graph.png')
    plt.close()

if __name__ == "__main__":
    create_graph()