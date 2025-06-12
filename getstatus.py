import psutil


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
