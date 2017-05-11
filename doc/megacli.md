### Introduction

MegaCli commands have presented a number of questions among our users for Cisco's 
Physical Security.  Here is an attempt to explain thier meaning and uses.

### 名词解释

LD称之为Logical Device

**VD(虚拟硬盘)**
> * Virtual Drive  (VD)：虚拟硬盘，简单说就是Raid
> * VD State Optimal  : Raid目前为正常
> * VD State Degraded : Raid状态不正常，退化或者降级

**PD(物理硬盘)**
> * Physical Drive  (PD)：实体硬盘，实际有的硬盘数量
> * PD State Online    : 硬盘目前的状态为正常
> * PD State Fail、Unconfigured、Rebuld：磁盘状态不正常，掉盘、未配置或正在重建Raid

### General Parameters

> * -a  是raid卡
> * -LD 表示Virtual Disk
> * -PD Physical Disk

    Adapter parameter -aN 

The parameter -aN (where N is a number starting with zero or the string ALL) 
specifies the adapter ID. If you have only one controller it’s safe to use ALL 
instead of a specific ID, but you’re encouraged to use the ID for everything 
that makes changes to your RAID configuration.

    Physical drive parameter      -PhysDrv [E:S] 

For commands that operate on one or more pysical drives, the -PhysDrv [E:S] 
parameter is used, where E is the enclosure device ID in which the drive resides 
and S the slot number (starting with zero). You can get the enclosure device ID 
using MegaCli -EncInfo -aALL. The E:S syntax is also used for specifying the 
physical drives when creating a new RAID virtual drive (see 5).

    Virtual drive parameter -Lx 

The parameter -Lx is used for specifying the virtual drive (where x is a number 
starting with zero or the string all).

Running the executable can be accomplished by:

    shell> /opt/MegaRAID/MegaCli/MegaCli <cmd>

or

    shell> cd /opt/MegaRAID/MegaCli
    shell> ./MegaCli <cmd>

### Gather information

Controller information 

     MegaCli -AdpAllInfo -aALL
     MegaCli -CfgDsply -aALL
     MegaCli -adpeventlog -getevents -f lsi-events.log -a0 -nolog

Enclosure information 

     MegaCli -EncInfo -aALL

Virtual drive information

     MegaCli -LDInfo -Lall -aALL

Physical drive information

     MegaCli -PDList -aALL

     MegaCli -PDInfo -PhysDrv [E:S] -aALL

Battery backup information (Cisco MSPs do not have the battery backup unit 
installed, but in case yours has one) 

     MegaCli -AdpBbuCmd -aALL 

Check Battery backup warning on boot.  If this is enabled on an MSP, it will 
require manual intervention every time the system boots

     MegaCli -AdpGetProp BatWarnDsbl -a0 
     
### Controller management

Silence active alarm 

     MegaCli -AdpSetProp AlarmSilence -aALL

Disable alarm 

     MegaCli -AdpSetProp AlarmDsbl -aALL

Enable alarm 

     MegaCli -AdpSetProp AlarmEnbl -aALL 

Disable battery backup warning on system boot

     MegaCli -AdpSetProp BatWarnDsbl -a0

Change the adapter rebuild rate to 60%:

     MegaCli -AdpSetProp {RebuildRate -60} -aALL

### Virtual drive management

Create RAID 0, 1, 5 drive 

     MegaCli -CfgLdAdd -r(0|1|5) [E:S, E:S, ...] -aN

Create RAID 10 drive 

     MegaCli -CfgSpanAdd -r10 -Array0[E:S,E:S] -Array1[E:S,E:S] -aN

Remove drive 

     MegaCli -CfgLdDel -Lx -aN 

### Physical drive management

Set state to offline 

     MegaCli -PDOffline -PhysDrv [E:S] -aN

Set state to online 

     MegaCli -PDOnline -PhysDrv [E:S] -aN

Mark as missing 

     MegaCli -PDMarkMissing -PhysDrv [E:S] -aN

