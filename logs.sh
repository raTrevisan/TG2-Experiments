
cd ./data
mkdir $1
cd $1
mkdir quic
for type in 1 2 3
do
    for num in 0 1 2 3 4 5 6 7 8 9
    do 
    kubectl logs -n dtwins mqtt-quic-type-${type}-sub-${num} > type-${type}/mqtt-quic-type-${type}-sub-${num}.log
    done
done
