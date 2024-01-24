#!/usr/bin/env python

# Programmatically upload firmwares via bootloader to the Asus DSL-N14U via command line.
# Requirements:
# pexpect pexpect-serialspawn pyserial requests requests-toolbelt rich

import time
import serial
import requests
import argparse
import threading
from pexpect.exceptions import TIMEOUT
from pathlib import Path
from rich.console import Console
from pexpect_serialspawn import SerialSpawn
import serial.tools.list_ports
from requests_toolbelt.multipart.encoder import MultipartEncoder

def expect_with_timeout(ss, pattern, timeout=1):
    if isinstance(pattern, list):
        pattern.insert(0, TIMEOUT)
    else:
        pattern = [TIMEOUT, pattern]
    return ss.expect(pattern, timeout=timeout)

def check_bldr_cmd(ss, timeout=1):
    ss.send('\r')
    return expect_with_timeout(ss, 'bldr>', timeout=timeout)

def upload(serial_port: str, firmware_path: Path, baudrate: int = 115200, ip_addr='192.168.2.1', logfile=None, interactive=True):
    console = Console()
    firmware_path = Path(firmware_path)
    if not firmware_path.exists():
        console.log('Could not open firmware file!')
    ser = serial.Serial(serial_port, baudrate)
    ss = SerialSpawn(ser, encoding='utf-8')
    if logfile:
        ss.logfile = open(logfile,'w')
    if not check_bldr_cmd(ss):
        console.log('Not in bootloader or bootloader not responding. Please reboot the router.')
        with console.status('Awaiting reboot...'):
            if not expect_with_timeout(ss, 'Press any key in 1 secs to enter boot command mode.', timeout=120):
                console.log('Timed out waiting for reboot!')
                ser.close()
                return False
            if not check_bldr_cmd(ss, timeout=10):
                console.log('Cannot enter bootloader interactive mode!')
                ser.close()
                return False
    with console.status(f'Starting web server...'):
        ss.send(f'ipaddr {ip_addr}\r')
        if not expect_with_timeout(ss, 'Change IP', timeout=5) or not check_bldr_cmd(ss):
            console.log('Cannot change bootloader ip!')
            ser.close()
            return False
        ss.send(f'httpd\r')
        if not expect_with_timeout(ss, 'bind to port', timeout=10) or not check_bldr_cmd(ss):
            console.log('Cannot start http server!')
            ser.close()
            return False
        try:
            time.sleep(3)
            r = requests.get(f'http://{ip_addr}/', timeout=10)
            r.raise_for_status()
            if not 'TC Rescue Page' in r.text:
                raise Exception('Wrong page...')
        except Exception as e:
            console.log('Cannot connect to the http server! Check your network card IP settings!')
            console.log(e)
            ser.close()
            return False
    def _upload_task(ip_addr, firmware_path):
        try:
            m = MultipartEncoder(
                boundary='---------------------------274518344616951420432640964747',
                fields={
                    'FWupload': (firmware_path.name, open(firmware_path, 'rb'), 'application/xml'),
                    'Upload': 'Upload'
                })
            r = requests.post(
                url=f'http://{ip_addr}/',
                data=m,
                headers={
                    'Content-Type': m.content_type
                },
                timeout=10)
        except:
            pass
    upload_thread=threading.Thread(target=_upload_task, args=(ip_addr, firmware_path))
    upload_thread.start()
    with console.status(f'Awaiting firmware...'):
        if not expect_with_timeout(ss, 'START TO RECEIVE the FILE', timeout=15):
            console.log('Could not send fw to router!')
            ser.close()
            upload_thread.join()
            return False
    with console.status('Uploading firmware...'):
        if not expect_with_timeout(ss, 'START TO CLOSE the FILE', timeout=120):
            console.log('Could not upload fw to router!')
            ser.close()
            upload_thread.join()
            return False
    upload_thread.join()
    with console.status('Checking data...'):
        if expect_with_timeout(ss, ['data success', 'data fail'], timeout=120) != 1:
            console.log('Failed to perform data check! Is the fw ok?')
            ser.close()
            return False    
    with console.status('Erasing old firmware...'):
        if not expect_with_timeout(ss, 'program from', timeout=120):
            console.log('Failed to erase old firmware!')
            ser.close()
            return False
    with console.status('Programming...'):
        if not expect_with_timeout(ss, 'successfully', timeout=120):
            console.log('Failed to program new firmware!')
            ser.close()
            return False
    console.log('All done! Sending a boot command!')
    ss.send(f'go\r')
    if interactive:
        ss.interact()
    ser.close()
    return True

def main():
    console = Console()
    console.print(r'  ___  ___ _       _  _ _ _ _  _   _                    ', style="b", highlight=False)
    console.print(r' |   \/ __| |  ___| \| / | | || | | |                   ', style="b", highlight=False)
    console.print(r' | |) \__ \ |_|___| .` | |_  _| |_| |                   ', style="b", highlight=False)
    console.print(r' |___/|___/____| _|_|\_|_| |_| \___/  _   ___  ___ ___  ', style="b", highlight=False)
    console.print(r' | __\ \    / / | | | | _ \ |  / _ \ /_\ |   \| __| _ \ ', style="b", highlight=False)
    console.print(r' | _| \ \/\/ /  | |_| |  _/ |_| (_) / _ \| |) | _||   / ', style="b", highlight=False)
    console.print(r' |_|   \_/\_/    \___/|_| |____\___/_/ \_\___/|___|_|_\ ', style="b", highlight=False)
    parser = argparse.ArgumentParser(description='Upload TRX firmwares to the Asus DSL-N14U via bootloader...')
    parser.add_argument('-s', '--serial', type=str, required=False)
    parser.add_argument('-f', '--firmware', type=str, required=True)
    parser.add_argument('-l', '--log', type=str, required=False)
    parser.add_argument('-n', '--noninteractive', type=bool, required=False, default=False)
    parser.add_argument('-a', '--address', type=str, required=False, default='192.168.2.1')
    args = parser.parse_args()
    if not args.serial:
        args.serial = serial.tools.list_ports.comports()[0].device
        console.log(f'No serial device specified, using {args.serial}.')
    upload(serial_port=args.serial, firmware_path=args.firmware, logfile=args.log, ip_addr=args.address, interactive=not args.noninteractive)

if __name__ == '__main__':
    main()
