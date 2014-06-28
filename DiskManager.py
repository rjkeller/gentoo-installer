#!/usr/bin/env python
import fileinput
import sys
import os


class DiskManager:
    """
    Provides a bunch of operations to format and manage hard disks.

    One cool thing that this class does is allow you to generate a fstab file
    based on disk formatting operations conducted earlier using this class. This
    is helpful when installing a new Gentoo installation.
    """

    def __init__(self):
        self.mountPoints = []

    def formatAndConfigSpareDisk(self, disk):
        """Configures a new spare hard disk and formats it."""
        self.disk_mkdisk(disk, ("mklabel gpt"
            "unit mib"
            "mkpart primary 1 -1"
            "name 1 rootfs"
            "print"
            "quit"))

        os.system("mkfs.ext4 " + disk + "1")
        os.system("mkdir -p /mnt/" + disk + "1")
        os.system("mount " + disk + "1 /mnt/" + disk + "1")
        
        print("Done! Disk mounted on /mnt/" + disk + "1. Please update Fstab")
        
    

    def formatStartupDisk(self, serverConfig):
        """
        Formats a disk to be a startup disk (i.e., has grub and swap
        partitions on it)
        """
        disks = serverConfig['disks'].split(",")
        
        if serverConfig['enableRaid']:
            diskDeviceNames = ""
            for disk in disks:
                diskDeviceNames += disk + "NUM "
                self.disk_mkdisk(disk, ("mklabel gpt"
                    "unit mib"
                    "mkpart primary 1 3"
                    "set 1 bios_grub on"
                    "name 1 boot"
                    "mkpart primary 3 -1"
                    "name 2 llvm"
                    "set 2 raid on"
                    "print"
                    "quit"))
            
            numDisks = len(disks)
            os.system("mdadm --create /dev/md0 --level=1 --raid-devices=" + numDisks + " " + diskDeviceNames.replace('NUM', 2))
            os.system("mdadm --assemble --scan")

            os.system("pvcreate /dev/md0")
            os.system("vgcreate vg-sata /dev/md0")
            os.system("lvcreate -L100M -n boot vg-sata")
            os.system("lvcreate -L512M -n swap vg-sata")
            os.system("lvcreate -l 100%FREE -n root vg-sata")

            self.disk_mkfs("/dev/vg-sata/root", "/", "std", "0 1")
            self.disk_mkfs("/dev/vg-sata/boot", "/boot", "boot")
            self.disk_mkswap("/dev/vg-sata/swap")

            os.system("mdadm --detail --scan > /etc/mdadm.conf")
        else:
            self.disk_mkdisk(disks[0], ("mklabel gpt\n"
                "unit mib\n"
                "mkpart primary 1 3\n"
                "set 1 bios_grub on\n"
                "name 1 grub\n"
                "mkpart primary 3 131\n"
                "name 2 boot\n"
                "mkpart primary 131 643\n"
                "name 3 swap\n"
                "mkpart primary 643 -1\n"
                "name 4 rootfs\n"
                "print\n"
                "quit\n"))
            self.disk_mkfs(disks[0] + '4', "/", "std", "0 1")
            self.disk_mkfs(disks[0] + '2', "/boot", "boot")
            self.disk_mkswap(disks[0] + '3')

            for disk in disks:
                self.disk_mkdisk(disk, ("mklabel gpt\n"
                    "unit mib\n"
                    "mkpart primary 1 -1\n"
                    "print\n"
                    "quit\n"))
                self.disk_mkfs(disk + '1', "/var/lib/mysql", "std", "0 2")

    def disk_mkdisk(self, device, options):
        """
        Creates partitions on the specified disk with the specified options.
        """
        os.system("echo \"" + options + "\" > /tmp/parted")
        os.system("parted -s -a optimal " + device + " < /tmp/parted")
        os.system("rm -f /tmp/parted")

    def disk_mkfs(self, device, mntPoint, type, options = ''):
        """
        Formats the hard disk using parted with the specified options.
        """
        os.system("mkfs.ext4 " + device)
        os.system("mkdir -p /mnt/gentoo" + mntPoint)
        os.system("mount " + device + " /mnt/gentoo" + mntPoint)

        self.mountPoints.append({
            'device': device,
            'mountPoint': mntPoint,
            'type': type
        })

    def disk_mkswap(self, device):
        """
        Formats and enables a swap partition on this disk.
        """
        os.system("mkswap " + device)
        os.system("swapon " + device)

        self.mountPoints.append({
            'device': device,
            'type': 'swap'
        })

    def createFstab(self):
        """
        Creates an fstab file based on disk operations conducted up until now.
        """
        cmd = "echo '"
        incr = 1
        for mountPoint in self.mountPoints:
            if mountPoint['type'] == "sawp":
                cmd += mountPoint['device'] + "\tnone\tswap\tsw\t0 0\n"
            elif mountPoint['type'] == "boot":
                cmd += mountPoint['device'] + "\t" + mountPoint['mountPoint'] + "\t" + self.fileSystem + "\tnoauto,noatime\t1 2\n"
            else:
                cmd += mountPoint['device'] + "\t" + mountPoint['mountPoint'] + "\t" + self.fileSystem + "\tnoatime\t0 " + incr + "\n"
            incr += 1
        cmd += "' > /etc/fstab"
        os.system(cmd)
        os.system("rm -rf /etc/mtab")
        os.system("ln -s /proc/self/mounts /etc/mtab")


"""
------------------------------------------------------------------------------
 MAIN FUNCTION
------------------------------------------------------------------------------
"""

if __name__ == '__main__':
    dm = DiskManager()

    if sys.argv[1] == "newdisk":
        dm.formatAndConfigSpareDisk(sys.argv[2])
