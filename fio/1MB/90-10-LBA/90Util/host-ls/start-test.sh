#!/bin/bash

cd /home/surbhi/github/fstl
sudo ./format /dev/sda
sudo ./populate /dev/sda 6553
sudo insmod lsdm.ko
sudo -s
echo "Creating device"
/sbin/dmsetup create TL1 --table '0 15566110720 lsdm /dev/sda TL1 524288 15566110720'
echo 55 > /sys/kernel/lsdm_stats/middle_watermark
cat /sys/kernel/lsdm_stats/middle_watermark

cd /home/surbhi/github/FAST27-eval-scripts/fio/1MB/90-10-LBA/90Util/host-ls
fio ./fio-start-cleaning.fio > fio.out.1

echo "1MB fio test for 90/10 zipf is done!"
sudo dmsetup remove TL1
sudo rmmod lsdm.ko
echo "Test done"

