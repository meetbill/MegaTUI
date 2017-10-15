#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-03-16 21:36:04

# File Name: three_page.py
# Description:
# version:1.0.3
"""
import os, sys
reload(sys)
sys.setdefaultencoding('utf8')
root_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, os.path.join(root_path, 'mylib'))
from snack_lib import Mask
from snack_lib import conformwindows
from snack_lib import Snack_output
from BLog import Log
from megalib import MegaCLI
cli = MegaCLI()
debug=False
logpath = "/var/log/menu_tool/acc.log"
logger = Log(logpath,level="debug",is_console=debug, mbs=5, count=5)

def three1_1funtion(screen):
    """
    raid status
    
    """
    try:
        adapters = cli.adapters()[0]    
    except :
        waring = Snack_output(screen, "waring", 35 )
        waring.text("not found raid card")
        waring.run(43,3)
        return 0
    m = Snack_output(screen, "status_raid", 35 )
    m.text("raid卡名称:   %s"%adapters["product_name"])
    m.text("物理磁盘数量: %s"%adapters["disks"])
    m.text("高危磁盘:     %s"%adapters["critical_disks"])
    m.text("失效磁盘:     %s"%adapters["failed_disks"])
    m.text("已创建磁盘组: %s"%adapters["virtual_drives"])
    m.text("下线磁盘组:   %s"%adapters["offline"])
    m.text("降级磁盘组:   %s"%adapters["degraded"])
    m.text("开启JBOD模式: %s"%adapters["enable_jbod"])
    m.run(43,3)

def three1_2funtion(screen):
    """
    物理磁盘信息
    """
    try:
        adapters = cli.adapters()[0]    
    except :
        waring = Snack_output(screen, "waring", 35 )
        waring.text("not found raid card")
        waring.run(43,3)
        return 0

    m = Snack_output(screen, "status_raid", 35 )
    physicaldrives = cli.physicaldrives()  
    m.text("%s%s%s"%(format("slot_number","^10"),format("raw_size","^15"),format("firmware_state","^20")))
    for drive in physicaldrives:
        m.text("%s%s%s"%(format(drive["slot_number"],"^10"),format(drive["raw_size"],"^15"),format(drive["firmware_state"],"^20")))
    m.run(43,3)

def three1_3funtion(screen):
    """
    逻辑磁盘信息
    """
    try:
        adapters = cli.adapters()[0]    
    except :
        waring = Snack_output(screen, "waring", 35 )
        waring.text("not found raid card")
        waring.run(43,3)
        return 0

    m = Snack_output(screen, "status_vd", 65 )
    logicaldrives = cli.logicaldrives()  
    m.text("%s%s%s%s%s"%(format("vd","^4"),format("num","^6"),format("size","^12"),format("state","^8"),format("raid_level","^8")))
    for vd in logicaldrives:
        if id in vd.keys():
            m.text("%s%s%s%s%s"%(format(vd["id"],"^4"),format(vd["number_of_drives"],"^6"),format(vd["size"],"^12"),format(vd["state"],"^8"),format(vd["raid_level"],"^8")))
    m.run(43,3)

def example(screen):
     m = Mask(screen, "test_windows1_1", 35 )
     m.text("label_test0","ceshi_text")
     m.entry( "label_test1", "entry_test1", "0" )
     m.entry( "label_test2", "entry_test2", "0" )
     m.entry( "label_test3", "entry_test3", "127.0.0.1" )
     m.checks( "复选框","checks_list",[
         ('checks_name1','checks1',0),
         ('checks_name2','checks2',0),
         ('checks_name3','checks3',0),
         ('checks_name4','checks4',1),
         ('checks_name5','checks5',0),
         ('checks_name6','checks6',0),
         ('checks_name7','checks7',0),
     ],
     height= 5
     )    
     m.radios( "单选框","radios", [ 
         ('radios_name1','radios1', 0), 
         ('radios_name2','radios2', 1), 
         ('radios_name3','radios3', 0) ] )  
     
     m.buttons( yes="Sava&Quit", no="Quit" )
     (cmd, results) = m.run(43,3)
     
     logger.debug(str(cmd)+" "+str(results))
     if cmd == "yes":
        rx = conformwindows(screen, "确认操作")
        if rx[0] == "yes" or rx[1] == "F12":
            """exe"""
            return
        else:
            logger.debug("cancel this operation")
            return
     else:
        return

if __name__ == "__main__":
    from snack import *
    try:
        screen = SnackScreen()
        screen.setColor("ROOT", "white", "blue")
        screen.setColor("ENTRY","white","blue")
        screen.setColor("LABEL","black","white")
        screen.setColor("HELPLINE","white","blue")
        screen.setColor("TEXTBOX","black","yellow")
        three1_2funtion(screen)
    except Exception,e:
        print e
    finally:
        screen.finish()
