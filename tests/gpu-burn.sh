#!/bin/bash

SCRIPT_PATH=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
#see bellow (+2)
BUILD_GPU_BURN=0
#(-1)what is this for????

if (($# == 0)); then
    MINUTES=60
else
    MINUTES=$1
fi

if (($MINUTES < 10)); then
    MINUTES=10
fi

SECONDS=$(($MINUTES * 60))
#(+1) probably change this
nohup bash -c "PATH=$PATH:$SCRIPT_PATH/bin LD_LIBRARY_PATH=$SCRIPT_PATH/lib gpu_burn -tc $SECONDS" &

nohup watch -n 1 nvidia-smi &

until pgrep -x "gpu_burn" &>/dev/null; do
    sleep 30
done

while pgrep -x "gpu_burn" &>/dev/null; do
    sleep 60
done

kill $(ps -Af | grep watch | grep nvidia-smi | awk '{print $2}')
