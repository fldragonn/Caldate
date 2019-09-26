# ip manager
# by PITCA
# 2019.09.19

import wmi
import ctypes, sys

def change_IP(ipnum):
    # 네트워크 어댑터 설정
    nic_cfg = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True) 

    # 첫 네트워크 어댑터
    nic = nic_cfg[0]

    # IP address, subnetmask and gateway values should be unicode objects 
    ip = u'192.168.0.' + ipnum
    subnetmask = u'255.255.255.0' 
    gateway = u'192.168.0.1'

    # Set IP address, subnetmask and default gateway 
    # Note: EnableStatic() and SetGateways() methods require *lists* of values to be passed 
    nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask]) 
    nic.SetGateways(DefaultIPGateway=[gateway]) 

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Code of your program here
    ipnum = input("변경 IP주소: ")
    change_IP(ipnum)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
