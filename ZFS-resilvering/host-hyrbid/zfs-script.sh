#!/bin/bash

sudo ./format /dev/sdd
cd /home/surbhi/github/hybrid-stl
sudo insmod hybrid-stl.ko
/sbin/dmsetup create TL1 --table '0 15566110720 hybrid-stl /dev/sdd TL1 524288 15566110720'
sudo zpool import silverpool
zpool status
sudo zpool replace silverpool <DEVICE> /dev/dm-0
