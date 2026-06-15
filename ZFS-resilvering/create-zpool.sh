sudo zpool create silverpool raidz -o ashift=12 -f  /dev/sda /dev/sdb /dev/sdc /dev/sdd
sudo zfs create silverpool/silverfs -o mountpoint=/zfs
sudo ./data-populate.sh
#zpool iostat -v -T d -y 60 | tee ./iostat-<devicename>.out
