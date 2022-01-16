import urllib.request
import sys
import time
import hashlib
import io
import http.cookiejar

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

def getHtml(LoginURL,username,password):
    #登录时需要POST的数据
    data={
        'Action': 'Login',
        'userName': username,
        'pwd': GetPassword(username,password),
        'sign': GetSign()
        }
    post_data = urllib.parse.urlencode(data).encode('utf-8')

    #设置请求头
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
           'Host': '202.115.133.173:805',
           'Origin': 'http://202.115.133.173:805',
           'Referer': 'http://202.115.133.173:805/Login.html',
           'X-Requested-With': 'XMLHttpRequest'}

    #登录时表单提交到的地址（用开发者工具可以看到）
    login_url = LoginURL

    #构造登录请求
    req = urllib.request.Request(login_url, headers = headers, data = post_data)

    #构造cookie
    cookie = http.cookiejar.CookieJar()

    #由cookie构造opener
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

    #发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
    resp = opener.open(req)

    #登录后才能访问的网页
    url = 'http://202.115.133.173:805/Classroom/ProductionSchedule/StuProductionSchedule.aspx?stuID=201813160119'

    #构造访问请求
    req = urllib.request.Request(url, headers = headers)
    resp = opener.open(req)
    html=resp.read().decode('utf-8')
    print(html)
    #print(resp.read().decode('utf-8'))


def GetPassword(username,password):
    password_md5=hashlib.md5(password.encode()).hexdigest()
    t=str(GetSign())
    temp=username+t+password_md5
    pwd=hashlib.md5(temp.encode()).hexdigest()
    return pwd

#毫秒级时间戳
def GetSign():
    return round(time.time() * 1000)

if __name__=='__main__':
    LoginURL="http://202.115.133.173:805/Common/Handler/UserLogin.ashx"
    getHtml(LoginURL,'201813160119','130532200010249517')




































