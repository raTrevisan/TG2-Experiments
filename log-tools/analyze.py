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

def analyze_performance():
    # Read the data
    tcp_times = read_history_file('./data/tcp-test/tcp_hf.log')
    quic_times = read_history_file('./data/quic-test/quic_hf.log')

    # Calculate total time for each protocol
    tcp_total = tcp_times[-1] - tcp_times[0]
    quic_total = quic_times[-1] - quic_times[0]

    # Calculate average message delivery time
    tcp_avg = np.mean(np.diff(tcp_times))
    quic_avg = np.mean(np.diff(quic_times))

    # Calculate percentage improvement
    time_improvement = ((tcp_total - quic_total) / tcp_total) * 100
    avg_improvement = ((tcp_avg - quic_avg) / tcp_avg) * 100

    print(f"\nPerformance Analysis:")
    print(f"Total time taken:")
    print(f"TCP:  {tcp_total:.3f} seconds")
    print(f"QUIC: {quic_total:.3f} seconds")
    print(f"\nAverage time between messages:")
    print(f"TCP:  {tcp_avg:.3f} seconds")
    print(f"QUIC: {quic_avg:.3f} seconds")
    print(f"\nQUIC is {time_improvement:.1f}% faster in total time")
    print(f"QUIC is {avg_improvement:.1f}% faster in average message delivery")

if __name__ == "__main__":
    analyze_performance() 