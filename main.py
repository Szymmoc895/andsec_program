import typer
import inquirer
import os
from rich import print
from subprocess import call
import time
from mobsfpy import MobSF
import console_explorer
from subprocess import check_output
import requests

from file_manager import run_file_manager

mobsf = MobSF('64dfc59be4fb79b25d4f1dbd9e015fecdbc159ee76c2c7273a0fdcc949a9d028')

__author__ = 'szymmoc895 ( @szymmoc895) '

def welcome():
    __bannner__ = """
Welcome to Automated Android Security Testing Platform

        ⣿⣿⣿⣿⣿⣿⣧⠻⣿⣿⠿⠿⠿⢿⣿⠟⣼⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⠟⠃⠁⠀⠀⠀⠀⠀⠀⠘⠻⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⡿⠃⠀⣴⡄⠀⠀⠀⠀⠀⣴⡆⠀⠘⢿⣿⣿⣿⣿
        ⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿
        ⣿⠿⢿⣿⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⣿⡿⠿⣿
        ⡇⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⢸
        ⡇⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⢸
        ⡇⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⢸
        ⡇⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⢸
        ⣧⣤⣤⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣤⣤⣼
        ⣿⣿⣿⣿⣶⣤⡄⠀⠀⠀⣤⣤⣤⠀⠀⠀⢠⣤⣴⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⣿⣿⣿⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣤⣤⣴⣿⣿⣿⣦⣤⣤⣾⣿⣿⣿⣿
      
            Hope U'll enjoy it """   

    print("\n")
    print(f"[bold red]{__bannner__}[/bold red]")
    print("\n")

def get_apk_name():
    apk_name = typer.prompt("What's your application name?")
    print(f"apk name: {apk_name}")
    return apk_name

def get_apk_path():
    file_path = run_file_manager()
    print(file_path)
    return file_path

def run_emulator():
    #os.system("emulator -avd Pixel_2_API_29 &")
    os.system('gnome-terminal -x emulator -avd Pixel_2_API_29')
    os.system("adb wait-for-device shell 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done;'")
    #while [ "`adb shell getprop sys.boot_completed | tr -d '\r' `" != "1" ] ; do sleep 1; done
    print("koniec bootowania")

def check_if_ready():
    print('start')
    rc = call("./sleep.sh")
    print('stop')

def set_proxy():
    os.system('adb shell settings put global http_proxy "192.168.211.128:8080"')

def run_drozer():
    os.system('adb forward tcp:31415 tcp:31415')
    os.system('drozer console connect')
    os.system('adb shell monkey -p com.mwr.dz -v 1')
    time.sleep(3)
    os.system('python3 scanme.py') # tutaj przekopiować kod z scanme i go wywoływać

def check_mobsf_status():
    url = "http://127.0.0.1:8000"  # Zmodyfikuj, jeśli MobSF słucha na innym porcie lub adresie
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

def run_mobsf():
    os.system('gnome-terminal -x sudo docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest')
    #mobsf.upload('/home/andsec/Downloads/InsecureShop.apk')
    #mobsf.scan('apk', 'InsecureShop.apk', 'c5d872355e43322f1692288e2c4e6f00')
    #hash = check_output(args='md5sum /home/andsec/Downloads/InsecureShop.apk', shell=True).decode().split(' ')[0]
    #print(hash)
    while(check_mobsf_status() == False):
        time.sleep(3)
        if check_mobsf_status():
            print("MobSF jest uruchomiony.")
        else:
            print("MobSF nie jest uruchomiony.")
    path_to_file = get_apk_path()
    mobsf.upload(path_to_file)
    hash = check_output(args=f'md5sum {path_to_file}', shell=True).decode().split(' ')[0]
    mobsf.scan('apk', get_apk_name(), hash)

def main():
    
    #welcome()
    #get_apk_name()
    #run_emulator()
    #set_proxy()
    #get_apk_path()
    run_mobsf()

main()

#if __name__ == "__main__":
#    typer.run(main)