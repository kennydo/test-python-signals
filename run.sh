#!/bin/bash
WORKER_PID=''

handle_sig_term(){
    echo "Sending USR1 to $WORKER_PID"
    kill -USR1 $WORKER_PID
    echo "Waiting for $WORKER_PID"
    wait $WORKER_PID
}

trap 'handle_sig_term' TERM

python3 run_python_workers.py & WORKER_PID=$!
wait $WORKER_PID
