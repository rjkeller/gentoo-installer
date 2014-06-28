#!/usr/bin/env python
import fileinput
import sys

class SystemD:
    def getName(self):
        return "systemd"
    def activateService(self, serviceName):

        #-- Build an init script if necessary
        if serviceName == "iptables":
            os.system(("echo 'echo \"[Unit]"
                "Description=Packet Filtering Framework"
                ""
                "[Service]"
                "Type=oneshot"
                "ExecStart=/sbin/iptables-restore /var/lib/iptables/rules-save"
                "ExecStop=/sbin/iptables -F"
                "RemainAfterExit=yes"
                ""
                "[Install]"
                "WantedBy=multi-user.target"
                '" > /usr/lib/systemd/system/iptables.service'))

        elif serviceName == "app-emulation/open-vm-tools":
            os.system(("echo 'echo \"[Unit]"
                "Description=HGFS Mount"
                ""
                "[Service]"
                "Type=oneshot"
                "ExecStart=/sbin/modprobe vmhgfs"
                "ExecStart=/bin/mount -t vmhgfs .host:/ /mnt/hgfs"
                "ExecStop=/bin/umount /mnt/hgfs"
                "RemainAfterExit=yes"
                ""
                "[Install]"
                "WantedBy=multi-user.target"
                "\" > /usr/lib/systemd/system/hgfs.service"))


        #-- activate the service
        
        # translate some packages to systemd service name
        if serviceName == "ntp":
            serviceName = "ntpd"
        elif serviceName == "app-emulation/open-vm-tools":
            serviceName = "hgfs"
        elif serviceName == "dev-db/redis":
            serviceName = "redis"
        elif serviceName == "www-servers/apache":
            serviceName = "apache2"
        elif serviceName == "sys-fs/mdadm":
            serviceName = "mdadm"
        elif serviceName == "dev-db/mongodb":
            serviceName = "mongodb"
        elif serviceName == "mariadb":
            serviceName = "mysqld"
        elif serviceName == "mysql":
            serviceName = "mysqld"
  

        # some services need custom handling
        if serviceName == "syslog-ng":
            os.system("ln -s /usr/lib/systemd/system/" + serviceName + ".service /etc/systemd/system/syslog.service")
            os.system("ln -s /usr/lib/systemd/system/" + serviceName + ".service /etc/systemd/system/multi-user.target.wants/")
        elif serviceName == "lvm2":
            os.system("ln -s /usr/lib/systemd/system/lvm2-lvmetad.service /etc/systemd/system/multi-user.target.wants/")
            os.system("ln -s /usr/lib/systemd/system/lvm2-monitor.service /etc/systemd/system/multi-user.target.wants/")
        elif serviceName == "app-emulation/libvirt":
            os.system("ln -s '/usr/lib64/systemd/system/libvirtd.service' '/etc/systemd/system/multi-user.target.wants/libvirtd.service'")
            os.system("ln -s '/usr/lib64/systemd/system/libvirt-guests.service' '/etc/systemd/system/multi-user.target.wants/libvirt-guests.service'")
        else:
            os.system("ln -s /usr/lib/systemd/system/" + serviceName + ".service /etc/systemd/system/multi-user.target.wants/")

    def activateNetwork(self, server, ipAddress = None):
        if ipAddress is None:
            os.system(("echo 'echo \"[Unit]"
                "Description=Static network service"
                "After=local-fs.target"
                "Documentation=man:ifconfig(8)"
                "Documentation=man:route(8)"
                ""
                "[Service]"
                "Type=oneshot"
                "RemainAfterExit=yes"
                "ExecStart=/bin/ifconfig " + server['networkInfo']['eth0Name'] + " " + server['networkInfo']['publicIp'] + " broadcast " + server['networkInfo']['broadcast'] + " netmask " + self.serverConfig['networkInfo']['netmask'] + " up"
                "ExecStart=/bin/route add default gw " + self.serverConfig['networkInfo']['gateway'] + ""
                ""
                "[Install]"
                "WantedBy=multi-user.target"
                '" > /usr/lib/systemd/system/network.' + server['networkInfo']['eth0Name'] + '.service'))

        else:
            #if this is a DHCP connection
            os.system(("echo 'echo \"[Unit]"
                "Description=DHCP on " + server['networkInfo']['eth0Name'] + ""
                "After=basic.target"
                ""
                "[Service]"
                "Type=oneshot"
                "RemainAfterExit=yes"
                "ExecStart=/bin/ifconfig " + server['networkInfo']['eth0Name'] + " up"
                "ExecStart=/sbin/dhcpcd -B " + server['networkInfo']['eth0Name'] + ""
                ""
                "[Install]"
                "WantedBy=multi-user.target"
                "\" > /usr/lib/systemd/system/network." + server['networkInfo']['eth0Name'] + ".service"))

        os.system("ln -s /usr/lib/systemd/system/network." + server['networkInfo']['eth0Name'] + ".service /etc/systemd/system/multi-user.target.wants/")
