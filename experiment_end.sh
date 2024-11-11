#bin/bash!

kubectl scale --replicas=0 statefulset/emqx -n dtwins
#kubectl scale --replicas=0 deployments/cluster-manager -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-pub -n dtwins
