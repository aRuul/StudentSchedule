# StudentSchedule
![Travis](https://img.shields.io/badge/aRuul-StudentSchedule-green)

---
## 简介
- 这是一个可以将课表导出到📅日历中的工具

## 目前支持的学校
- 成都理工大学
- 河北农业大学

## 食用方法
### windows系统exe文件使用方法
[点我下载windows打包版本](https://aru.lanzous.com/b01bulq6b) | [备用链接](https://objects.githubusercontent.com/github-production-release-asset-2e65be/309921127/e6fece69-68b4-46da-abb9-cb4eceeb6f13?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220117%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220117T042856Z&X-Amz-Expires=300&X-Amz-Signature=f9e62bd2bdcb250b0a48d5f6463690f698d91282c9c1ab3e6cac571b4628d4b5&X-Amz-SignedHeaders=host&actor_id=66399688&key_id=0&repo_id=309921127&response-content-disposition=attachment%3B%20filename%3DaRu_iCalendar.zip&response-content-type=application%2Foctet-stream) 

[本项目版本在线使用指南](https://shimo.im/docs/GKtW6pWkWGTp8p3Y/read)

### 直接运行代码使用方法
1. 修改config.py文件中的8、10行代码
```python
#学号 设置成你的学号
username=''
#教务处密码 设置成你的密码
password=''
```
2. 运行show.py即可
  
   **注意**！如果要使用本地解析，请登录学校教务处，打开课表页面，Ctrl+S将网页保存在本工具的同级目录下即可使用

## 更新记录

- Jan 16, 2022 突然诈尸更新，添加了[成都理工大学]本地课表解析导出的功能，解决了无法登录教务处的问题
- Nov 11, 2020 完成 [河北农业大学] 的课表导出
- Nov 4, 2020 完成 [成都理工大学] 的课表导出

---
## 开源协议
<img src="https://img.shields.io/github/license/tensorflow/tensorflow.svg"/>
