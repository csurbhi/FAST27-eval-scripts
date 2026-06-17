#!/bin/bash

# Configuration
DEVICE="/dev/dm-0"
MOUNT_POINT="/mnt"
SRC_DIR="/home/surbhi/github/linux"  # Path to your clean source
LOG_DIR="$(pwd)"

cd /home/surbhi/github/hybrid-stl
sudo ./format /dev/sda 600
sudo insmod hybrid-stl
sudo /sbin/dmsetup create TL1 --table '0 315097088 hybrid-stl /dev/sda TL1 524288 315097088'

echo "--- Starting SMR Parallel Build Evaluation ---"

mkfs.ext4 $DEVICE
mount -t ext4 $DEVICE $MOUNT_POINT

# 1. Start iostat in the background
iostat -d "$DEVICE" "/dev/sdb" 1 > "$LOG_DIR/parallel_build_iostat.log" &
IOSTAT_PID=$!

# 2. Run the workload with GNU Parallel
# -j 7: Runs 7 instances in parallel
# {}: Replaces with the instance number (1-7)
parallel -j 5 "
    mkdir -p $MOUNT_POINT/inst_{} && \
    cp -r $SRC_DIR/. $MOUNT_POINT/inst_{}/ && \
    cd $MOUNT_POINT/inst_{} && \
    make -j 12 &> $LOG_DIR/build_{}.log
" ::: {1..5}

# GNU Parallel blocks the script until all 7 instances are finished,
# so we don't need a manual 'wait' command here.

# 3. Finalize
echo "Workload complete. Flushing buffers..."
sync
sleep 5  # Ensure SMR background GC or metadata updates are captured

kill $IOSTAT_PID
echo "--- Evaluation Complete ---"

sudo umount /mnt
sudo dmsetup remove TL1
sudo rmmod hybrid-stl
