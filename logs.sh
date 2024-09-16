
mkdir logs_$1
cd logs_$1
mkdir raw
cd raw
mkdir mc 
mkdir dab
mkdir das
mkdir well


for type in mc dab das well
do

    for num in 0 1 2 3 4 
    do 
    kubectl logs -n dtwins twin-${type}-stateful-${num} > ${type}/twin-${type}-stateful-${num}.log
    done
done
