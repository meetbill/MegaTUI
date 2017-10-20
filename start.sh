#########################################################################
# File Name: start.sh
# Author: meetbill
# mail: meetbill@163.com
# Created Time: 2016-12-30 14:49:49
#########################################################################
#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)
cd ${CUR_DIR}

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to install"
    exit 1
fi

##########################################################process
x=''
NUM=2
function ProcessBar()
{
	x=##########$x
	printf "install-megacli_menu:[%-${NUM}0s]\r" $x
	sleep 0.1
}
##########################################################process_end
g_BACKUP_DIR=/opt/megacli_menu_oldbackup
g_APP=mymegacli
function check_dir()
{
    if [[ -d /opt/${g_APP}  ]]
	then
        if [ ! -d ${g_BACKUP_DIR} ]
        then
            mkdir -p ${g_BACKUP_DIR}
        else
            rm -rf ${g_BACKUP_DIR}
            mkdir -p ${g_BACKUP_DIR}
        fi
        mv /opt/${g_APP} ${g_BACKUP_DIR}/
        cp -rf ./${g_APP} /opt/
	else
        cp -rf ./${g_APP} /opt/
	fi
    ProcessBar
}
function check_command()
{
    # megatui
    if [[ -f /usr/bin/megatui ]]
    then
        unlink /usr/bin/megatui
        ln -s /opt/mymegacli/py_menu.py /usr/bin/megatui
    else
        ln -s /opt/mymegacli/py_menu.py /usr/bin/megatui
    fi
    chmod +x /usr/bin/megatui
    ProcessBar
}
rpm -ivh ./tools/MegaCli-8.07.14-1.noarch.rpm
bash ./tools/install_lib.sh
check_dir
check_command
echo

