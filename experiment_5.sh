#bin/bash!
mkdir $1
cd $1

for num in 1 2 3 4 5
do 
../experiment_start.sh 15 1
sleep 2100
mkdir ${num}
cd ${num}
../../logs.sh log-${num}
../../experiment_end.sh
cd ..
sleep 600
done 
