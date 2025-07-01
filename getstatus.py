import subprocess
from datetime import datetime
import datetime as dt
import re
import urllib

import psutil
import socket

def formatsize(byte):
    if byte >= 1024 * 1024 * 1024:
        return f'{byte / (1024 * 1024 * 1024):.1f} GiB'

    if byte >= 1024 * 1024:
        return f'{byte / (1024 * 1024):.1f} MiB'

    if byte >= 1024:
        return f'{byte / 1024:.1f} KiB'

    return f'{byte:.2f} B'



def get_memory_info():
    # 获取内存信息
    mem = psutil.virtual_memory()
    if mem :
        total_memory = mem.total
        used_memory = mem.used
        memory_percent = mem.percent
        return total_memory, used_memory, memory_percent
    else:
        return 0, 0, 0


def get_swap_info():

    swap = psutil.swap_memory()
    if swap :
        total_swap = swap.total
        used_swap = swap.used
        swap_percent = swap.percent
        return total_swap, used_swap, swap_percent
    else:
        return 0, 0, 0


def get_disk_info():

    disk = psutil.disk_usage('/')
    if disk:
        total_disk = disk.total
        used_disk = disk.used
        disk_percent = disk.percent
        return total_disk, used_disk, disk_percent
    else :
        return 0, 0, 0

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_interent_status():
    try:
        urllib.request.urlopen('https://www.archlinux.org')
        return True
    except:
        return False

def get_ip_addresses():
    ip_addresses = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                if not addr.address=="127.0.0.1":
                    ip_addresses.append(f'{interface}-{addr.address}')

    return ip_addresses


def get_alldisk_usage():
    total_size = 0
    used_size = 0

    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        total_size += usage.total
        used_size += usage.used

    return total_size, used_size


def get_cpu_temp():

    try:
        temps = subprocess.check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"]).decode("utf-8")
        cpu_temp = float(temps) / 1000
        return f'{cpu_temp:.2f}'
    except Exception as e:
        print(f"get Cpu Temperature Failed: {e}")
        return None

def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    days = uptime.days
    seconds = uptime.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{days}D {hours}H {minutes}M {seconds}S"


def get_disks_usage():
    disks=[]
    disk_usage = psutil.disk_partitions()
    for partition in disk_usage:
        if not partition.mountpoint == '/var/log.hdd': #忽略
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append(f'{partition.mountpoint}: {(usage.used/usage.total)*100:.2f} %')

    return disks