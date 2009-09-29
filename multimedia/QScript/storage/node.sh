#!/bin/bash

DESC="stroage node"
STOREBASE="/"
SCRIPT_DIR="/opt/Qscript/"

#check linux release version
RELEASE_INFO=( $(lsb_release -i ) )
SUPPORT=0
CHECK_SUPPORT=1

if [ $CHECK_SUPPORT -eq 1 ];then
    for (( i=0; i< ${#RELEASE_INFO[@]}; i++ ));
    do
        if [ "${RELEASE_INFO[$i]}" = "CentOS" ];then
            SUPPORT=1
        fi
    done

    if [ $SUPPORT  -eq 0 ]; then
        echo "sorry we only support centos 5.2 latest version"
        exit;
    fi
fi

# on error exit
set -e

#usage
Usage (){
    echo "Usage: node.sh install [node_num]]"
    exit 0
}

# if input string is a number
isNumber (){
    expr $1 + 1 2> /dev/null > /dev/null

    if [ $? = 0 ];then
        return 0
    else
        return 1
    fi
}

#script param is right in number
if [ $# -lt 1 ]; then
    Usage
fi

#add portmap nfs as service
addService (){
    if [ ! -e "/sbin/chkconfig" ];then
        echo "chkconfig not exists" >&2
        exit
    fi

    if [ ! -e "/etc/init.d/portmap" ];then
        echo "portmap service not exists" >&2
        exit
    fi

    if [ ! -e "/etc/init.d/nfs" ];then
        echo "nfs service not exists" >&2
        exit
    fi

    if [ ! -e "/usr/sbin/exportfs" ];then
        echo "exportfs not exists" >&2
        exit
    fi

    /sbin/chkconfig --add portmap
    /sbin/chkconfig --add nfs
    /etc/init.d/portmap start
    /etc/init.d/nfs start
    /usr/sbin/exportfs -ra
}

#add crontab script for tracker
addScript (){

    if [ ! -d $SCRIPT_DIR ];then
        mkdir $SCRIPT_DIR
    fi

    SCRIPTNAME=$SCRIPT_DIR$1".sh"
    echo "#!/bin/sh" >$SCRIPTNAME
    echo 'NODE="'$1'"' >>$SCRIPTNAME
    echo 'DISK="'$2'"' >>$SCRIPTNAME
    echo 'df -l|grep ${DISK} > ${DISK}/${NODE}disk.txt' >>$SCRIPTNAME
    echo 'top -n 1 -b|head -4 > ${DISK}/${NODE}top.txt' >>$SCRIPTNAME
    echo 'free |grep Swap > ${DISK}/${NODE}swap.txt'  >>$SCRIPTNAME

    chmod +x $SCRIPTNAME

    #ubuntu
    if [ -e "/var/spool/cron/crontabs/root" ];then
        CRON_SCRIPT="/var/spool/cron/crontabs/root"
        echo
    fi

    #centos
    if [ -e "/var/spool/cron/root" ];then
        CRON_SCRIPT="/var/spool/cron/root"
    fi

    if [ -z $CRON_SCRIPT ];then
        echo "CRON_SCRIPT NOT FOUND" >&2
        exit
    fi

    CRON_JOB_EXISTS=0

    JOB="*/3 * * * * ( $SCRIPTNAME >/dev/null 2>&1 )"

    exec 3<&0
    exec 0<$CRON_SCRIPT

    while read line
    do
        if [ "$line" = "$JOB" ];then
            CRON_JOB_EXISTS=1
        fi
    done
    exec 0<&3

    if [ $CRON_JOB_EXISTS -eq 1 ];then
        echo "cron job exists,if you want to modify your job, Manually modify"
    else
        echo  "$JOB">>$CRON_SCRIPT
        /etc/init.d/crond restart
    fi
}

#install as a node of storage with nfs server
Install (){

    isNumber $1

    if [ $? -eq 1 ]; then
        Usage
        exit
    fi

    node_num=`printf %03d $1`
    if [ $node_num -lt 1 ];then
        Usage
    fi

    NODENAME="st"$node_num

    STORE_DIR=$STOREBASE$NODENAME

    if [ ! -d $STORE_DIR ];then
        echo $STORE_DIR" not exists" >&2
        echo "check if disk is mounted" >&2
        exit
    fi

    #echo $NODENAME;
    EXPORTED=0
    if [ -e /etc/exports ];then
        EXPORT_MACHINE=( $(cat /etc/exports) )
        for (( i=0; i<${#EXPORT_MACHINE[@]}; i++ ));
        do
            TMP_NODE_NAME=${EXPORT_MACHINE[$i]}
            if [ $TMP_NODE_NAME = $STORE_DIR ];then
                EXPORTED=1
            fi
        done
    fi

    if [ $EXPORTED -eq 0 ];then
        echo $STORE_DIR"  10.10.208.0/24(rw,sync)" >> /etc/exports
    fi

    addService
    addScript $NODENAME $STORE_DIR

    echo "run successfully"
    exit
}

Check (){
    echo "TODO"
    exit
}

case "$1" in
  install)
        shift
        Install $1
	;;
  check)
        shift
        Check $1
        ;;
esac

Usage
exit
