#!/bin/bash

sudo dmzadm --format /dev/sda
# 90% utilization
/home/surbhi/github/fstl/zonepopulate /dev/sda 29807 6553
date +%m:%s >> fio.out.1
fio fio-fill-cache.fio >> fio.out.1
date +%m:%s >> fio.out.1
echo "Stopping the test" >> fio.out.1
