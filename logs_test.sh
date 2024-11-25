
cd raw
mkdir logs_$1
cd logs_$1

for num in 0 1 2 3 4 5 6 7 8 9 10
do 
kubectl logs -n dtwins mqtt-quic-sub-${num} > ./twin-${type}-stateful-${num}.log
done
