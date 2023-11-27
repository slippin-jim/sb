#!/bin/bash -l

echo 'Started games load'
echo date +'%a %b %e %H:%M:%S %Z %Y'

conda run -n sb /Users/jim/dev/sb/helpers/load_logger.py "start"
output=$(conda run -n sb /Users/jim/dev/sb/load_stats.py)
conda run -n sb /Users/jim/dev/sb/helpers/load_logger.py $output