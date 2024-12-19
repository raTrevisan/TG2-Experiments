./experiment_start.sh quic 10 1 1
sleep 3600
./logs.sh quic-10-1-manager-queue_10x1-1000
sleep 30
./experiment_end.sh

sleep 600

./experiment_start.sh quic 20 1 2
sleep 3600
./logs.sh quic-20-1-manager-queue_10x1-1000
sleep 30
./experiment_end.sh

sleep 600

./experiment_start.sh quic 30 1 3
sleep 3600
./logs.sh quic-30-1-manager-queue_10x1-1000
sleep 30
./experiment_end.sh

sleep 600

./experiment_start.sh quic 40 1 4
sleep 3600
./logs.sh quic-30-1-manager-queue_10x1-1000
sleep 30
./experiment_end.sh
