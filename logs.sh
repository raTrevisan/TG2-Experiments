
cd ./data
mkdir $1
cd $1
mkdir raw
cd raw
mkdir tcp
mkdir quic
for type in tcp quic
do
    for num in 0 1 2 3 4 5 6 7 8 9
    do 
    kubectl logs -n dtwins mqtt-${type}-sub-${num} > ${type}/mqtt-${type}-${num}.log
    done
done
