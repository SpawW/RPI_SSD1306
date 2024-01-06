#!/usr/bin/env python3
# Copyright (c) 2017 Adafruit Industries
# Author: Adail Horst
# Some ideas came from youtube videos and from this repo: https://github.com/xxlukas42/RPI_SSD1306
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time
import psutil
import docker
import socket
import netifaces
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

def get_system_uptime():
    boot_time = psutil.boot_time()

    uptime_seconds = time.time() - boot_time

    uptime_days, remainder = divmod(uptime_seconds, 86400)
    uptime_hours, remainder = divmod(remainder, 3600)
    uptime_minutes, uptime_seconds = divmod(remainder, 60)

    return f"{int(uptime_days)} dias, {int(uptime_hours)}:{int(uptime_minutes)}:{int(uptime_seconds)}"
    
def get_private_ip():
    default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    private_ip = netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]['addr']
    return private_ip

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_disk_usage():
    return psutil.disk_usage('/').percent

def get_memory_usage():
    return psutil.virtual_memory().percent

def draw_icon(draw, x, top, unicode_code, font, fill=255):
    draw.text((x, top), chr(unicode_code), font=font, fill=fill)

def get_running_containers():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        return str(len(containers)) 
    except ImportError:
        return "Docker não instalado"

def display_info(carousel_interval=2):
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, rotate=0)

    font2 = ImageFont.truetype('fonts/fontawesome-webfont.ttf', 14)

    icons = [61888, 62152, 62171, 61899, 61931, 61463]  

    message_order = [0, 1, 2, 3]

    while True:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")  
            print_info(draw,message_order[0],0,f"{get_cpu_usage()}%",icons[0],font2)
            print_info(draw,message_order[0],1,f"{get_running_containers()}",icons[3],font2)
            # todo: create a method to get icon from a file (maybe using svg)
            # print_info(draw,message_order[0],1,f"{get_running_containers()}",icons[3],font2,image_path = "./images/docker.png")
            print_info(draw,message_order[1],0,f"{get_memory_usage()}%",icons[2],font2)
            print_info(draw,message_order[1],1,f"{get_disk_usage()}%",icons[1],font2)
            print_info(draw,message_order[2],0,f"{get_private_ip()}",icons[4],font2)
            print_info(draw,message_order[3],0,f"{get_system_uptime()}",icons[5],font2)

        # Rotate messages in display and wait
        message_order = rotate_array(message_order)
        time.sleep(carousel_interval)

def rotate_array(arr):
    if len(arr) < 2:
        return arr

    rotated_arr = [arr[-1]] + arr[:-1]
    return rotated_arr

def print_info(draw, line, col, text, icon, font, image_path = ""):
    pos_line = line * 16
    pos_col  = [20, 70][col]
    if image_path == "":
        draw_icon(draw, pos_col-20, pos_line, icon, font)
    else:
        draw_image(draw, pos_col-20, pos_line, image_path, (20,20))
    draw.text((pos_col, pos_line), text, fill="white")

def draw_image(draw, x, y, icon_path, icon_size):
    try:
        icon = Image.open(icon_path).convert("1")
        icon = icon.resize(icon_size)
        draw.bitmap((x, y), icon, fill="black")
    except IOError:
        print(f"Erro: Não foi possível carregar o ícone em {icon_path}")

if __name__ == "__main__":
    display_info()
