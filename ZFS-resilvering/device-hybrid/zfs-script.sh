#!/bin/bash

sudo ./format /dev/sdd
sudo zpool import silverpool
zpool status
sudo zpool replace silverpool <DEVICE> /dev/sdd
