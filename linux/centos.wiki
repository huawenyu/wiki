# Quick Start:

## [Actually it's not work] Install from centos.org's cloud kvm image

    ### https://www.theurbanpenguin.com/using-cloud-images-in-kvm/

    ### https://cloud.centos.org/centos/7/images/
    ### $ wget https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1907.qcow2

    ### query current image's size
    $ qemu-img info bionic-server-cloudimg-amd64.img

    ### Extend image's size
    $ qemu-img resize bionic-server-cloudimg-amd64.img 60G
    $ qemu-img info bionic-server-cloudimg-amd64.img

## config network [from command line]

### commandline: GUI Mode
    https://lintut.com/how-to-setup-network-after-rhelcentos-7-minimal-installation/

    $ nmcli d       <=== list network device
    $ nmtui         <=== open command-line's network manager

    <Offcouse you can Set ip adress using DHCP>
        $ service network restart
        $ systemctl restart network

### command mode

        Network interface config files are located in /etc/sysconfig/network-scripts/ directory.
        Open ifcfg-enp0s17 file ( For interface enp0s17 ) and you can see the content like below.

        [root@krizna ~]# vi /etc/sysconfig/network-scripts/ifcfg-enp0s17
            TYPE=Ethernet
            BOOTPROTO=none
            DEFROUTE=yes
            IPV4_FAILURE_FATAL=no
            IPV6INIT=yes
            IPV6_AUTOCONF=yes
            IPV6_DEFROUTE=yes
            IPV6_FAILURE_FATAL=no
            NAME=enp0s17
            UUID=7f1aff2d-b154-4436-9497-e3a4dedddcef
            ONBOOT=no
            HWADDR=00:0C:29:A1:B5:D6
            PEERDNS=yes
            PEERROUTES=yes
            IPV6_PEERDNS=yes
            IPV6_PEERROUTES=yes

## sudoer

The `sudo` command provides a mechanism for granting administrator privileges, ordinarily only available to the root user, to normal users.

Log in to your server as the root user.

    $ ssh root@server_ip_address

      # adduser username
      # passwd username

      ### By default, on CentOS, members of the wheel group have sudo privileges.
      # usermod -aG wheel username

      ### Test sudo access on new user account
      # su - username

## Development Env

    $ sudo yum group list
    $ sudo yum groupinstall "Development Tools"
    $ sudo yum groupinstall "Development Libraries" "Additional Development"
    $ sudo yum install libstdc++.i686

  [1]: https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-centos-quickstart
