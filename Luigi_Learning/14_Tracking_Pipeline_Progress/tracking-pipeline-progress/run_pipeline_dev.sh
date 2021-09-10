#!/bin/zsh
cd /Users/purpleblack/sources/scheduling-pipeline &&\
LUIGI_CONFIG_PATH=luigi_dev.cfg \
/Users/purpleblack/envs/demo/bin/python -m luigi --module scheduling-pipeline \
DownloadSalesData >>luigi_dev.log 2>&1 #puts output message and error message in the same log file
