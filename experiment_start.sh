#bin/bash!
echo "Scaling Broker..."
kubectl scale --replicas=$2 statefulset/emqx -n dtwins
sleep 80

#kubectl scale --replicas=0 deployments/cluster-manager -n dtwins
#sleep 60

echo "Scaling Subscribers..."
kubectl scale --replicas=$1 statefulset/mqtt-quic-sub -n dtwins
sleep 60

echo "Scaling Clients..."
kubectl scale --replicas=$3 statefulset/mqtt-quic-pub -n dtwins
echo "Done"
