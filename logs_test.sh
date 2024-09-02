
mkdir logs_$1
cd logs_$1
mkdir mc 
mkdir well

for type in mc well
do

    for num in 0 1 2 3 4
    do 
    kubectl logs -n dtwins twin-${type}-stateful-${num} > ${type}/twin-${type}-stateful-${num}.log
    done
    
done
