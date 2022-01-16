import urllib.request
import re
from bs4 import BeautifulSoup
from lxml import etree
import time
from icalendar import Calendar, Event,Alarm
import datetime

from pandas.io import html
from theSpider import mainFuction
from config import LoginURL
from config import username
from config import password
from config import URL

#解析课表并生成.ics文件
# type=='' 代表在线解析    type=='&nbsp;'代表本地解析
def CourseInformation(soup,theYear,id,type):
    #第一周开始时间
    findFirstTime=re.compile(r'<td class="td1" nowrap="nowrap">01周<br/>([0-9]{1,}/[0-9]{1,})-.*?</td>')
    FirstTime=re.findall(findFirstTime,str(soup))[0]
    theMonth=int(FirstTime[0:2])
    theDay=int(FirstTime[3:5])
    #正则
    findCourseName=re.compile(r'<b class="fontcourse">.*?[(](.*?)[)].*</b>',re.S)     #课程缩写
    findCourseNames=re.compile(r'<b class="fontcourse">.*?[)](.*?)[(].*</b>',re.S)    #课程全称

    Scname_name=[]      #课程缩写与全称对应表
    for item in soup.find_all('b',class_="fontcourse"): 
        temp=[]
        item=str(item)

        CourseName=re.findall(findCourseName,item)[0].strip()      #课程缩写
        CourseNames=re.findall(findCourseNames,item)[0]            #课程全称

        temp.append(CourseName)
        temp.append(CourseNames)

        Scname_name.append(temp)
    #print(Scname_name)

    count=0                                     #课时计数
    InitialDate=datetime.date(theYear, theMonth, theDay)      #初始日期
    formatDate=InitialDate.strftime('%Y%m%d')   #标准格式
    #print(formatDate)

    testIcs=setCalendar('test')                 #建立ics

    for item in soup.select('.fontcss'):
        if item.get_text().strip()!=type:
            #print(item) 
            course=item.get_text()
            try:
                ctime=item['colspan']
            except:
                ctime=1      
            count=count+int(ctime)
            timee=CourseDate(count,ctime)
    
            for key in Scname_name:
                if key[0] in course:
                    course=key[1] 
                    #print("缩写"+key[0]+"全程"+key[1])   
            
            try:
                cplace=item.font.string
            except AttributeError as e:
                cplace=''
            #print(count,'1-课程',course,'时长',ctime,'地点',cplace,'时间',timee)

            uid=str(formatDate)+str(count)
            summary=course
            location=cplace
            startTime=str(formatDate)+timee[0]
            endTime=str(formatDate)+timee[1]
            setCalendarEvent(testIcs,uid,summary,location,startTime,endTime)
        else:
            #print('2-没课')
            count=count+1
        
        #1天过去了
        if count==12:
            count=0
            InitialDate=getDate(InitialDate,1)                 #日期加一
            formatDate=str(InitialDate.strftime('%Y%m%d'))     #化为日历文件日期标准格式
            #print(formatDate)

    #保存
    saveCalendarFile(testIcs,id)              
    

#课程时间字典
def CourseDate(count,ctime):
    key=str(count)+'-'+str(ctime)
    CourseDateKey={'2-2':['T081000','T094500'],
                   '4-2':['T101500','T115000'],'4-4':['T081000','T115000'],
                   '5-5':['T081000','T140000'],
                   '7-2':['T143000','T160500'], '7-3':['T120000','T160500'],'7-7':['T081000','T160500'],
                   '9-2':['T162500','T180000'],'9-4':['T143000','T180000'],'9-9':['T081000','T180000'],
                   '10-1':['T191000','T204500'],
                   '11-2':['T191000','T204500'],'11-6':['T143000','T204500'],
                   '12-3':['T191000','T213500'],'12-5':['T162500','T213500'],'12-7':['T143000','T213500'],'12-12':['T081000','T213500']}
    if CourseDateKey.__contains__(key):
        return CourseDateKey[key]
    else:
        print('错误',key)

#日期变换
#InitialDate数据类型实例-datetime.date(2020, 8, 31)
def getDate(InitialDate,changeDays):
    delta = datetime.timedelta(days = changeDays)
    newDate=InitialDate+delta
    return newDate



#生成日历文件
def setCalendar(CalendarName):
    cal = Calendar()
    cal.add('VERSION','2.0')
    cal.add('X-WR-CALNAME',CalendarName)
    cal.add('X-APPLE-CALENDAR-COLOR','#540EB9')
    cal.add('X-WR-TIMEZONE','Asia/Shanghai')
    return cal

#添加日历事件
def setCalendarEvent(calendar,uid,summary,location,startTime,endTime):
    event=Event()

    event.add('UID',uid)
    event.add('DTSTART;VALUE=DATE',startTime)
    event.add('DTEND;VALUE=DATE',endTime)
    event.add('SUMMARY',summary)
    event.add('SEQUENCE','0')
    event.add('DESCRIPTION','')
    event.add('LOCATION',location)

    alarm=Alarm()
    alarm.add('ACTION','NONE')
    alarm.add('TRIGGER;VALUE=DATE-TIME','19760401T005545Z')
    alarm.add('DESCRIPTION','This is an event reminder')

    event.add_component(alarm)
    calendar.add_component(event)

#保存
def saveCalendarFile(calendar,username):
    filePath='./aRu/'
    fileName=str(username)+'.ics'
    f=open(filePath+fileName, 'wb')
    f.write(calendar.to_ical())
    f.close()

#直接在线解析课表
def cdutCourse(theYear,id):
    start=time.time()
    
    #读取html
    newUrl=URL+id
    html=mainFuction(LoginURL,newUrl,username,password)
    middle=time.time()
    print('爬取到数据',(middle-start))
    #靓汤解析
    soup=BeautifulSoup(html,"lxml")

    CourseInformation(soup,theYear,id,'')
    end=time.time()
    print('Running time: %s Seconds'%(end-start))

#将课表保存到本地解析
def cdutCourseFile(theYear,id):
    path = './StuProductionSchedule.htm'
    html = open(path, 'r', encoding='utf-8').read()
    #print(html)
    #靓汤解析
    soup=BeautifulSoup(html,"lxml")
    CourseInformation(soup,theYear,id,'')



