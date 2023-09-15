#!/user/bin/env pyhton解释器路径
# -*-coding:utf-8-*- 脚本编码
import cryptocode
import msvcrt
import os
import requests
import time
import json
import pywifi
from pywifi import const
from configparser import ConfigParser
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

file100 = 'config.ini'
version_info = '1.7'

def run(playwright: Playwright) -> None:
    try:
        global context
        browser = playwright.chromium.launch(headless=mode, channel=local)
        context = browser.new_context()
        page = context.new_page()
        printer('url: ' + testurl)
        page.goto(testurl)
        printer('account: ' + account)
        page.locator("[placeholder=\"请输入账号\"]").fill(account)  # .type(account)
        printer('password: ' + len(password) * '*')
        page.locator("[placeholder=\"请输入密码\"]").fill(password)
        page.locator("xpath=//*[@id='protocol']").click()
        printer('submit')
        page.locator("text=登录").click()
        browser.close()
        if network_check():
            printer('success')
        else:
            printer('fail')

    except:
        printer('fail')

    # 下线功能
    ''' printer('enter to log out')
        if len(input()) != 0:
            page.click('xpath=//*[@id="logout"]')
            page.click('text=确认')
            printer('exiting program...')
            time.sleep(5)
            #browser.close()
            #sys.exit()'''


def file1():  # 文件读写
    global account, password, testurl, mode, local, wifi, check
    console = Console()
    if os.path.exists(file100):  # 文件存在检测
        # printer('file existed')
        cf = ConfigParser()
        cf.read(file100)
        version = cf.get('parm', 'ver')
        if version < version_info:
            os.remove(file100)
            with console.screen(style="bold white on red") as screen:
                text = Align.center("[blink]配置文件\n版本过低\n自动删除[/blink]", vertical="middle")
                screen.update(Panel(text))
                time.sleep(5)
            file1()
        # main
        account = cf.get('main', 'uid')
        password = cf.get('main', 'pwd')
        # parm
        local = cf.get('parm', 'browser')
        mode = cf.get('parm', 'mode')
        check = cf.get('parm', 'check')
        wifi = cf.get('parm', 'wifi')
        testurl = cf.get('parm', 'url')

        # return account, password, testurl, mode, local, wifi, check
    else:
        printer('config file not fund')
        os.system('mode con cols=48 lines=23')
        printer('密码会自动加密');printer('输入后请按回车')
        printer('input account')
        account = input()

        printer('input password')
        password = pwd_input()
        print(' ')

        printer('运行模式选择')
        printer('headless(1)|browser(2)')
        mode = input()

        printer('浏览器选择')
        printer('edge(1)|chrome(2)')
        local = input()

        printer('使用网线(0)|GDOU.NET(1)')
        wifi = input()

        printer('网络检查间隔（秒）')
        check = int(input())

        testurl = 'http://1.1.1.1/'
        password = cryptocode.encrypt(password, 'louis16s')  # 加密

        with open(file100, "w") as file:
            file.write(
                '[main]' + '\n' +
                'uid = ' + str(account) + '\n' +
                'pwd = ' + str(password) + '\n' +
                '[parm]' + '\n' +
                'browser = ' + str(local) + '\n' +
                'mode = ' + str(mode) + '\n' +
                'check = ' + str(check) + '\n' +
                'wifi = ' + str(wifi) + '\n' +
                'url = ' + str(testurl) + '\n' +
                'ver = ' + version_info + '\n' + '\n' +
                '# browser 1 for edge 2 for chrome' + '\n' +
                '# mode 1 for headless'+ '\n' +
                '# check for ping time(s)'+ '\n' +
                '# wifi 0 for off 1 for on'+ '\n')
            file.close()
        for step in track(range(100), description="Writing..."):
            time.sleep(0.01)
        printer('config is generated')

    password = cryptocode.decrypt(password, 'louis16s')  # 解密
    # 浏览器
    if local == '0':
        local = None  # Chromium
    if local == '1':
        local = 'msedge'
    if local == '2':
        local = 'chrome'

    if mode == '1':
        mode = True  # 无头模式
    else:
        mode = False

    return account, password, testurl, mode, local, wifi, check


def connect_wifi(ssid):
    if ssid == '1':
        ssid0 = "GDOU.NET"
    if ssid == '2':
        ssid0 = "海大校园网"
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]
    print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()
    time.sleep(3)
    profile = pywifi.Profile()  # 配置文件
    profile.ssid = ssid0  # wifi名称
    ifaces.remove_all_network_profiles()  # 删除其它配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    ifaces.connect(tmp_profile)
    time.sleep(3)
    isok = True

    if ifaces.status() == const.IFACE_CONNECTED:
        print("connect successfully!")
    else:
        print("connect failed!")
        print('turn on ur wifi')
        time.sleep(5)
        connect_wifi(ssid)

    time.sleep(1)
    return isok


def network_check():
    try:
        session = requests.Session()
        html = session.get("https://www.baidu.com", timeout=2)
    except:
        return False
    return True


def os_checker():
    temp = file1()
    if temp[5] != "0":
        connect_wifi(temp[5])
    # os_version = platform.platform()
    if os.path.exists(file100):
        os.system('mode con cols=45 lines=8')
        printer('version ' + version_info)
        printer('script started')


def pwd_input():  # 密码
    chars = []
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")
        if newChar in '\r\n':  # 如果是换行，则输入结束
            break
        elif newChar == '\b':  # 如果是退格，则删除密码末尾一位并且删除一个星号
            if chars:
                del chars[-1]
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格
                msvcrt.putch(' '.encode(encoding='utf-8'))  # 输出一个空格覆盖原来的星号
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格准备接受新的输入
        else:
            chars.append(newChar)
            msvcrt.putch('*'.encode(encoding='utf-8'))  # 显示为星号
    return ''.join(chars)


def printer(content):  # 彩色输出
    console = Console()
    time1 = datetime.now().strftime('[%Y-%m-%d][%H:%M:%S]')
    console.print(time1, end='')
    console.print(content, style="yellow")


def info():
    try:
        url = (
            "http://10.129.1.1/cgi-bin/rad_user_info?callback=jQuery112406118340540763985_1556004912581&_=1556004912582")  # 指定网址
        response = requests.get(url=url)  # 发起请求#get会返回一个响应对象
        json_start = response.text.index('(') + 1;json_end = response.text.rindex(')')
        json_data = response.text[json_start:json_end]
        data = json.loads(json_data)
        ip = str(data.get("online_ip")).replace('"', " ")
        printer("ip: " + ip)
        sum_bytes = data.get("sum_bytes")
        sum_gb = sum_bytes * 0.000000001
        if sum_gb >= 1024:
            sum = sum_gb/1024;printer("已用流量:{:.2f} TB".format(sum))
        else:
            sum = sum_gb;printer("已用流量:{:.2f} GB".format(sum))
        device = str(data.get("online_device_total")).replace('"', " ")
        printer("在线设备:" + device)
    except:
        printer("获取信息失败")


if __name__ == '__main__':
    temp = file1()
    os_checker()
    i = True
    while True:
        if network_check():  # 网络正常
            if i:
                printer('认证通过，网络正常')
                info()
                i = False

        else:  # 网络异常或未连接
            with sync_playwright() as playwright:
                run(playwright)

        time.sleep(int(temp[6]))
