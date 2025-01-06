#!/bin/bash

# Start subscriber for client type 1
echo "Starting subscriber for client type 1..."
kubectl scale --replicas=1 statefulset/mqtt-quic-type-1-sub -n dtwins
kubectl scale --replicas=1 statefulset/mqtt-quic-type-2-sub -n dtwins
kubectl scale --replicas=1 statefulset/mqtt-quic-type-3-sub -n dtwins
kubectl scale --replicas=1 statefulset/mqtt-quic-type-4-sub -n dtwins
kubectl scale --replicas=1 statefulset/mqtt-quic-type-5-sub -n dtwins
25

# Start publishers for client type 1
for i in {0..9}; do
    echo "Starting publisher $((1 + i)) for client type 1..."
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-1-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-2-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-3-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-4-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-5-pub -n dtwins
    sleep 25  # Wait for 1 second before starting the next publisher
done


# Start subscriber for sub 2
echo "Starting subscriber for client type 1..."
kubectl scale --replicas=2 statefulset/mqtt-quic-type-1-sub -n dtwins
kubectl scale --replicas=2 statefulset/mqtt-quic-type-2-sub -n dtwins
kubectl scale --replicas=2 statefulset/mqtt-quic-type-3-sub -n dtwins
kubectl scale --replicas=2 statefulset/mqtt-quic-type-4-sub -n dtwins
kubectl scale --replicas=2 statefulset/mqtt-quic-type-5-sub -n dtwins
25

# Start publishers for pub 2
for i in {10..19}; do
    echo "Starting publisher $((1 + i)) for client type 1..."
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-1-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-2-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-3-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-4-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-5-pub -n dtwins
    sleep 25  # Wait for 1 second before starting the next publisher
done


# Start subscriber for client type 1
echo "Starting subscriber for client copy 3..."
kubectl scale --replicas=3 statefulset/mqtt-quic-type-1-sub -n dtwins
kubectl scale --replicas=3 statefulset/mqtt-quic-type-2-sub -n dtwins
kubectl scale --replicas=3 statefulset/mqtt-quic-type-3-sub -n dtwins
kubectl scale --replicas=3 statefulset/mqtt-quic-type-4-sub -n dtwins
kubectl scale --replicas=3 statefulset/mqtt-quic-type-5-sub -n dtwins
25

# Start publishers for client type 1
for i in {20..29}; do
    echo "Starting publisher $((1 + i)) for client type 1..."
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-1-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-2-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-3-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-4-pub -n dtwins
    kubectl scale --replicas=$i statefulset/mqtt-quic-type-5-pub -n dtwins
    sleep 25  # Wait for 1 second before starting the next publisher
done
