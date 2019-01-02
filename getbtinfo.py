#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
from plistlib import *
import ConfigParser

def DevMenu(m):
	try:
		os.system("clear")
		print('Which one do you want to export?')
		i = 1
		c = []
		for dname in m:
			print (str(i) + ': ' + dname)
			c.append(dname)
			i += 1;
		print(str(i) + ': Exit')
		x = input('Please enter a number: ')
		if x == i:
			return 'Exit'
		return m[c[None if x == 0 else x - 1]]
	except:
		return None


if __name__ == "__main__":

	ostype = ['windows', 'linux']
	para = {'LTK' : [True, False], 'RAND' : [True, False], 'EDIV': [True, True]}
	workdir = os.path.expanduser('~') + '/Desktop/BTFix'
	if not os.path.exists(workdir):
		os.makedirs(workdir)

	# Get BT device
	btdev = workdir + '/btdev.plist'
	subprocess.check_output('defaults export /Library/Preferences/com.apple.Bluetooth.plist ' + btdev, shell=True)
	subprocess.check_output('plutil -convert xml1 ' + btdev, shell=True)
	pldev = readPlist(btdev)

	# Get BT data
	blued = workdir + '/blued.plist'
	subprocess.check_output('sudo defaults export /var/root/Library/Preferences/com.apple.bluetoothd.plist ' + blued, shell=True)
	subprocess.check_output('sudo plutil -convert xml1 ' + blued, shell=True)
	pl = readPlist(blued)

	DevNameDict = {}     # Menu
	for adapter in pl['SMPDistributionKeys']:
		for device in pl['SMPDistributionKeys'][adapter]:
			for CacheDev in pldev['DeviceCache']:
				if CacheDev == device :
					DevNameDict.update({pldev['DeviceCache'][CacheDev]['Name']:CacheDev})
	while True:
		ExpMac = DevMenu(DevNameDict)
		if ExpMac == 'Exit':
			print('Exit...')
			exit(1)
		if ExpMac != None:
			break

	cfg = ConfigParser.ConfigParser()
	
	for adapter in pl['SMPDistributionKeys']:
		for device in pl['SMPDistributionKeys'][adapter]:
			if ExpMac == device:
				cfg.add_section('general')
				cfg.set('general', 'adapter', adapter)
				cfg.set('general', 'device', device)
				cfg.add_section(ostype[0])
				cfg.add_section(ostype[1])
				for item in pl['SMPDistributionKeys'][adapter][device].keys():
					if para.has_key(item) :
						for i in range(0, len(ostype)):
							if para[item][i]:
								cfg.set(ostype[i], item, pl['SMPDistributionKeys'][adapter][device][item].data[::-1].encode('hex'))
							else:
								cfg.set(ostype[i], item, pl['SMPDistributionKeys'][adapter][device][item].data.encode('hex'))
	with open(workdir + '/BTInfo.ini', 'wb') as f:
		cfg.write(f)
	print('done.')
