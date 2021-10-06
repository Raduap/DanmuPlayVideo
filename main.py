#coding:utf-8
import bilibili_api
import asyncio
import re
import time  # 引入time模块
import codecs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bilibili_api.live import LiveDanmaku

f = open("house.txt","r")   #设置文件对象
roomid = f.read()     #将txt文件的所有内容读入到字符串str中
f.close()   #将文件关闭
room = LiveDanmaku(room_display_id=int(roomid))
driver = webdriver.Chrome()


@room.on("DANMU_MSG")  # 指定事件名
async def on_dan_mu(msg_json):
    com = msg_json['data']['info'][1]
    print("收到弹幕:" + com)
    pattern = r"点播"
    matchobj = re.match(pattern, com)
    if matchobj is None:
        print("未匹配")
    else:
        print("匹配成功")
        print("视频号：" + com[2:])
        f = open("time.txt", "r")  # 设置文件对象
        times = f.read()
        f.close()
        nowtime = time.time()
        if int(times) < nowtime:
            f = open("time.txt", "r+")  # 设置文件对象
            f.write(str(int(nowtime) + 70))
            f.close()
            print("开始播放")
            videonum = com[2:]
            driver.get("https://www.bilibili.com/video/" + videonum)
            f = codecs.open(r'./details.txt', 'w+', encoding='utf-8')
            f.write(str(u"正在播放的是：" + videonum + "      \r\n"))
            f.write(str(u"点播时间：" + time.strftime("%H:%M:%S", time.localtime()) + "       \r\n"))
            f.close()
            sleep(3)
            element = driver.find_element_by_xpath(
                '/html/body/div[2]/div[4]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[11]/div[2]/div[2]/div[3]/div[9]/button[1]')  # xpath抓取播放控件
            ActionChains(driver).move_to_element(element).perform()
            element.click()
            element = driver.find_element_by_xpath('/html/body')
            ActionChains(driver).move_to_element(element).perform()
        else:
            print(nowtime)
            print("时间未到！请等待够一分钟")




print("start connect")
asyncio.set_event_loop(asyncio.new_event_loop())
stat = room.connect()
bilibili_api.sync(stat)
