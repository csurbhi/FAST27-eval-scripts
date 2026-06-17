#!/bin/bash

dmzadm --format /dev/sda
cd "run1"
echo "Starting first run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.1
date +%m:%s
cd ..
#start the test after waiting for 2 hours
sleep 120m
cd "run2"
echo "Starting second run after sleeping for 470 minutes"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.2
date +%m:%s
cd ..
# sleep 4 hours
sleep 240m
cd "run3"
echo "Starting third run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.3
date +%m:%s
cd ..
# sleep 5 hours
sleep 300m
cd "run4"
echo "Starting fourth run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.4
date +%m:%s
cd ..
# sleep 6 hours
sleep 360m
cd "run5"
echo "Starting first run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.5
date +%m:%s
cd ..
# sleep 7 hours
sleep 420m
cd "run6"
echo "Starting sixth run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.6
date +%m:%s
cd ..
# sleep 8 hours
sleep 480m
cd "run7"
echo "Starting seventh run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.7
date +%m:%s
cd ..
# sleep 8.5 hours
sleep 510m
cd "run8"
echo "Starting eigth run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.8
date +%m:%s
cd ..
# sleep 9 hours
sleep 540m
cd "run9"
echo "Starting ninth run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.9
date +%m:%s
cd ..
# sleep 9.5 hours
sleep 570m
cd "run10"
echo "Starting tenth run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.10
date +%m:%s
cd ..
# sleep 10 hours
sleep 600m
cd "run11"
echo "Starting eleventh run"
date +%m:%s
fio ./fio-fill-cache.fio | tee ./fio.out.11
date +%m:%s
cd ..
echo "Stopping the test"
