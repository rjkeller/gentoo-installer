from InstallerConfig import InstallerConfig

config = {
  'disks': '/dev/sda',
  'enableRaid': False,
  'hostname': 'gdev',
}
installer = InstallerConfig(config)
installer.syncSystemClock()
