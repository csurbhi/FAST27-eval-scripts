#!/bin/bash +x

#nr cache zones is 7 + 4 watermark + 1 metadata
sudo /home/surbhi/github/hybrid-stl/format /dev/sda 0 3
sudo /home/surbhi/github/hybrid-stl/populate /dev/sda 6553
sudo insmod hybrid-stl.ko
echo "Creating device"
sudo /sbin/dmsetup create TL1 --table '0 15566110720 hybrid-stl /dev/sda TL1 524288 15566110720'

sudo fio ./fio-fill-cache.fio 2>&1 | tee ./fio.out

sudo dmsetup remove TL1
sudo rmmod hybrid-stl
echo "4KB host-hybrid 90/10 zipf fio microbenchmark executed"
