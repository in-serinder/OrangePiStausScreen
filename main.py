# -*- coding: utf-8 -*-

import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from datetime import datetime
import sys

import getstatus as st
import getAPI
import jsondeal as config


serial = i2c(port=config.get_i2c_port(), address=0x3C)
device = ssd1306(serial)



count_3 = 0
count_3600 = 0
timecount_5=0
pages_index =[0,1,2,3] #修改页面顺序
page_count =0
# lastpage=0


weather, temp, humidity, winddirection , windpower , reporttime = getAPI.getWeather()
total_memory, used_memory, memory_percent = st.get_memory_info()
total_swap, used_swap, swap_percent = st.get_swap_info()
total_disk, used_disk, disk_percent = st.get_disk_info()
total_alldisk,used_alldesk=st.get_alldisk_usage()

while True:

    timecount_5+=1
    count_3 += 1
    count_3600 += 1
    if count_3 % 3 == 0:

        total_memory, used_memory, memory_percent = st.get_memory_info()
        total_swap, used_swap, swap_percent = st.get_swap_info()
        total_disk, used_disk, disk_percent = st.get_disk_info()
        total_alldisk, used_alldesk = st.get_alldisk_usage()
        count_3 = 0
        # page = not page #三秒值
    # 页面切换
    if timecount_5 >= 5:
        page_count += 1
        timecount_5 = 0

    if page_count >=4 :
        page_count=0

    if count_3600 % 3600 == 0:
        weather, temp, humidity, winddirection , windpower , reporttime = getAPI.getWeather()

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    # print(getAPI.getWeathertemp())

    with canvas(device) as draw:
        draw.text((0, 0), f'{current_date} - {current_time}', fill="white")
        draw.text((0, 10), f'Cpu: {st.get_cpu_usage()}% ({st.get_cpu_temp()} C)', fill="white")




        if pages_index[page_count] == 0:
            draw.text((0, 20), f'System Status ---------', fill="white")
            draw.text((0, 30),
                      f'Mem: {(used_memory / total_memory) * 100:.1f}% Ava-{st.formatsize(total_memory-used_memory)}%',
                      fill="white")
            draw.text((0, 40),
                      f'Swap: {(used_swap / total_swap) * 100:.1f}%',
                      fill="white")
            draw.text((0, 50),
                      f'Disk: {st.formatsize(total_disk)}/{st.formatsize(used_disk)} ',
                      fill="white")



        if pages_index[page_count] == 1:

            draw.text((0, 20), f'Weather Status -P1------', fill="white")
            draw.text((0, 30), f'Weather: {getAPI.get_weather_en_description(weather)}', fill="white")
            draw.text((0, 40), f'Temperature: {temp} C', fill="white")
            draw.text((0, 50), f'Humidity: {humidity}', fill="white")



        if pages_index[page_count] == 2:

            draw.text((0, 20), f'Weather Status -P2------', fill="white")
            draw.text((0, 30), f'W.D: {getAPI.get_english_direction(winddirection)}', fill="white")
            draw.text((0, 40), f'W.P: {getAPI.extract_numbers(windpower)} ', fill="white")
            draw.text((0, 50), f'R.T: {reporttime}', fill="white")




        if pages_index[page_count] == 3:
            draw.text((0, 20), f'Extra Status ---------', fill="white")
            draw.text((0, 30),
                      f'Interent:{st.get_interent_status()} ',
                      fill="white")
            draw.text((0, 40),
                      f'IP: {st.get_ip_addresses()}',
                      fill="white")
            draw.text((0, 50),
                      f'Disk: {st.formatsize(total_alldisk)}/{st.formatsize(used_alldesk)}',
                      fill="white")

        # print("page",pages_index[page_count])
        # lastpage=pages_index[page_count]

    time.sleep(1)