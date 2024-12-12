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

kubectl scale --replicas=0 statefulset/mqtt-quic-sub -n dtwins
kubectl scale --replicas=0 statefulset/mqtt-quic-pub -n dtwins
kubectl scale --replicas=0 statefulset/cluster-manager -n dtwins


cd ./data
mkdir $1
cd $1
for type in 1 2 3
do
    mkdir type-${type}
    cd type-${type}
    for num in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49
    do 
    kubectl delete pod -n dtwins mqtt-quic-type-${type}-pub-${num} --force
    kubectl delete pod -n dtwins mqtt-quic-type-${type}-sub-${num} --force
    done
    cd ..
done
