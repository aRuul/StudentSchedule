import datetime
from cdut import cdutCourse
from cdut import cdutCourseFile
from hbny import hbnyCourse
print('''
*----------------------------------------------------------*                
*              _   _                          __           *
*   __ _ _   _| |_| |__   ___  _ __    __ _  /__\_   _     *
*  / _` | | | | __| '_ \ / _ \| '__|  / _` |/ \// | | |    *
* | (_| | |_| | |_| | | | (_) | |    | (_| / _  \ |_| |    *
*  \__,_|\__,_|\__|_| |_|\___/|_|     \__,_\/ \_/\__,_|    *
*                                                          *
*                        日历课表                          *
* 目前支持的大学：成都理工大学    河北农业大学             *
*                                                          *
*----------------------------------------------------------*
''')

while 1:
    choice=input('''
                请输入你的大学对应的数字并回车
                ********************************
                *      1 成都理工大学--在线解析  *
                *      2 成都理工大学--本地解析  *
                *      3 河北农业大学           *
                ********************************
            github： https://github.com/aRuul/StudentSchedule
            食用指南：https://shimo.im/docs/GKtW6pWkWGTp8p3Y
    ''')   

    if choice=='1':
        theYear=input('请输入第一周开始时间的年份数字，并回车，如 2020: ')
        id=input("请输入你的学号，并回车,然后深呼吸一秒钟：")
        cdutCourse(int(theYear),id)
        print('课表已导出到 /aRu 文件夹下')
        print('===================================')
    elif choice=='2':
        print('本地解析请查看食用指南：https://shimo.im/docs/GKtW6pWkWGTp8p3Y')
        sure=input('查看完成后请输入ok，并回车')
        theYear=input('请输入第一周开始时间的年份数字，并回车，如 2020: ')
        id=input("请输入你的学号，并回车,然后深呼吸一秒钟：")
        cdutCourseFile(int(theYear),id)
        print('课表已导出到 /aRu 文件夹下')
        print('===================================')
    elif choice=='3':
        print('请河北农业大学的同学查看食用指南：https://shimo.im/docs/GKtW6pWkWGTp8p3Y')
        sure=input('查看完成后请输入ok，并回车')
        year=input('请输入第一周周一的年份de数字，如 2020：')
        month=input('请输入第一周周一的月份的数字，如 1：')
        day=input('请输入第一周周一的日份的数字，如 12：')

        InitialDate=datetime.date(int(year), int(month), int(day))

        try:
            hbnyCourse(InitialDate)
            print('导出成功，课表已导出到 /aRu 文件夹下')
            print('===================================')
        except BaseException:
            print('出错啦，请仔细阅读教程')
    else:
        print('请输入正确的数字')



