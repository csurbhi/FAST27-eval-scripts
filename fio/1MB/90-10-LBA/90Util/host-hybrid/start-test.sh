#!/bin/bash

cd /home/surbhi/github/hybrid-stl
sudo ./format /dev/sda
sudo ./populate /dev/sda 6553
sudo insmod hybrid-stl.ko
echo "Creating device"
/sbin/dmsetup create TL1 --table '0 15566110720 hybrid-stl /dev/sda TL1 524288 15566110720'

cd /home/surbhi/github/FAST27-eval-scripts/fio/1MB/90-10-LBA/90Util/host-hybrid
fio ./fio-start-cleaning.fio > fio.out.1

sudo dmsetup remove TL1
sudo rmmod hybrid-stl
echo "Test done"

