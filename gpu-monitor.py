import os
import time
import re
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import logging


# --------------------log--------------------
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='gpu-monitor.log', level=logging.DEBUG, format=LOG_FORMAT)
# --------------------log--------------------


# --------------------fn--------------------
# 这里直接返回内存占用率
def get_gpu_info():
    # test
    strs = "| N/A   35C    P0    86W / 300W |  15515MiB / 16276MiB |     57%      Default |"

    # real
    # p = os.popen('nvidia-smi | grep N/A')
    # strs = p.read()
    # p.close()

    pattern = re.compile(r'\d+%')  # 查找 57%
    result = pattern.findall(strs)

    logging.info("GPU占用率：" + result[0])

    return int(result[0][0:-1])


# send Email
def send_email(username, password, receiver, smtp_server='smtp.163.com', message='有空闲GPU资源'):
    # 正文内容
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = Header("GPU监测", 'utf-8')
    msg['From'] = username
    msg['To'] = receiver

    smtp = smtplib.SMTP()
    smtp.connect(smtp_server, 25)
    smtp.set_debuglevel(1)
    smtp.login(username, password)
    smtp.sendmail(username, [receiver], msg.as_string())
    smtp.quit()


# start my program
def start_my(cmd):
    # real
    p = os.popen(cmd)
    strs = p.read()
    logging.info("程序执行情况：" + strs)
    p.close()

# --------------------fn--------------------
# main
memory = get_gpu_info()

# 判断
if memory < 10:
    send_email()
    start_my("dir")

else:
    time.sleep(1)

print(memory)










