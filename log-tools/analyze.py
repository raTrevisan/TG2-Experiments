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
    tcp_times = read_history_file('./data/tcp_hf.log')
    quic_times = read_history_file('./data/quic_hf.log')

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
    print(f"\nMessage Counts:")
    print(f"TCP:  {len(tcp_times)} messages")
    print(f"QUIC: {len(quic_times)} messages")
    
    print(f"\nTotal time taken:")
    print(f"TCP:  {tcp_total:.3f} seconds ({tcp_total/len(tcp_times):.3f} sec/msg)")
    print(f"QUIC: {quic_total:.3f} seconds ({quic_total/len(quic_times):.3f} sec/msg)")
    
    print(f"\nAverage time between messages:")
    print(f"TCP:  {tcp_avg:.3f} seconds")
    print(f"QUIC: {quic_avg:.3f} seconds")
    
    print(f"\nPerformance Improvements:")
    print(f"QUIC is {time_improvement:.1f}% faster in total time")
    print(f"QUIC is {avg_improvement:.1f}% faster in average message delivery")
    
    # Message rate analysis
    tcp_rate = len(tcp_times) / tcp_total
    quic_rate = len(quic_times) / quic_total
    rate_improvement = ((quic_rate - tcp_rate) / tcp_rate) * 100
    
    print(f"\nMessage Rates:")
    print(f"TCP:  {tcp_rate:.1f} messages/second")
    print(f"QUIC: {quic_rate:.1f} messages/second")
    print(f"QUIC processes {rate_improvement:.1f}% more messages per second")

if __name__ == "__main__":
    analyze_performance() 