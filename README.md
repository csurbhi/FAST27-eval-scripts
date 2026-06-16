# FAST27-eval-scripts
Evaluation scripts for FAST27 


To evalatuate the results access to SMR drives is necessary.
We will provide remote access to our machine that has the SMR drives for the experiments.

Following test results are provided in the paper:
1) fio tests
2) Linux kernel parallel build
3) ZFS resilvering.

The ZFS resilvering is done on a machine with CMR drives and then it needs someone to physically yank a device and replace the CMR drive with SMR drive and rerun the test.
This will need some co-ordination with the authors - as someone at UBC needs to yank the disk out and the AEC member to rerun the resilvering test.
We will provide this co-ordination as per the AEC member's availability by communicating over email. Please contact csurbhi@cs.ubc.ca for this.

------------
## Contents of this repository:

.
├── Linux-kernel-compile/               # Evaluation scripts to compile 5 instances of Linux kernel 
├── ZFS-resilvering           		# Evaluation scripts to perform ZFS silvering - needs human intervention 
├── fio					# Evaluation scripts to run fio scripts.
├── Reverse-Engineering			# Evaluation scripts to show the results of Reverse engineering
└── README.md				# this file

Clone the following repositories to checkout the STL source code:
a) Host-LS:
git clone git@github.com:csurbhi/fstl.git

b) Host-Hybrid:
git clone git@github.com:csurbhi/hybrid-stl.git

------------

## Dependencies

### Linux Kernel Dependency:

a) **Linux Kernel version:** `6.6.0`
b) **Custom Kernel:** We recompiled this kernel with the necessary Zoned device support. 
* Our compiled kernel version is identified as:`6.6.0-dirty`. 
* The config file for this compile is included in this github repo as config-6.0-FAST
c) > ⚠️  This kernel version produces a very large initrd as the .ko are unstripped
The instructions to fix  this and allow the kernel to boot are listed here:
https://unix.stackexchange.com/questions/270390/how-to-reduce-the-size-of-the-initrd-when-compiling-your-kernel

#### Copied the relevant portion here:

-------------
You could also change the configuration of your initramfs.conf

Find the file at /etc/initramfs-tools/initramfs.conf

There is a setting that says MODULES=most this includes most of the modules kn your initrd image.

Change it to MODULES=dep this makes the initramfs generator guess which modules to include.

-------------
### Package dependency:
The evaluation depends on the following packages:
a) parallel
b) iostat
c) python3.
d) tmux
** sudo apt-get update && sudo apt-get install -y parallel sysstat python3 tmux **

These tests need to be completed on the UBC machine with the specialized hardware (SMR drives). The necessary packages and the compiled Linux kernel are preinstalled on these machines.

------------

### Hardware Verification (SMR Drive)

Ensure that you have the right SMR drive installed by executing the following:

Run the following command (replace `/dev/sda` with your target drive):
```bash
sudo sg_inq /dev/sda  -> ensure that /dev/sda is a SMR drive.
```

#### Expected Output
The output should closely match the following block. 

```bash
standard INQUIRY:
  PQual=0  PDT=0  RMB=0  LU_CONG=0  hot_pluggable=0  version=0x05  [SPC-3]
  [AERC=0]  [TrmTsk=0]  NormACA=0  HiSUP=0  Resp_data_format=2
  SCCS=0  ACC=0  TPGS=0  3PC=0  Protect=0  [BQue=0]
  EncServ=0  MultiP=0  [MChngr=0]  [ACKREQQ=0]  Addr16=0
  [RelAdr=0]  WBus16=0  Sync=0  [Linked=0]  [TranDis=0]  CmdQue=1
  [SPI: Clocking=0x0  QAS=0  IUS=0]
    length=96 (0x60)   Peripheral device type: disk
 Vendor identification: ATA
 Product identification: ST8000AS0022-1WL
 Product revision level: SN01
 Unit serial number:             Z840Y0FY
```

------------

## Artifact Reevaluation:

> ⚠️  Note: All the tests run one at a time. They cannot be run in parallel for now.

Access the scripts on the machine we give you access to (they are the same as the contents of this repository):
-----------

cd /home/surbhi/github/FAST27-eval-scripts


-----------
### 1. Linux kernel compile results (requires around 4-5 hours for all three STL tests)

Note that this test - needs to be run on the machine called "sharada"
We will provide the instructions to access this machine over email.


A) device-hybrid:

start a tmux instance:

1) sudo fdisk /dev/sda
(Create a 150GB worth partition using the following options:
		select "n" command to create a partition
		select "p" command to create a primary partition
		partition number 1
		first section -> select the default
		last sector -> +150G
		select "p" to print the partition created. Make sure that the partition is indeed 150GB before you proceed further.
2) ./start.sh
3) This should generate the following log files:
	a) parallel_build_iostat.log
	b) build_[1-5].log
	c) dmesg
	

