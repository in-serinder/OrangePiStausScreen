import display
import asyncio
# import psutil

# import getstatus

if __name__ == '__main__':
    asyncio.run(display.update_display())
    # disks = psutil.disk_partitions()
    # for disk in disks:
    #     print(psutil.disk_usage(disk.mountpoint))
    # print(getstatus.get_disks_usage())