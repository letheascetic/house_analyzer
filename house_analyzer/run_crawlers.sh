#!/usr/bin/env bash


source activate py3
nohup python run_crawlers.py >/dev/null  2>&1 &
echo $! > pid.txt