B) host-hybrid:

start tmux

in this tmux instance:
	1) tail -f /var/log/kern.log | tee ./dmesg
	2) Ctr + B + D (to detach from it)

start another tmux instance:
	1) cd /home/surbhi/github/hybrid-stl
	2) sudo ./format /dev/sda SIZE (GB)
	3) sudo insmod hybrid-stl.ko
	4) Copy the last line printed by the above script.
	This should create the /dev/dm-0 device.
	5) cd /home/surbhi/github/FAST27-eval-scripts/Linux-kernel-compile/5ParallelCompiles/host-ls/compile5Times/150GB/7GB-MiddleWaterMark
	6) ./start.sh
	7) This should generate the following log files:
		a) parallel_build_iostat.log
		b) build_[1-5].log
		c) dmesg
	8) Now run the following python script to get the result file:
	9) dmsetup remove TL1
	10) rmmod hybrid-stl.ko

C) host-ls:

start tmux

in this tmux instance:
	1) tail -f /var/log/kern.log | tee ./dmesg
	2) Ctr + B + D (to detach from it)

start another tmux instance:
	1) cd /home/surbhi/github/fstl
	2) sudo ./format /dev/sda SIZE (GB)
	3) sudo insmod lsdm.ko
	4) Copy the last line printed by the above script.
	This should create the /dev/dm-0 device.
	5) cd /home/surbhi/github/FAST27-eval-scripts/Linux-kernel-compile/5ParallelCompiles/host-ls/compile5Times/150GB/7GB-MiddleWaterMark
	6) ./start.sh
	7) This should generate the following log files:
		a) parallel_build_iostat.log
		b) build_[1-5].log
		c) dmesg
	8) dmsetup remove TL1
	9) rmmod lsdm.ko


Now run the following python script to get the result file:
/home/surbhi/github/FAST27-eval-scripts/Linux-kernel-compile/FAST27_linux-compile-iostat.ipynb

The paths in this python notebook needs to change to reflect the actual iostat files collected.
The files are writes.csv -> generated as follows:

```bash 
cat parallel_build_iostat.log  | grep "dm-0" | tr -s " " | cut -d " " -f 4 | tee ./writes_dm0.csv

for device-hybrid:
cat parallel_build_iostat.log  | grep "sda" | tr -s " " | cut -d " " -f 4 | tee ./writes_sda.csv

The plot script uses these writes_dm0.csv and the writes_sda.csv
```

-----------------------------------

### 2. ZFS resilvering tests:
-----------

We will provide the machine access to run these tests over email. These tests need 4 CMR drive and a proportionally sized Host-Aware SMR drive.
This also needs some coordination with the authors - as someone at UBC needs to yank a drive
and replace it with the SMR drive in consideration. This will start the resilvering process
on this replaced drive. Please reach out when you are ready to run this test.
This is nearly a 2 week long test.

	1) cd /home/surbhi/github/FAST27-eval-scripts/ZFS-resilvering
	2) create the zpool and populate its contents using the following:
	```bash
		./create-zpool.sh
	```
	This should populate ~5TB of the device space and should take around 2 days.
	3)  After the device is populated, the AEC member should coordinate with the authors to yank out a CMR drive
	and replace it with a SMR drive and eventually a CMR drive back.
	Once the device is replaced. Go to the respective folder (host-ls, host-hybrid, device-hybrid, CMR) and every time
	start the resilvering process. Before that is done, start the iomonitoring by this command in a tmux instance.
	```bash
	zpool iostat -v -T d -y 60 | tee ./iostat-<devicename>.out
	```
	4) start resilvering by:
		cd host-ls OR
		cd host-hybrid OR 
		cd device-hybrid OR
		cd CMR OR
	Run:
	```bash
		./zfs-script.sh
	```
	In this script replace  the <DEVICE> with the zfs device we replace - this is seen in the command:
		zpool status

	Resilvering completion status can also be seen with this zpool status command.
	The completion times should be as follows:
	a) host-ls: /~9 hours
	b) CMR: ~12.5 hours
	c) host-hybrid: ~ 2 days
	d) device-hybrid: ~ 4 days.

	5) The plots can generated using this python notebook:
FAST27_zfs-iostat-resilvering_final.ipynb

Similar to the linux kernel test - the python notebook runs on the writebw-<device>.csv file.
This file is generated by getting the column out from the zpool iostat output.

--------------------------------------------------------

fio tests:
-----------
1MB test:
--------

1) cd /home/surbhi/github/FAST27-eval-scripts/fio/1MB/90-10-LBA/90Util
2) cd host-hybrid
3) ./start.sh
4) cd ../device-hybrid
5) ./start.sh
6) cd ../host-ls
7) ./start.sh



