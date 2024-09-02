
mkdir logs_$1
cd logs_$1
mkdir logs_$1/mc 
mkdir logs_$1/v2x

for type in mc v2x
do

    for num in 0 1 2 3 4 5 6 7 8 9 10
    do 
    kubectl logs -n dtwins twin-${type}-stateful-${num} > ${type}/twin-${type}-stateful-${num}.log
    done
    python3 ../main.py
    
done
