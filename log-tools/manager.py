import matplotlib.pyplot as plt
from collections import deque
import time
from datetime import datetime

def init_metrics_tracking():
    # Keep last 100 data points
    return {
        'timestamps': deque(maxlen=100),
        'queue_avg': deque(maxlen=100),
        'inflight_avg': deque(maxlen=100)
    }

def update_graph(metrics_data, queue_avg, inflight_avg):
    metrics_data['timestamps'].append(datetime.now())
    metrics_data['queue_avg'].append(queue_avg)
    metrics_data['inflight_avg'].append(inflight_avg)
    
    # Create the graph
    plt.clf()  # Clear the current figure
    plt.figure(figsize=(10, 6))
    
    # Plot both metrics
    plt.plot(list(metrics_data['timestamps']), list(metrics_data['queue_avg']), label='Queue Avg')
    plt.plot(list(metrics_data['timestamps']), list(metrics_data['inflight_avg']), label='Inflight Avg')
    
    # Customize the graph
    plt.title('Queue and Inflight Metrics Over Time')
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Save the graph
    plt.savefig('metrics_graph.png', bbox_inches='tight')
    plt.close()

def main():
    # ... existing initialization code ...
    
    metrics_data = init_metrics_tracking()
    
    while True:
        try:
            response_clients = call_api_clients(...)
            response_nodes = call_api_nodes(...)
            
            if response_clients.status_code == 200 and response_nodes.status_code == 200:
                metrics = response_clients.json()
                nodes = response_nodes.json()
                
                # Calculate averages
                queue_total = sum(metric.get("mqueue_len", 0) for metric in metrics["data"])
                inflight_total = sum(metric.get("inflight_cnt", 0) for metric in metrics["data"])
                node_count = len(nodes)
                
                if node_count > 0:
                    queue_avg = queue_total/node_count
                    inflight_avg = inflight_total/node_count
                    
                    # Update and save the graph
                    update_graph(metrics_data, queue_avg, inflight_avg)
                
                # ... rest of the existing code ...