Prepare for removal 

     MegaCli -PdPrpRmv -PhysDrv [E:S] -aN

Replace missing drive 

     MegaCli -PdReplaceMissing -PhysDrv [E:S] -ArrayN -rowN -aN

The number N of the array parameter is the Span Reference you get using 
**MegaCli -CfgDsply -aALL** and the number N of the row parameter is the 
Physical Disk in that span or array starting with zero (it’s not the physical 
disk’s slot!).

Rebuild drive - Drive status should be "Firmware state: Rebuild"

     MegaCli -PDRbld -Start -PhysDrv [E:S] -aN
     MegaCli -PDRbld -Stop -PhysDrv [E:S] -aN
     MegaCli -PDRbld -ShowProg -PhysDrv [E:S] -aN     
     MegaCli -PDRbld -ProgDsply -physdrv [E:S] -aN

Clear drive 

     MegaCli -PDClear -Start -PhysDrv [E:S] -aN
     MegaCli -PDClear -Stop -PhysDrv [E:S] -aN
     MegaCli -PDClear -ShowProg -PhysDrv [E:S] -aN

Bad to good 

     MegaCli -PDMakeGood -PhysDrv[E:S] -aN

Changes drive in state Unconfigured-Bad to Unconfigured-Good.

### Hot spare management

Set global hot spare 

     MegaCli -PDHSP -Set -PhysDrv [E:S] -aN

Remove hot spare 

     MegaCli -PDHSP -Rmv -PhysDrv [E:S] -aN

Set dedicated hot spare 

     MegaCli -PDHSP -Set -Dedicated -ArrayN,M,... -PhysDrv [E:S] -aN 

### Walkthrough: Rebuild a Drive that is marked 'Foreign' when Inserted:

* Bad to good 

    MegaCli -PDMakeGood -PhysDrv [E:S]  -aALL

* Clear the foreign setting

    MegaCli -CfgForeign -Clear -aALL

* Set global hot spare 

     MegaCli -PDHSP -Set -PhysDrv [E:S] -aN

### Walkthrough: Change/replace a drive

1.Set the drive offline, if it is not already offline due to an error

    MegaCli -PDOffline -PhysDrv [E:S] -aN

2.Mark the drive as missing

    MegaCli -PDMarkMissing -PhysDrv [E:S] -aN

3.Prepare drive for removal

    MegaCli -PDPrpRmv -PhysDrv [E:S] -aN

4.Change/replace the drive

5.If you’re using hot spares then the replaced drive should become your new hot spare drive

    MegaCli -PDHSP -Set -PhysDrv [E:S] -aN

6.In case you’re not working with hot spares, you must re-add the new drive to 
your RAID virtual drive and start the rebuilding

    MegaCli -PdReplaceMissing -PhysDrv [E:S] -ArrayN -rowN -aN
    MegaCli -PDRbld -Start -PhysDrv [E:S] -aN

### Gathering Standard logs

On every instance of a hard drive problem with an MSP server, we need to run the 
following commands to have any information about the problem:

    shell> rm –f MegaSAS.log
 
    shell> /opt/MegaRAID/MegaCli/MegaCli -adpallinfo -a0
 
    shell> /opt/MegaRAID/MegaCli/MegaCli -encinfo -a0
 
    shell> /opt/MegaRAID/MegaCli/MegaCli -ldinfo -lall -a0
 
    shell> /opt/MegaRAID/MegaCli/MegaCli -pdlist -a0
 
    shell> /opt/MegaRAID/MegaCli/MegaCli -adpeventlog -getevents -f lsi-events.log -a0 -nolog
 
    shell> /opt/MegaRAID/MegaCli/MegaCli -fwtermlog -dsply -a0 -nolog > lsi-fwterm.log

Collect the MegaSAS.log, lsi-events.log, and the lsi-fwterm.log files from the 
directory where the commands are run (they can be run from any directory on the 
MSP server) and attach the logs to the service request. You may use a program 
such as WinSCP (freeware) to pull the files off of the server.

