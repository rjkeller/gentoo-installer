from InstallerConfig import InstallerConfig
from DiskManager import DiskManager

config = {
  'arch': 'amd64',

  'disks': '/dev/sda',
  'enableRaid': False,
  'hostname': 'gdev',

  'numCpus': 4,
  'compileNative': True,
  'isLowMemoryEnvironment': False,

  'useFlags': "-ipv6 systemd -openrc apache2 php curl ruby_targets_ruby19 iptables mariadb"

}

installer = InstallerConfig(config)
diskManager = DiskManager()

#installer.syncSystemClock()

#diskManager.formatStartupDisk(config)

installer.installStage3("amd64-nomultilib")
#installer.installPortage()