#!/bin/bash

#define the storage server
MACHINESFILE=machines
exec 3<&0
exec 0<$MACHINESFILE
i=0
while read line
do
    NODE_INFO=( $line )
    STORAGENODE[$i]=${NODE_INFO[0]}
    STORAGECPUS[$i]=${NODE_INFO[2]}
    (( i++ ))
done
exec 0<&3

#define the storage server CPUS number
#define the storage root path
STORAGEROOT=/Data/upload/

#low disk available percent
LOWDISKAVAILABLE=10
#priority {optional : disk,load  default: disk}
PRIORITY=disk
#diskinfo filename
DISKFILE=disk.txt
#topinfo filename
TOPFILE=top.txt
#swapinfo filename
SWAPFILE=swap.txt


WEIGHTFILE=/upload_config/weight.config.tmp.php

THRESHOLD=5
LVLCPU=10
LVLSWAP=1

if [ $PRIORITY = "load" ]; then
	LVLDISK=100
	LVLLOAD=50
else
	LVLDISK=100
	LVLLOAD=25
fi

cat /dev/null > ${WEIGHTFILE}
echo '<?php' >> ${WEIGHTFILE}
echo '$weights = array(' >> ${WEIGHTFILE}

lenSTORAGENODE=${#STORAGENODE[@]}
handle=0
while [ $handle -lt $lenSTORAGENODE ]
do
	if [ -e ${STORAGEROOT}${STORAGENODE[$handle]}/${STORAGENODE[$handle]}${DISKFILE} ]
	then

		disk=`cat ${STORAGEROOT}${STORAGENODE[$handle]}/${STORAGENODE[$handle]}${DISKFILE}|awk '{print $5}'|awk -F'%' '{print int($1)}'`
		load=`cat ${STORAGEROOT}${STORAGENODE[$handle]}/${STORAGENODE[$handle]}${TOPFILE}|awk -F"," '(NR==1){print $4}'|awk -F':' '{print int($2)}'`
		cpu=`cat ${STORAGEROOT}${STORAGENODE[$handle]}/${STORAGENODE[$handle]}${TOPFILE}|awk -F"," '(NR==3){print $4}'|awk -F'%' '{print int($1)}'`
		swap=`cat ${STORAGEROOT}${STORAGENODE[$handle]}/${STORAGENODE[$handle]}${SWAPFILE}|awk '{print int($3)}'`

		MAXCPULOAD=$[${STORAGECPUS[$handle]}*$THRESHOLD]
		diskavalibale=$[100-disk]
		if [ $diskavalibale -lt $LOWDISKAVAILABLE ]
		then
			WEIGHT=0
		elif [ $MAXCPULOAD -lt $load ]; then
			WEIGHT=0
		else
			WEIGHT=$[diskavalibale*LVLDISK]
			tempload=$[load*LVLLOAD]
			WEIGHT=$[WEIGHT-tempload]
			tempcpu=$[cpu*LVLCPU]
			WEIGHT=$[WEIGHT+tempcpu]
			tempswap=$[swap*LVLSWAP]
			WEIGHT=$[WEIGHT-tempswap]
		fi
		tmphandle=$[lenSTORAGENODE-1]
		if [ $handle = $tmphandle ]; then
			echo \'${STORAGENODE[$handle]}\' '=>' ${WEIGHT} >> ${WEIGHTFILE}
		else
			echo \'${STORAGENODE[$handle]}\' '=>' ${WEIGHT}, >> ${WEIGHTFILE}
		fi

		#echo ${STORAGENODE[$handle]}:${disk}:${load}:${cpu}:${swap}
	fi

	handle=$(($handle+1))
done

echo ');' >> ${WEIGHTFILE}
echo '?>' >> ${WEIGHTFILE}

#echo ${STORAGENODE[@]}
#echo ${MAXDISKUSE}
