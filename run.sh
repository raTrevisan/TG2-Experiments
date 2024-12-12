./experiment_start.sh quic 10 1
sleep 3600
./logs.sh quic-10-1-manager-queue
sleep 30
./experiment_end.sh

sleep 600

./experiment_start.sh quic 20 1
sleep 3600
./logs.sh quic-20-1-manager-queue
sleep 30
./experiment_end.sh

sleep 600

./experiment_start.sh quic 30 1
sleep 3600
./logs.sh quic-30-1-manager-queue
sleep 30
./experiment_end.sh

sleep 600

./experiment_start.sh quic 40 1
sleep 3600
./logs.sh quic-40-1-manager-queue
sleep 30
./experiment_end.sh


sleep 600

./experiment_start.sh quic 50 1
sleep 3600
./logs.sh quic-50-1-manager -queue
sleep 30
./experiment_end.sh
