# -*- coding: UTF-8 -*-
import os
import smtplib
import email
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header
import ssl
from email.mime.base import MIMEBase
from email import encoders
from email.utils import parseaddr, formataddr

import re
import time
import hashlib
import requests
import pymssql
from datetime import datetime, date, timedelta
from collections import Counter
from configparser import ConfigParser

def _format_addr(s):
    addr = parseaddr(s)
    return formataddr(addr)



conn = pymssql.connect(server='10.8.80.26', user='devops', password='Inceptio@20200831', database='OCULAR3', autocommit=True, port='1433', charset='utf8')
# 获取游标
# cur = conn.cursor() #结果形式：[(),(),..]
cur = conn.cursor(as_dict=True)  # [{},{},..]
if not cur:
    raise (NameError, "连接数据库失败")  # 将DBC信息赋值给cur
cursor_1 = conn.cursor()

# sql1 = """SELECT AGT_ALIAS FROM dbo.AGENT WHERE AGT_ID = '68355'"""
# cursor_1.execute(sql1)
# resp =cursor_1.fetchall()
# print(resp)

while True:
    today = (date.today()).strftime("%Y-%m-%d")
    # today = "2024-05-18"


    sql2 = """SELECT DAR_AGT_ID FROM dbo.DECRYPT_AUTH_REQUEST WHERE DAR_APPLY_TIME > '%s'""" % (today)
    cursor_1.execute(sql2)
    resp2 = cursor_1.fetchall()
    #print(resp2)
    print(len(resp2))

    resp2set = set(resp2)

    print(len(resp2set))





    for item in resp2set:
        leijicishu = resp2.count(item)

        agentid = item[0]
        print(agentid)
        cf = ConfigParser()

        cf.read("maillog.ini")

        cursorMark = cf.options(today)
        print(cursorMark)

        if str(agentid) in cursorMark:
            print(str(agentid) + "已发送过了~~")
            print("++++++++++++++++++++++++")
        elif leijicishu > 10:
            print("6666666666666666666666666666666")

            namesql = """SELECT AGT_ALIAS FROM dbo.AGENT WHERE AGT_ID = '%s'""" % (agentid)

            cursor_1.execute(namesql)
            respname = cursor_1.fetchall()
            print(respname[0][0])

            print("find ")
            print(item)

            mail_text = respname[0][0] + ",  申请解密次数：" + str(leijicishu)

            # start send email

            # SMTP服务器
            mail_host = "smtp.qiye.aliyun.com"
            # 发件人邮箱
            mail_sender = "noc@inceptio.ai"

            mail_license = "i@iTn@aDi#889"

            receiver = "taishan.yuan@inceptio.ai"
            # receiver2 = "bingfeng.yan@inceptio.ai"
            # receiver3 = "jackson.chen@inceptio.ai"

            # 收件人邮箱，可以为多个收件人
            # mail_receivers = [receiver, receiver2, receiver3]
            mail_receivers = [receiver]

            # mm = MIMEMultipart('alternative')
            mm = MIMEText(mail_text, 'plain', 'utf-8')

            # 邮件主题
            subject_content = "监控到以下员工今日申请解密次数大于10次"

            mm['From'] = _format_addr('<%s>' % mail_sender)

            mm["To"] = _format_addr('<%s>' % (mail_receivers))
            # 设置邮件主题
            mm["Subject"] = Header(subject_content, 'utf-8')

            context = ssl.create_default_context()

            # 创建SMTP对象
            stp = smtplib.SMTP(mail_host, 80)

            stp.starttls(context=context)

            stp.login(mail_sender, mail_license)
            try:

                stp.sendmail(mail_sender, mail_receivers, mm.as_string())
                print(" 邮件发送成功")
                print("****" * 4)
                # 关闭SMTP对象
                stp.quit()
                cf.set(today, str(agentid), '1')  # 在新的sec
                # write to file
                with open("maillog.ini", "w+") as f:
                    cf.write(f)

            except Exception as msg:
                print("无法发送邮件", msg)
    #time.sleep(21600) #6 hour
    time.sleep(3600)  # 1 hour
    #time.sleep(43200)  # 12 hour  11:50 and  23:50
