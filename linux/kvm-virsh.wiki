# Quick Start:

## KVM - Fix Missing Default Network

error: Failed to start network default
error: internal error: Failed to initialize a valid firewall backend

https://blog.programster.org/kvm-missing-default-network

## [Actually it's not work] Install from centos.org's cloud kvm image

    ### https://www.theurbanpenguin.com/using-cloud-images-in-kvm/

    ### https://cloud.centos.org/centos/7/images/
    ### $ wget https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1907.qcow2

    ### query current image's size
    $ qemu-img info bionic-server-cloudimg-amd64.img

    ### Extend image's size
    $ qemu-img resize bionic-server-cloudimg-amd64.img 60G
    $ qemu-img info bionic-server-cloudimg-amd64.img

    $ sudo apt install virtinstall
    Once installed we can either create a script to import the disks or run directly from the command line. Here is an example using the disk I created previously:

    $ sudo virt-install \
            --name proxy1\
            --memory 1024 \
            --disk /var/lib/libvirt/images/proxy1.img,device=disk,bus=virtio \
            --disk /var/lib/libvirt/images/proxy1.iso,device=cdrom \
            --os-type linux \
            --os-variant ubuntu16.04 \
            --virt-type kvm \
            --graphics none \
            --network network=default, model=virtio \
            --import
    On running the command, the Virtual Machine meta-data will be created and the image will fire up. We will be connected to the console of the system. We can log in as the user Ubuntu with the password we supplied to cloud-config.

## virsh: save config

If you make lot of changes to your VM, it is recommended that you save the configurations.
```sh
    $ virsh dumpxml myRHELVM1 > myrhelvm1.xml

    ### you can always recreate your guest VM from this XML file, using virsh create command as shown below:
    $ virsh create myrhelvm1.xml
```

## virsh: delete a kvm-virtual-machine

```sh
    $ virsh shutdown myRHELVM2
    $ virsh destroy myRHELVM2
    $ virsh undefine myRHELVM2
    $ rm /var/lib/libvirt/images/myRHELVM2-disk1.img
    $ rm /var/lib/libvirt/images/myRHELVM2-disk2.img
```

## virsh: Add memory

```sh
    # virsh shutdown myRHELVM1
    # virsh edit myRHELVM1
        Change according to your requirement: <memory unit='KiB'>4194304</memory>
    # virsh create /etc/libvirt/qemu/myRHELVM1.xml
        Domain myRHELVM1 created from /etc/libvirt/qemu/myRHELVM1.xml

    # virsh dominfo myRHELVM1 | grep memory
        Max memory:     4194304 KiB
        Used memory:    2097152 KiB
    # virsh setmem myRHELVM1 4194304
    # virsh dominfo myRHELVM1 | grep memory
        Max memory:     4194304 KiB
        Used memory:    4194304 KiB
```

## virsh: Add cpu

```sh
    # virsh shutdown myRHELVM1
    # virsh edit myRHELVM1
        Change according to your requirement: <vcpu placement='static'>4</vcpu>
    # virsh create /etc/libvirt/qemu/myRHELVM1.xml
        Domain myRHELVM1 created from /etc/libvirt/qemu/myRHELVM1.xml

    # virsh dominfo myRHELVM1 | grep -i cpu
```

## virsh: Add Disk

1. First, create a virtual disk image

```sh
    # cd /var/lib/libvirt/images/
    # qemu-img create -f raw myRHELVM1-disk2.img 7G
        Formatting 'myRHELVM1-disk2.img', fmt=raw size=7516192768
```

2. Attach the virtual disk image to the VM
```sh
    # virsh attach-disk myRHELVM1 --source /var/lib/libvirt/images/myRHELVM1-disk2.img --target [vdb ](vdb )--persistent
        Disk attached successfully
    # virsh detach-disk myRHELVM1 vdb
        Disk detached successfully
```
