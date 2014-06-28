#!/usr/bin/env python
import fileinput
import sys

///<summary>
///Provides a bunch of operations to format and manage hard disks.
///
///One cool thing that this class does is allow you to generate a fstab file
///based on disk formatting operations conducted earlier using this class. This
///is helpful when installing a new Gentoo installation.
///</summary>
class BuildKernel:

    def compileNewKernel(self, kernelType, initSettings):
        f = fopen('/etc/superGentoo/kernel', 'w')
        f.write(kernelType + "," + initSettings)
        f.close()
        
        os.system("emerge " + kernelType)

        os.system("mv /usr/src/.config /usr/src/linux/.config")
        os.system("touch /usr/src/linux/.config")
        
        os.system("cd /usr/src/linux")
        os.system("make")
        os.system("make modules_install")
        os.system("cp arch/x86_64/boot/bzImage /boot/kernel-`find /usr/src -name linux-3* | awk -Flinux- '{print \$NF }'`")

    def upgradeKernel(self):
        kernelData = open('/etc/superGentoo/kernel').read(1000).split(",")
        os.system("emerge --update ". kernelData[0])
        os.system()

//--------------------------------------------------------------------------//
// MAIN FUNCTION
//--------------------------------------------------------------------------//

if __name__ == '__main__':
    bk = BuildKernel()

    if sys.argv[1] == "upgrade":
        bk.upgradeKernel()
    elif sys.argv[1] == "newKernel":
        bk.compileNewKernel(sys.argv[2], sys.argv[3])
