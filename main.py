import bilibili_api
import asyncio
import re
from selenium import webdriver

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
        videonum = com[2:]
        driver.get("https://www.bilibili.com/video/" + videonum)

    """if com[:2] == '*-':
        color = 'rgb(125, 0, 0)'
        msg = [color, f'{u_name}: {com}']
        dan_mu_msg.append(msg)"""


print("start connect")
asyncio.set_event_loop(asyncio.new_event_loop())
stat = room.connect()
bilibili_api.sync(stat)
