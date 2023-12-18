import json
import typer
import inquirer
from inquirer.themes import BlueComposure
import os
from rich import print
from subprocess import call
import time
from mobsfpy import MobSF
from subprocess import check_output
import requests

from .file_manager import run_file_manager

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

def what_tool():
    questions = [
    inquirer.Checkbox(
        "tools",
        message="What tools do you want to use?",
        choices=["Trufflehog", "Drozer", "RMS(Runtime-Mobile-Security)", "MobSF", "MITM", "Just Android Emulator", "Others"],
        default=["Just Android Emulator"],
    ),
    ]

    answers = inquirer.prompt(questions)
    print(answers)
    # if 'Trufflehog' in answers["tools"]:
    #     trufflehog()
    if 'Drozer' in answers["tools"]:
        run_drozer()
    if 'RMS(Runtime-Mobile-Security)' in answers["tools"]:
        run_RMS()
    if "MobSF" in answers["tools"]:
        run_mobsf()
    

def trufflehog():
    q = [
        inquirer.Checkbox(
            "gitOrLocal",
            message="Do You want to scan Ur local or github repo?",
            choices=["Local", "Github"],
            default=["Local"],
        ),
    ]
    ans = inquirer.prompt(q, theme=BlueComposure())
    if 'Local' in ans['gitOrLocal']:
        path = get_repo_path()
        os.system(f'trufflehog git file://{path} --json | jq . >> "trufflehog_report_local.json"')
        os.system("gedit trufflehog_report_local.json")
    if 'Github' in ans['gitOrLocal']:
        os.system('trufflehog git https://github.com/StartupZmitac/ZMiTACinema.git --no-update --json | jq . >> "trufflehog_report_github.json')
        os.system("gedit trufflehog_report_github.json")
    if not ans['gitOrLocal']:
        print("No options have been choosen")

def get_repo_path():
    question = inquirer.Path("directory", path_type=inquirer.Path.DIRECTORY, message="What is Ur repo's directory?"),
    repo_path = inquirer.prompt(question)
    print(repo_path['directory']) 
    return repo_path['directory']

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
    time.sleep(10)

def check_if_ready():
    print('start')
    rc = call("./sleep.sh")
    print('stop')

def set_proxy():
    os.system('adb shell settings put global http_proxy "192.168.211.128:8080"')

def run_drozer():
    os.system('adb forward tcp:31415 tcp:31415')
    os.system('adb shell monkey -p com.mwr.dz -v 1')
    time.sleep(3)
    #os.system('gnome-terminal -- drozer console connect')
    #time.sleep(3)
    os.system('python3 /home/andsec/Documents/program/andsec_program/andsec/scanme.py') # tutaj przekopiować kod z scanme i go wywoływać

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
            print("MobSF is read.")
        else:
            print("MobSF is not ready.")
    path_to_file = get_apk_path()
    mobsf.upload(path_to_file)
    hash = check_output(args=f'md5sum {path_to_file}', shell=True).decode().split(' ')[0]
    mobsf.scan('apk', get_apk_name(), hash)
    mobsf.report_pdf(hash)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(mobsf.report_json(hash), f, ensure_ascii=False, indent=4)
    print('Scan completed!')

def run_RMS():
    run_emulator()
    os.system('rms')

def andsec_main():
    
    #welcome()
    #get_apk_name()
    #run_emulator()
    #set_proxy()
    #run_drozer()
    #get_apk_path()
    #run_mobsf()
    #run_emulator()
    #what_tool()
    #get_repo_path()
    run_RMS()

#main()

#if __name__ == "__main__":
#    typer.run(main)