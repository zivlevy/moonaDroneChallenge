#!/bin/sh
# launcher.sh

echo "start"
cd /
cd home/pi
echo $1
sudo screen -d -m -s /bin/bash mavproxy.py --master=/dev/ttyACM0 --baudrate 115200 --out=$1:14550 --out=127.0.0.1:1244 &
echo "mavproxy done"
# sleep 10
# cd copter 
# python mdc.py > mdc.txt 2> errors.log & 
# echo "mds.py done"
python webUpdate.py & 
echo "webUpdate.py done"
cd /