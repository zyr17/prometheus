mkdir /textfile
# echo node_host_name{nodename=`cat /etc/hostname`,hostname=`cat /rootfs/etc/hostname`} `cat /rootfs/etc/hostname` > /textfile/node_host_name.prom
echo node_host_name{nodename=\"`cat /etc/hostname`\",hostname=\"`cat /rootfs/etc/hostname`\"} 1 > /textfile/node_host_name.prom
echo /bin/node_exporter "$@"
/bin/node_exporter "$@"
