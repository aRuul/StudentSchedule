import urllib.request
import sys
import re
from bs4 import BeautifulSoup
import xlwt
import time
import hashlib
import io
import http.cookiejar


#改变标准输出的默认编码的
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

#模拟登陆
def askURL(LoginURL,username,password):
    #临时存储数据的list
    temp=[]

    #登录时需要POST的数据
    data={
        'Action': 'Login',
        'userName': username,
        'pwd': GetPassword(username,password),
        'sign': GetSign()
        }
    post_data = urllib.parse.urlencode(data).encode('utf-8')

    #设置登陆请求头
    headerss = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
           'Host': '202.115.133.173:805',
           'Origin': 'http://202.115.133.173:805',
           'Referer': 'http://202.115.133.173:805/Login.html',
           'X-Requested-With': 'XMLHttpRequest'}

    try:
        #构造登录请求
        req = urllib.request.Request(LoginURL, headers = headerss, data = post_data)
        #构造cookie
        cookie = http.cookiejar.CookieJar()
    except BaseException:
        print("啊呀～，出错了。可能的原因：\n1.康康你的账号密码正确不  \n2.康康你的网络还好吗  \n3.教务处炸了")

    temp.append(req)
    temp.append(cookie)

    return temp

#爬取页面
def GetHtml(LoginURL,URL,username,password):
    loginInfor=askURL(LoginURL,username,password)
    #获得cookie
    req=loginInfor[0]
    cookie=loginInfor[1]

    #由cookie构造opener
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

    #发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
    resp = opener.open(req)

    #设置请求头
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52',
           'Host': '202.115.133.173:805',
           'Origin': 'http://202.115.133.173:805',
           'Referer': 'http://202.115.133.173:805/Default.aspx',
           'X-Requested-With': 'XMLHttpRequest',
           'Upgrade-Insecure-Requests': '1'}

    #构造访问请求
    req = urllib.request.Request(URL, headers = headers)
    resp = opener.open(req)
    html=resp.read().decode('utf-8')
    #print(html)
    return html

#账号密码加密
def GetPassword(username,password):
    password_md5=hashlib.md5(password.encode()).hexdigest()
    t=str(GetSign())
    temp=username+t+password_md5
    pwd=hashlib.md5(temp.encode()).hexdigest()
    return pwd

#毫秒级时间戳
def GetSign():
    return round(time.time() * 1000)

#main函数
def mainFuction(LoginURL,URL,username,password):
    html=GetHtml(LoginURL,URL,username,password)
    return html



