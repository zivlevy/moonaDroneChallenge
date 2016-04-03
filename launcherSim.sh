#!/bin/sh
# launcherSim.sh

echo "start"
cd /
cd home/pi
echo $1
sudo screen -d -m -s /bin/bash mavproxy.py --master=tcp:$1:5760 --out=$1:14550 --out=127.0.0.1:1244 &
echo "mavproxy done"
cd copter 
# python mdc.py & 
# echo "mds.py done"
python webUpdate.py & 
echo "webUpdate.py done"
cd /
