#bin/bash!

kubectl scale --replicas=0 statefulset/emqx -n dtwins
#kubectl scale --replicas=0 deployments/cluster-manager -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-1-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-2-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-3-sub -n dtwins

kubectl scale --replicas=0 statefulset/mqtt-quic-type-1-pub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-2-pub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-3-pub -n dtwins

kubectl scale --replicas=0 statefulset/mqtt-tcp-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-tcp-pub -n dtwins
