#-*- coding:utf-8 -*-

import urllib
import urllib2
import socket
import time
import re
import os
import subprocess

class Login:

    #初始化
    def __init__(self):
        #学号密码
        self.username = '141250136'
        self.password = 'A2wozuida'
        #NJU无线STU的IP网段
        self.ip_pre = '114.212'
        #检测间隔时间，单位为秒
        self.every = 1

    #模拟登录
    def login(self):
        print self.getCurrentTime(), u"正在尝试认证NJU网络"
        ip = self.getIP()
        data = {
            "username": self.username,
            "password": self.password
        }
        #消息头
        headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
            'Host': 'p.nju.edu.cn',
            'Origin': 'http://p.nju.edu.cn',
            'Referer': 'http://p.nju.edu.cn/portal/index.html?t=1412576034'
        }
        post_data = urllib.urlencode(data)
        login_url = "http://p.nju.edu.cn/portal_io/login"
        request = urllib2.Request(login_url, post_data, headers)
        response = urllib2.urlopen(request)
        result = response.read().decode('utf-8')
        #print result
        self.getLoginResult(result)


    #打印登录结果
    def getLoginResult(self, result):
        if u"登录成功!" in result:
            print self.getCurrentTime(),u"用户上线成功!"
        elif u"已登陆!" in result:
            print self.getCurrentTime(),u"您已经建立了连接,无需重复登陆"
        elif u"用户不存在" in result:
            print self.getCurrentTime(),u"用户不存在，请检查学号是否正确"
        elif u"用户密码错误" in result:
            pattern = re.compile('<td class="tWhite">.*?2553:(.*?)</b>.*?</td>', re.S)
            res = re.search(pattern, result)
            if res:
                print self.getCurrentTime(),res.group(1),u"请重新修改密码"
        else:
            print self.getCurrentTime(),u"未知错误，请检查学号密码是否正确"

    #获取当前时间戳，13位
    def getNowTime(self):
        return str(int(time.time()))+"000"

    #获取本机无线IP
    def getIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 0))
            print s.getsockname()
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
            return IP

    #判断当前是否可以联网
    def canConnect(self):
        fnull = open(os.devnull, 'w')
        result = subprocess.call('ping -c 5 www.baidu.com', shell = True, stdout = fnull, stderr = fnull)
        #print fnull
        fnull.close()
        if result:
            return False
        else:
            return True

    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #主函数
    def main(self):
        print self.getCurrentTime(), u"您好，欢迎使用模拟登陆系统"
        while True:
            nowIP = self.getIP()
            if not nowIP:
                print self.getCurrentTime(), u"请检查是否正常连接NJU无线网络"
            else:
                print self.getCurrentTime(),u"成功连接了NJU网络,本机IP为",nowIP
                self.login()
                while True:
                    can_connect = self.canConnect()
                    if not can_connect:
                        nowIP = self.getIP()
                        if not nowIP:
                            print self.getCurrentTime(), u"当前已经掉线，请确保连接上了NJU网络"
                        else:
                            print self.getCurrentTime(), u"当前已经掉线，正在尝试重新连接"
                            self.login()
                    else:
                        print self.getCurrentTime(), u"当前网络连接正常"
                    time.sleep(self.every)
            time.sleep(self.every)

login = Login()
login.main()