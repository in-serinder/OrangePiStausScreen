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
        socket.create_connection(("8.8.8.8",52),timeout=5)
        return True
    except OSError:
        return False

def get_ip_addresses():
    ip_addresses = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_addresses.append(addr.address)
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
    return psutil.sensors_temperatures().get('coretemp')