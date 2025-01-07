
cd ./data
mkdir $1
cd $1
for type in 1 2 3 4 5
do
    mkdir type-${type}
    cd type-${type}
    for num in 0 1 2
    do 
    kubectl logs -n dtwins mqtt-quic-type-${type}-sub-${num} > mqtt-quic-type-${type}-sub-${num}.log
    done
    cd ..
done
kubectl logs -n dtwins cluster-manager-0 > cluster-manager.log
