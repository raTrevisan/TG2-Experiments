#bin/bash!
kubectl scale --replicas=$2 statefulset/emqx -n dtwins

sleep 80

kubectl scale --replicas=1 deployments/cluster-manager -n dtwins

sleep 60

kubectl scale --replicas=$1 statefulset/twin-ncv2x-stateful -n dtwins
kubectl scale --replicas=$1 statefulset/twin-dab-stateful -n dtwins
kubectl scale --replicas=$1 statefulset/twin-das-stateful -n dtwins
kubectl scale --replicas=$1 statefulset/twin-mc-stateful -n dtwins
kubectl scale --replicas=$1 statefulset/twin-v2x-stateful -n dtwins

sleep 60

kubectl scale --replicas=$1 statefulset/client-ncv2x-stateful -n dtwins
kubectl scale --replicas=$1 statefulset/client-dab-stateful -n dtwins
kubectl scale --replicas=$1 statefulset/client-das-stateful -n dtwins
kubectl scale --replicas=$1 statefulset/client-mc-stateful -n dtwins
kubectl scale --replicas=$1 statefulset/client-v2x-stateful -n dtwins
