#bin/bash!

kubectl scale --replicas=0 statefulset/emqx -n dtwins
#kubectl scale --replicas=0 deployments/cluster-manager -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-1-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-2-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-3-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-4-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-5-sub -n dtwins

kubectl scale --replicas=0 statefulset/mqtt-quic-type-1-pub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-2-pub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-3-pub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-4-pub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-type-5-pub -n dtwins

kubectl scale --replicas=0 statefulset/mqtt-tcp-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-tcp-pub -n dtwins

kubectl scale --replicas=0 statefulset/mqtt-quic-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-pub -n dtwins
kubectl scale --replicas=0 statefulset/cluster-manager -n dtwins


for type in 1 2 3 4 5
do
    for num in 0 1 2 3 4 5 6 7 8 9 10 
    do 
    kubectl delete pod -n dtwins mqtt-quic-type-${type}-pub-${num} --force 
    kubectl delete pod -n dtwins mqtt-quic-type-${type}-sub-${num} --force 
    done
    cd ..
done
