#!/bin/bash

sudo -s
/home/surbhi/github/fstl/format /dev/sda
/home/surbhi/github/fstl/populate /dev/sda 6553
insmod lsdm.ko
echo "Creating device"
/sbin/dmsetup create TL1 --table '0 15566110720 lsdm /dev/sda TL1 524288 15566110720'
echo 55 > /sys/kernel/lsdm_stats/middle_watermark
cat /sys/kernel/lsdm_stats/middle_watermark
fio ./fio-start-cleaning.fio > fio.out.1

echo "1MB fio test for 90/10 zipf is done!"
sudo dmsetup remove TL1
sudo rmmod lsdm.ko
echo "Test done"

