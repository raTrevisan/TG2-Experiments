./experiment_start_critical.sh quic 30 1
sleep 3000
./logs.sh quic-30-1-critical 
sleep 30
./experiment_end.sh

sleep 600

./experiment_start_critical.sh quic 40 1
sleep 3000
./logs.sh quic-40-1-critical 
sleep 30
./experiment_end.sh

sleep 600

./experiment_start_critical.sh quic 50 1
sleep 3000
./logs.sh quic-50-1-critical 
sleep 30
./experiment_end.sh

sleep 600

./experiment_start.sh quic 40 1
sleep 3000
./logs.sh quic-40-1 
sleep 30
./experiment_end.sh


sleep 600

./experiment_start.sh quic 50 1
sleep 3000
./logs.sh quic-50-1 
sleep 30
./experiment_end.sh
