#!/bin/bash
WORKER_PID=''

send_usr1_to_worker(){
    kill -USR1 $WORKER_PID
    wait $WORKER_PID
}

trap 'send_usr1_to_worker' TERM INT

python3 /code/run_python_workers.py & WORKER_PID=$!
wait $WORKER_PID
