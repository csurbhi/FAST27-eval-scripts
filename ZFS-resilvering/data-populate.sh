#!/bin/bash +x

echo "writing to file a ...."
dd if=/dev/urandom of=/zfs/random-fileA count=100000 bs=4096000 iflag=fullblock
echo "writing to file b ...."
dd if=/dev/urandom of=/zfs/random-fileB count=100000 bs=4096000 iflag=fullblock
echo "writing to file c ...."
dd if=/dev/urandom of=/zfs/random-fileC count=100000 bs=4096000 iflag=fullblock
echo "rewriting file a (100 blocks)...."
dd if=/dev/urandom of=/zfs/random-fileA count=100 bs=4096000 iflag=fullblock
echo "writing to file d ...."
dd if=/dev/urandom of=/zfs/random-fileD count=100000 bs=4096000 iflag=fullblock
rm /zfs/random-fileA
echo "writing to file e ...."
dd if=/dev/urandom of=/zfs/random-fileE count=100000 bs=4096000 iflag=fullblock
#repeat
echo "rewriting to file a ...."
dd if=/dev/urandom of=/zfs/random-fileA count=100000 bs=4096000 iflag=fullblock
rm /zfs/random-fileC
echo "writing to file f ...."
dd if=/dev/urandom of=/zfs/random-fileF count=100000 bs=4096000 iflag=fullblock
rm /zfs/random-fileE
echo "writing to file g ...."
dd if=/dev/urandom of=/zfs/random-fileG count=100000 bs=3196000 iflag=fullblock
#repeat
echo "rewriting file e...."
dd if=/dev/urandom of=/zfs/random-fileE count=100000 bs=4096000 iflag=fullblock
#repeat
echo "rewriting file c...."
dd if=/dev/urandom of=/zfs/random-fileC count=100000 bs=4096000 iflag=fullblock
echo "rewriting file e (100 blocks)...."
dd if=/dev/urandom of=/zfs/random-fileE count=100 bs=4096000 iflag=fullblock
