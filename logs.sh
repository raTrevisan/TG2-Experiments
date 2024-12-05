
cd ./data
mkdir $1
cd $1
mkdir quic
for type in 1 2 3
do
    mkdir type-${type}
    cd type-${type}
    for num in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29
    do 
    kubectl logs -n dtwins mqtt-quic-type-${type}-sub-${num} > mqtt-quic-type-${type}-sub-${num}.log
    done
    cd ..
done
