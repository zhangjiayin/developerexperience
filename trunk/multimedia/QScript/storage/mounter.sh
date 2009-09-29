#!/bin/bash

MACHINESFILE="machines"
STOREBASE="/"
USEBASE="/Data/upload/"
TRACKER_DIR="/upload_config/"

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


dryAdd (){
    addService
    mountstorage
}

mountstorage (){
    echo "mounting sotrage"
    exec 3<&0
    exec 0<$MACHINESFILE

    i=0
    while read line
    do
        NODE_INFO=( $line )

        SERVERS[$i]=${NODE_INFO[0]}
        MASTERS[$i]=${NODE_INFO[1]}
        CPUS[$i]=${NODE_INFO[2]}
        SLAVES[$i]=${NODE_INFO[3]}

        #TODO
        set +e
        echo "mounting ${NODE_INFO[0]} @ ${NODE_INFO[1]}"
        `mount "${NODE_INFO[1]}":"$STOREBASE"${NODE_INFO[0]}""  $USEBASE${NODE_INFO[0]} -t nfs`
	MOUNT_RETURN=$?
	if [ $MOUNT_RETURN -ne 32 -a $MOUNT_RETURN -ne 0 ];then
	 	echo "error mounting ${NODE_INFO[0]} at  ${NODE_INFO[1]}"
		exit
	fi
        echo "mounting ${NODE_INFO[0]} @ ${NODE_INFO[1]} done"
        set -e

        MOUNTED=( $(cat /etc/fstab ) )
        ISMOUNTED=0
        for (( j=0; j<${#MOUNTED[@]}; j++));
        do
            if [ "$USEBASE${NODE_INFO[0]}"   = ${MOUNTED[$j] } ];then
                ISMOUNTED=1
            fi
        done

        if [ $ISMOUNTED -eq 0 ];then
            echo "${NODE_INFO[1]}:$STOREBASE${NODE_INFO[0]} $USEBASE${NODE_INFO[0]} nfs rsize=8192,wsize=8192,timeo=14,intr,tcp" >> /etc/fstab
        fi

        (( i++ ))
    done
    exec 0<&3
    mount -a
    echo "mounting sotrage done"
}

addTracker (){
    if [ ! -d $TRACKER_DIR ];then
        mkdir $TRACKER_DIR -p -m 0755
    fi

    cp tracker.sh  $TRACKER_DIR
    cp machines $TRACKER_DIR

    echo "#!/bin/sh" > $TRACKER_DIR"cron.sh"
    echo "cd "$TRACKER_DIR >> $TRACKER_DIR"cron.sh"
    echo $TRACKER_DIR"tracker.sh" >> $TRACKER_DIR"cron.sh"
    echo "cp -f "$TRACKER_DIR"weight.config.tmp.php "$TRACKER_DIR"weight.config.php" >> $TRACKER_DIR"cron.sh"
    chmod +x $TRACKER_DIR"cron.sh"

    bash $TRACKER_DIR"cron.sh"

    #ubuntu
    if [ -e "/var/spool/cron/crontabs/root" ];then
        CRON_SCRIPT="/var/spool/cron/crontabs/root"
    fi

    #centos
    if [ -e "/var/spool/cron/root" ];then
        CRON_SCRIPT="/var/spool/cron/root"
    fi

    if [ -z $CRON_SCRIPT ];then
        echo "CRON_SCRIPT NOT FOUND" >&2
        exit
    fi

    CRON_JOB=$TRACKER_DIR"cron.sh"

    JOB_EXISITS=`cat $CRON_SCRIPT |grep $CRON_JOB`

    if [ -z "$JOB_EXISITS" ];then
        JOB="*/3 * * * * ( $CRON_JOB >/dev/null 2>&1 )"
        echo "$JOB" >> $CRON_SCRIPT
    fi

    if [ -e "/etc/init.d/cron" ];then
       /etc/init.d/cron restart
        echo "run successfully"
        exit
    fi

    if [ -e "/etc/init.d/crond" ];then
       /etc/init.d/crond restart
        echo "run successfully"
        exit
    fi

    echo "crond restart fail"
}


#usage
Usage (){
    echo "Usage: mounter.sh [ lit|full ]"
    echo "只挂载不用程序的时候 用dry参数"
    exit 0
}

case "$1" in
  lit)
  #只挂载 不用程序
        shift
        dryAdd
        exit;
	;;
  full)
        shift
        dryAdd
        addTracker
        exit
        ;;
esac

Usage
exit
