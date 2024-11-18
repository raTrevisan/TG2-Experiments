
cd ./data/raw
for type in tcp quic
do
    for num in 0 1 2 3 4 5 6 7 8 9
    do 
    kubectl logs -n dtwins mqtt-${type}-${num} > ${type}/mqtt-${type}-${num}.log
    done
done
