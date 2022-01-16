import time
from icalendar import Calendar, Event,Alarm
import datetime
import pandas as pd
import numpy as np
import re
from cdut import setCalendar
from cdut import setCalendarEvent
from cdut import saveCalendarFile


#将html表格转化为csv格式
def HtmlToCsv():
    pdTable=pd.read_html(r"C:\saved_resource.html")[4]
    #保存成csv文件
    pdTable.to_csv(r'HBNYDX.csv', mode='a', encoding='utf_8_sig', header=1, index=0)
    

 #week=data.loc[2].get('周次')   #获得特定行的特定数据   
#数据解析
def parseData(InitialDate):
    #读取html
    data=pd.read_html(r"C:\saved_resource.html")[4]
    #正则
    pattern = re.compile(r'([0-9]{1,}-[0-9]{1,}|[0-9]{1,})')
    #行数
    RowsNumber=data.shape[0]      
    #生成日历文件
    Hbny=setCalendar('hbnyCalendar_author_aRu')

    uid=1001
    for i in range(2,RowsNumber):
        uid=uid+1
        #获得第i行的数据，转为list
        courseInfor=np.array(data.loc[i])
        #课程信息字典
        courseKey={'courseName':courseInfor[2],'courseWeek':courseInfor[12],'section':courseInfor[13],
                   'classNumber':courseInfor[14],'coursePlace':str(courseInfor[16])+str(courseInfor[17])}

        #正则匹配到目标周数
        weekly=re.findall(pattern,str(courseInfor[11]))
        #处理周数
        for i in range(0,len(weekly)):
            uid=uid+1
            if '-' in weekly[i]:                                 #如2-6周的形式
                minWeek=int(weekly[i][0:1])                      #最小周数
                maxWeek=int(weekly[i][2:4])                      #最大周数
                #print('min',minWeek,'maxWeek',maxWeek)

                #遍历周数
                for j in range(minWeek,maxWeek+1):
                    day=getDate(InitialDate,j,courseKey['courseWeek'])
                    courseTime=ChineseToNumber(courseKey['section'],courseKey['classNumber'])

                    uid=uid+1
                    summary=courseKey['courseName']
                    location=courseKey['coursePlace']
                    startTime=str(day.strftime('%Y%m%d'))+str(courseTime[0])
                    endTime=str(day.strftime('%Y%m%d'))+str(courseTime[1])

                    #加入日历事件
                    setCalendarEvent(Hbny,uid,summary,location,startTime,endTime)
                    #print('遍历',day,courseTime)
            else:
                day=getDate(InitialDate,weekly[i],courseKey['courseWeek'])
                courseTime=ChineseToNumber(courseKey['section'],courseKey['classNumber'])

                uid=uid+1
                summary=courseKey['courseName']
                location=courseKey['coursePlace']
                startTime=str(day.strftime('%Y%m%d'))+str(courseTime[0])
                endTime=str(day.strftime('%Y%m%d'))+str(courseTime[1])
                #加入日历事件
                setCalendarEvent(Hbny,uid,summary,location,startTime,endTime)
                #print('正常',day,courseTime)

    #保存
    saveCalendarFile(Hbny,'hbny')
 

#时间处理
#InitialDate数据类型实例-datetime.date(2020, 8, 31)
#weekly 周次，week星期数
def getDate(InitialDate,weekly,week):
    changeDays=(int(weekly)-1)*7+int(week)-1
    delta = datetime.timedelta(days = changeDays)
    newDate=InitialDate+delta
    return newDate


#节次时间 字典
#section 节次   classNumber节数
def ChineseToNumber(section,classNumber):
    Chinese_Number={'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,
                    '七':7,'八':8,'九':9,'十':10,'十一':11,'十二':12}
    courseTime=[['NULL'],
                ['T080000','T084500'],['T085500','T094000'],['T101000','T105500'],['T110500','T115000'],
                ['T143000','T151500'],['T152500','T161000'],['T162000','T170500'],['T171500','T180000'],
                ['T184000','T192500'],['T193500','T202000'],['T203000','T211500'],['T211500','T220000']]
    section=Chinese_Number[section]
    startTime=courseTime[section][0]
    temp=int(classNumber)+section-1
    endTime=courseTime[temp][1]
    classTime=[startTime,endTime]
    return classTime


def hbnyCourse(InitialDate):
    start=time.time()

    parseData(InitialDate)

    end=time.time()
    print('Running time: %s Seconds'%(end-start))
