#bin/bash!

kubectl scale --replicas=0 statefulset/emqx -n dtwins
kubectl scale --replicas=0 deployments/cluster-manager -n dtwins
kubectl scale --replicas=0 statefulset/twin-ncv2x-stateful -n dtwins
kubectl scale --replicas=0 statefulset/twin-dab-stateful -n dtwins
kubectl scale --replicas=0 statefulset/twin-das-stateful -n dtwins
kubectl scale --replicas=0 statefulset/twin-mc-stateful -n dtwins
kubectl scale --replicas=0 statefulset/twin-v2x-stateful -n dtwins
kubectl scale --replicas=0 statefulset/client-ncv2x-stateful -n dtwins
kubectl scale --replicas=0 statefulset/client-dab-stateful -n dtwins
kubectl scale --replicas=0 statefulset/client-das-stateful -n dtwins
kubectl scale --replicas=0 statefulset/client-mc-stateful -n dtwins
kubectl scale --replicas=0 statefulset/client-v2x-stateful -n dtwins
