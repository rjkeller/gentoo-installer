
class InstallerConfig:
    def __init__(self, serverConfig):
        self.serverConfig = serverConfig
        self.mountPoints = []
        self.initManager = SystemD()
        self.filesystem = "ext4"

    # self.serverConfig['networkInfo']['eth0Name']
    # self.serverConfig['networkInfo']['publicIp']
    # self.serverConfig['networkInfo']['broadcast']
    # self.serverConfig['networkInfo']['netmask']
    # self.serverConfig['networkInfo']['gateway']
    # self.serverConfig['networkInfo']['nameserver']
    # self.serverConfig['disks']
    # self.serverConfig['enableRaid']
    # self.serverConfig['hostname']

    def activateLocalNetwork(self):
        try:
            os.system("ifconfig " + self.serverConfig['networkInfo']['eth0Name'] + " " + self.serverConfig['networkInfo']['publicIp'] ." broadcast ". self.serverConfig['networkInfo']['broadcast'] ." netmask ". self.serverConfig['networkInfo']['netmask'] ." up")
            os.system("route add default gw " + self.serverConfig['networkInfo']['gateway'])
			os.system('echo "nameserver ' + self.serverConfig['networkInfo']['nameserver'] + '" > /etc/resolv.conf');
			
        except IndexError:

    def syncSystemClock:
        os.system("service ntpd stop")
        os.system("ntpdate -s time.nist.gov")
        os.system("service ntpd start")
    
	
	def installStage3(self, type):
	    os.system("cd /mnt/gentoo")
	    
	    if type == "amd64-hardened+nomultilib":
			os.system("wget $( echo http://distfiles.gentoo.org/releases/amd64/autobuilds/`curl http://distfiles.gentoo.org/releases/amd64/autobuilds/latest-stage3-amd64-hardened+nomultilib.txt -q | tail -n 1` )")
		elif type == "amd64-nomultilib":
			os.system("wget $( echo http://distfiles.gentoo.org/releases/amd64/autobuilds/`curl http://distfiles.gentoo.org/releases/amd64/autobuilds/latest-stage3-amd64-nomultilib.txt -q | tail -n 1` )")

		os.system("tar xjpf stage3*.tar.bz2")
		os.system("rm -rf stage3*.tar.bz2")

		os.system("echo \"nameserver 8.8.8.8\" > /mnt/gentoo/etc/resolv.conf")
		os.system("wget '' -O /mnt/gentoo/usr/src/.config")

        os.system('mount -t proc proc /mnt/gentoo/proc')
        os.system('mount --rbind /sys /mnt/gentoo/sys')
        os.system('mount --rbind /dev /mnt/gentoo/dev')
        os.system('chroot /mnt/gentoo /bin/bash')

    def installPortage:
        os.system("wget 'http://master/config_files/12/portage' -O /etc/portage/make.conf")
        os.system("echo 'sys-apps/dbus -systemd' > /etc/portage/package.use")
        os.system("echo 'sys-kernel/gentoo-sources ~amd64' > /etc/portage/package.accept_keywords")
        os.system("echo '' > /etc/portage/package.mask")
        os.system("emerge-webrsync")
        os.system("emerge --sync")
    
    def eselect(self, item, num):
        if item == "gcc-config":
            os.system("gcc-config -l")
            os.system("gcc-config " + num)
        else:
            os.system("eselect " + item + " list")
            os.system("eselect " + item + " set " + num)
        os.system("env-update && source /etc/profile")
    
    def setTonezone(self, timezone):
        os.system("echo 'America/Los_Angeles' > /etc/timezone")
        os.system("emerge --config sys-libs/timezone-data")
    
    def setLocale(self, locale):
        os.system(("echo 'en_US ISO-8859-1"
            "en_US.UTF-8 UTF-8' > /etc/locale.gen"));
        os.system("env-update && source /etc/profile")
        os.system("locale-gen")

    def multiEmerge(self, allApps):
        cmdToRun = "emerge "
        for app in allApps:
            cmdToRun += app + " "
        os.system(cmdToRun)
        
        for app in allApps:
            self.emerge(app, true)
    
    def emerge(self, app, configOnly = False):
        # Compile application phase
        if app == "pip:aws":
            os.system("pip install awscli")
            os.system("mkdir -p /root/.aws")
            os.system(('echo "[default]'
                'region = us-west-1'
                'aws_access_key_id = AKIAIFQQ37ZPD4MBBH5A'
                'aws_secret_access_key = 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'
                '" > /root/.aws/config'));
        elif app == "sshd":

        elif app = "php:composer":
            os.system("curl -sS https://getcomposer.org/installer | php -- --install-dir=/bin")
            os.system("mv /bin/composer.phar /usr/local/bin/composer")
        
        else:
            if not configOnly:
                os.system("emerge " + app)
        
        # Activate Service Phase
        if app in ('ntp',
            'app-emulation/open-vm-tools',
            'cronie',
            'sshd',
            'iptables',
		    'fail2ban',
		    'dev-db/redis',
		    'www-servers/apache',
		    'app-antivirus/clamav',
		    'dev-db/mongodb',
		    'mariadb',
		    'mysql',
		    'iptables',
		    'syslog-ng',
		    'sys-fs/mdadm',
		    'lvm2',
		    'app-emulation/libvirt'):
		    self.initManager.activateService(app)
            
		# Post-config (where applicable)
		if app == 'app-emulation/open-vm-tools':
		    os.system("mkdir -p /mnt/hgfs")
		elif app == "sys-fs/mdadm":
		    os.system("mdadm --examine --scan > /etc/mdadm.conf")
		elif app == "conky":
		    os.system("rm -rf /etc/conky/conky.conf")
		    os.system("wget 'http://71.19.151.36/conky.conf' -O /etc/conky/conky.conf")
		elif app == "genkernel":
		    os.system("rm /usr/share/genkernel/arch/x86_64/kernel-config")
		    os.system("ln -s /usr/src/linux/.config /usr/share/genkernel/arch/x86_64/kernel-config")
        elif app == "mariadb":
            os.system("emerge --config dev-db/mariadb")
        elif app == "app-forensics/chkrootkit":
            os.system("echo '0 3 * * * /usr/sbin/chkrootkit\n' >> /var/spool/cron/crontabs/root")
            os.system("chown root:crontab /var/spool/cron/crontabs/root")
        elif app == "sudo":
            os.system("chmod +w /etc/sudoers")
            os.system("echo '%admin ALL=(ALL) ALL\n' >> /etc/sudoers")
            os.system("chmod -w /etc/sudoers")
        elif app == "app-antivirus/clamav":
            os.system("paxctl -m /usr/sbin/clamd /usr/bin/freshclam /usr/bin/clamconf")
            os.system("freshclam")
        elif app == "www-servers/apache":
            os.system(("echo '"
                ""
                "ServerName " + self.serverConfig['hostname']
                "KeepAlive On"
                "MaxKeepAliveRequests 100"
                "KeepAliveTimeout 15"
                ""
                "StartServers       8"
                "MinSpareServers    5"
                "MaxSpareServers   20"
                "ServerLimit      256"
                "MaxClients       256"
                "MaxRequestsPerChild  4000"
                ""
                "' >> /etc/apache2/httpd.conf"))
            os.system("sed -i 's/-D DEFAULT_VHOST -D INFO/-D DEFAULT_VHOST -D INFO -D PHP5/g' /etc/conf.d/apache2")
    
    def setInitManager(self, manager):
		if manager.getName == "systemd":
		    os.system(("echo '"
		        "sys-apps/dbus -systemd' >> /etc/portage/package.use"))
		    self.emerge(manager.getName)
		    os.system("sed -i 's/sys-apps\/dbus -systemd/ /g' /etc/portage/package.use")
		    os.system("emerge sys-apps/dbus")
		else:
		    self.emerge(manager.getName)
		self.initManager = manager
	
	def updateAll:
	    os.system("emerge --update --deep --with-bdeps=y @world")
	    os.system("emerge @preserved-rebuild")
	    os.system("emerge --changed-use --deep world")
	
    def installNetwork(self):
        os.system("echo '". $this->_server->hostname ."' > /etc/hostname")
        os.system("echo 'hostname=\"". $this->_server->hostname ."\"' > /etc/conf.d/hostname")
        os.system("echo \"127.0.0.1 localhost   ". $this->_server->hostname ."\n::1     localhost\n\" > /etc/hosts")
        os.system("cd /etc/conf.d")
        
        try:
            self.initManager.activateNetwork(self.server, self.serverConfig['networkInfo']['publicIp'])
		except IndexError:
		    this.emerge("net-misc/dhcpcd")

    def emergeIptablesFirewall(self, rules):
        self.emerge("iptables")
        
        os.system(('echo "*filter'
            ':INPUT ACCEPT [0:0]'
            ':FORWARD ACCEPT [0:0]'
            ':OUTPUT ACCEPT [82:5518]'
            ':RH-Firewall-1-INPUT - [0:0]'
            '-A INPUT -j RH-Firewall-1-INPUT'
            '-A INPUT -i ' + self.serverConfig['networkInfo']['eth0Name'] + ' -p tcp -m state --state RELATED,ESTABLISHED -j ACCEPT'
            '-A FORWARD -j RH-Firewall-1-INPUT'
            '-A OUTPUT -o ' + self.serverConfig['networkInfo']['eth0Name'] .' -m state --state RELATED,ESTABLISHED -j ACCEPT'
            '-A RH-Firewall-1-INPUT -i lo -j ACCEPT'
            '-A RH-Firewall-1-INPUT -p icmp -m icmp --icmp-type any -j ACCEPT'
            '-A RH-Firewall-1-INPUT -p esp -j ACCEPT'
            '-A RH-Firewall-1-INPUT -p ah -j ACCEPT'
            '-A RH-Firewall-1-INPUT -i ' + self.serverConfig['networkInfo']['eth0Name'] + ' -p tcp -m tcp --sport 1024:65535 --dport 443 -m state --state NEW -j ACCEPT'
            '-A RH-Firewall-1-INPUT -i ' + self.serverConfig['networkInfo']['eth0Name'] + ' -p tcp -m tcp --sport 1024:65535 --dport 80 -m state --state NEW -j ACCEPT'
            '-A RH-Firewall-1-INPUT -i ' + self.serverConfig['networkInfo']['eth0Name'] + ' -p tcp -m tcp --sport 1024:65535 --dport 22 -m state --state NEW -j ACCEPT'
            '-A RH-Firewall-1-INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT'
            '-A RH-Firewall-1-INPUT -s 71.19.151.32/28 -i ' + self.serverConfig['networkInfo']['eth0Name'] + ' -j ACCEPT'
            '-A RH-Firewall-1-INPUT -j REJECT --reject-with icmp-port-unreachable'
            'COMMIT" > /var/lib/iptables/rules-save'))

    def installGrub2(self, device):
        packagesToInstall = { "sys-boot/grub" }
        if self.server.enableRaid:
            packagesToInstall.append("sys-fs/mdadm")
            packagesToInstall.append("lvm2")
            packagesToInstall.append("genkernel")

        self.multiEmerge(packagesToInstall);

        if self.server.enableRaid:
            for dev in device:
                os.system("grub2-install " + dev)
            else:
                os.system("grub2-install " + device)
        
        os.system(("echo '"
            "GRUB_CMDLINE_LINUX=\"init=/usr/lib/systemd/systemd\""
            "' >> /etc/default/grub"))
        
        cmdLineDefault = "rootfstype=ext4";
        if self.server.enableRaid:
            cmdLineDefault += " domdadm dolvm"
        elif self.site.hasAppFlag("PIXO/SECURE_TOOLS"):
            cmdLineDefault += " apparmor=1 security=apparmor"
        
        os.system(("echo '"
            "GRUB_CMDLINE_LINUX_DEFAULT=\"" + cmdLineDefault + "\""
            "' >> /etc/default/grub"))
        
        # use GenKernel to create initramfs
        if self.server.enableRaid:
            os.system("genkernel --lvm --mdadm --install initramfs")
        
        os.system("grub2-mkconfig -o /boot/grub/grub.cfg")
        