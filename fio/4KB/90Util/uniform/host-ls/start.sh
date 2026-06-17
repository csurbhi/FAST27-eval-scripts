#!/bin/bash +x

sudo /home/surbhi/github/fstl/format /dev/sda 
sudo /home/surbhi/github/fstl/populate /dev/sda 6553
sudo -s
/sbin/dmsetup create TL1 --table '0 15597043712 lsdm /dev/sda TL1 524288 15597043712'
# 201 - 2 - 3
echo 196 > /sys/kernel/lsdm_stats/middle_watermark
cat /sys/kernel/lsdm_stats/middle_watermark

fio ./fio-fill-cache.fio 2>&1 | tee ./fio.out
sudo dmsetup remove TL1
sudo rmmod lsdm
