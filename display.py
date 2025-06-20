# -*- coding: utf-8 -*-

import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from datetime import datetime

import asyncio

import getstatus as st
import getAPI
import jsondeal as config


serial = i2c(port=config.get_i2c_port(), address=0x3C)
device = ssd1306(serial)



count_3 = 0
count_3600 = 0
count_60 = 0
timecount_=0
pages_index =[0,1,2,3,4] #页面播放顺序
page_count =0
page_switch_time = config.get_switch_time()
# lastpage=0


weather, temp, humidity, winddirection , windpower , reporttime = getAPI.getWeather()
total_memory, used_memory, memory_percent = st.get_memory_info()
total_swap, used_swap, swap_percent = st.get_swap_info()
total_disk, used_disk, disk_percent = st.get_disk_info()
total_alldisk,used_alldesk=st.get_alldisk_usage()
network_list,interent_status = st.get_ip_addresses(),st.get_interent_status()
uptime = st.get_uptime()


async def update_data():
    global total_memory, used_memory, memory_percent
    global total_swap, used_swap, swap_percent
    global total_disk, used_disk, disk_percent
    global total_alldisk, used_alldesk


    total_memory, used_memory, memory_percent = st.get_memory_info()
    total_swap, used_swap, swap_percent = st.get_swap_info()
    total_disk, used_disk, disk_percent = st.get_disk_info()
    total_alldisk, used_alldesk = st.get_alldisk_usage()
    await asyncio.sleep(0)

async def update_weather():
    global weather, temp, humidity, winddirection , windpower , reporttime
    weather, temp, humidity, winddirection, windpower, reporttime = getAPI.getWeather()
    await asyncio.sleep(0)

async def update_network():
    global network_list, interent_status
    network_list, interent_status = st.get_ip_addresses(), st.get_interent_status()
    await asyncio.sleep(0)

####################################################################################################################
##########################################Main######################################################################
####################################################################################################################

async def update_display():
    global count_3,count_3600,timecount_,page_count,page_switch_time,count_60

    global total_memory, used_memory, memory_percent
    global total_swap, used_swap, swap_percent
    global total_disk, used_disk, disk_percent
    global total_alldisk, used_alldesk
    global weather, temp, humidity, winddirection, windpower, reporttime
    global network_list,interent_status
    global uptime


    while True:
        timecount_+=1
        count_3 += 1
        count_60 += 1
        count_3600 += 1
        if count_3 % 3 == 0:
            # total_memory, used_memory, memory_percent = st.get_memory_info()
            # total_swap, used_swap, swap_percent = st.get_swap_info()
            # total_disk, used_disk, disk_percent = st.get_disk_info()
            # total_alldisk, used_alldesk = st.get_alldisk_usage()
            await update_data()
            uptime = st.get_uptime()
            count_3 = 0

        # 页面切换
        if timecount_ >= page_switch_time:
            page_count += 1
            timecount_ = 0


        if page_count >=5 :
            page_count=0

        if count_60 >=60:
            await update_network()
            count_60 = 0

        if count_3600 % 3600 == 0:
            # weather, temp, humidity, winddirection , windpower , reporttime = getAPI.getWeather()
            await update_weather()

        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")

        # print(getAPI.getWeathertemp())

        with canvas(device) as draw:
            draw.text((0, 0), f'{current_date} - {current_time}', fill="white")
            draw.text((0, 10), f'Cpu Usage: {st.get_cpu_usage()}% ({st.get_cpu_temp()} C)', fill="white")




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
                draw.text((0, 30), f'WindDirection: {getAPI.get_english_direction(winddirection)}', fill="white")
                draw.text((0, 40), f'WindPower: {getAPI.extract_numbers(windpower)} ', fill="white")
                draw.text((0, 50), f'R.T: {reporttime}', fill="white")




            if pages_index[page_count] == 3:
                draw.text((0, 20), f'Extra Status ---------', fill="white")
                draw.text((0, 30),
                          f'Interent:{interent_status} ',
                          fill="white")
                draw.text((0, 40),
                          f'Uptime: {uptime}',
                          fill="white")
                draw.text((0, 50),
                          f'Disk: {st.formatsize(total_alldisk)}/{st.formatsize(used_alldesk)}',
                          fill="white")

            if pages_index[page_count] == 4:
                draw.text((0, 20), f'Network Status ---------', fill="white")
                for i,network in enumerate(network_list):
                    draw.text((0, 30 + i*10), f'{network}', fill="white")


#########################################################################################################


        # if pages_index[page_count] == 0:
        #     print( f'System Status ---------')
        #     print(f'Mem: {(used_memory / total_memory) * 100:.1f}% Ava-{st.formatsize(total_memory-used_memory)}%')
        #     print(f'Swap: {(used_swap / total_swap) * 100:.1f}%')
        #     print(f'Disk: {st.formatsize(total_disk)}/{st.formatsize(used_disk)} ')
        #
        #
        # if pages_index[page_count] == 1:
        #
        #     print( f'Weather Status -P1------')
        #     print(f'Weather: {getAPI.get_weather_en_description(weather)}')
        #     print( f'Temperature: {temp} C')
        #     print(f'Humidity: {humidity}')
        #
        #
        #
        #
        # if pages_index[page_count] == 2:
        #
        #     print( f'Weather Status -P2------')
        #     print(f'WindDirection: {getAPI.get_english_direction(winddirection)}')
        #     print(f'WindPower: {getAPI.extract_numbers(windpower)} ')
        #     print(f'R.T: {reporttime}')
        #
        #
        #
        #
        #
        # if pages_index[page_count] == 3:
        #     print(f'Extra Status ---------')
        #     print( f'Interent:{st.get_interent_status()} ')
        #     print(f'IP: {st.get_ip_addresses()}')
        #     print( f'Disk: {st.formatsize(total_alldisk)}/{st.formatsize(used_alldesk)}')
        #
        # if pages_index[page_count] == 4:
        #     print( f'NetWork Status --------')
        #     for networkitem in network_list:
        #         print(f'Network: {networkitem}')
        #
        #
        # print("page",pages_index[page_count])
            # lastpage=pages_index[page_count]

        time.sleep(1)




