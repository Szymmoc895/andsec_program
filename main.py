import typer
import inquirer
import os
from rich import print
from subprocess import call
import time
from mobsfpy import MobSF
import console_explorer

mobsf = MobSF('117a684b67789264547447f1567daf8e5ea7d18ba12b4bf605673680f10d8624')

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

def get_apk_path():
    file_path = console_explorer.browse_for_file()

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

def run_mobsf():
    os.system('gnome-terminal -x sudo docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest')
    mobsf.upload

def main():
    
    #welcome()
    #get_apk_name()
    #run_emulator()
    #set_proxy()
    get_apk_path()

main()

#if __name__ == "__main__":
#    typer.run(main)