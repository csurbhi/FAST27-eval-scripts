#!/bin/bash

sudo dmzadm --format /dev/sda
# 50% utilization
/home/surbhi/github/fstl/zonepopulate /dev/sda 29807 6553
echo "Starting first run (90-10-LBA - 50% zone utilization, bs=4K, sda), to fill the cache" > fio.out.1
date +%m:%s >> fio.out.1
fio fio-fill-cache.fio >> fio.out.1
date +%m:%s >> fio.out.1
echo "Stopping the test"
