import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from datetime import datetime
import sys

import getstatus as st
import getAPI

# 初始化OLED屏幕
serial = i2c(port=0, address=0x3C)
device = ssd1306(serial)


count_3 = 0
count_3600 = 0
page =False


weather, temp, humidity = getAPI.getWeather()
total_memory, used_memory, memory_percent = st.get_memory_info()
total_swap, used_swap, swap_percent = st.get_swap_info()
total_disk, used_disk, disk_percent = st.get_disk_info()

while True:
    count_3 += 1
    if count_3 % 3 == 0:

        total_memory, used_memory, memory_percent = st.get_memory_info()
        total_swap, used_swap, swap_percent = st.get_swap_info()
        total_disk, used_disk, disk_percent = st.get_disk_info()
        count_3 = 0
        page = not page #三秒值

    count_3600 += 1
    if count_3600 % 3600 == 0:
        weather, temp, humidity = getAPI.getWeather()

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    with canvas(device) as draw:
        draw.text((0, 0), f'{current_date} - {current_time}', fill="white")
        draw.text((0, 10), f'Cpu Usage: {st.get_cpu_usage()}%', fill="white")


        if page:
            draw.text((0, 20), f'System Status ---------', fill="white")
            draw.text((0, 30),
                      f'Mem: {(used_memory / total_memory) * 100:.1f}% Ava-{st.formatsize(total_memory-used_memory)}%',
                      fill="white")
            draw.text((0, 40),
                      f'Swap: {(used_swap / total_swap) * 100:.1f}%',
                      fill="white")
            draw.text((0, 50),
                      f'Disk: {st.formatsize(total_disk)}/{st.formatsize(used_disk)} - {(used_disk / total_disk) * 100:.2f}%',
                      fill="white")
        else:
            draw.text((0, 20), f'Weather Status ---------', fill="white")
            draw.text((0, 30), f'Weather: {getAPI.get_weather_en_description(weather)}', fill="white")
            draw.text((0, 40), f'Temperature: {temp} C', fill="white")
            draw.text((0, 50), f'Humidity: {humidity}', fill="white")
        print("Page", (count_3 // 3) % 2)

    time.sleep(1)