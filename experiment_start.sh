#bin/bash!
echo "Scaling Broker..."
kubectl scale --replicas=$3 statefulset/emqx -n dtwins

sleep 60

kubectl scale --replicas=1 statefulset/cluster-manager -n dtwins
#sleep 60

#!/bin/bash

# Check if the first argument is "tcp"
if [ "$1" == "tcp" ]; then
    echo "Using TCP:"
    echo "Scaling Subscribers..."
    kubectl scale --replicas=$2 statefulset/mqtt-tcp-sub -n dtwins
    #kubectl scale --replicas=$1 statefulset/mqtt-tcp-type-1-sub -n dtwins
    #kubectl scale --replicas=$1 statefulset/mqtt-tcp-type-2-sub -n dtwins
    #kubectl scale --replicas=$1 statefulset/mqtt-tcp-type-3-sub -n dtwins
    sleep 60

    echo "Scaling Clients..."
    kubectl scale --replicas=$2 statefulset/mqtt-tcp-pub -n dtwins
    #kubectl scale --replicas=$3 statefulset/mqtt-tcp-type-1-pub -n dtwins
    #kubectl scale --replicas=$3 statefulset/mqtt-tcp-type-2-pub -n dtwins
    #kubectl scale --replicas=$3 statefulset/mqtt-tcp-type-3-pub -n dtwins
    echo "Done"
fi


if [ "$1" == "quic" ]; then
    echo "Using QUIC"
    echo "Scaling Subscribers..."
    #kubectl scale --replicas=$2 statefulset/mqtt-quic-sub -n dtwins
    kubectl scale --replicas=$2 statefulset/mqtt-quic-type-1-sub -n dtwins
    kubectl scale --replicas=$2 statefulset/mqtt-quic-type-2-sub -n dtwins
    kubectl scale --replicas=$2 statefulset/mqtt-quic-type-3-sub -n dtwins
    sleep 60

    echo "Scaling Clients..."
    #kubectl scale --replicas=$2 statefulset/mqtt-quic-pub -n dtwins
    kubectl scale --replicas=$2 statefulset/mqtt-quic-type-1-pub -n dtwins
    kubectl scale --replicas=$2 statefulset/mqtt-quic-type-2-pub -n dtwins
    kubectl scale --replicas=$2 statefulset/mqtt-quic-type-3-pub -n dtwins
    echo "Done"
fi
