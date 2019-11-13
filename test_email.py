#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 22:11
# @Author  : Ryu
# @Site    : 
# @File    : test_email.py
# @Software: PyCharm

import smtplib;
from email.mime.text import MIMEText;
from email.mime.multipart import MIMEMultipart;
from email.header import Header;

class email_test(object):
    def __init__(self,sender,receivers,enclosure_path_list):
        self.sender = sender;
        self.receivers = receivers;
        self.enclosure_path_list = enclosure_path_list;
        # 这是第三方服务
        self.mail_host = 'smtp.qq.com';
        self.mail_user = '1482795788@qq.com'
        self.mail_pass = 'ympsyxppqbtmjahe';

    # 信息邮件的发送
    def sender_email(self):

        message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8');
        # 发送者
        message['From'] = Header('1482795788@qq','utf-8');
        # 接收者
        message['To'] = Header('测试','utf-8');
        # 主题
        subject = 'Python SMTP 邮件测试';
        message['Subject'] = Header(subject,'utf-8');

        try:
            smtpObj = smtplib.SMTP();
            smtpObj.connect(self.mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass);
            smtpObj.sendmail(self.sender, self.receivers, message.as_string());
            print("发送邮件成功!")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件 error:%s" %(e));

    def send_email_by_hred(self):
        mail_msg = '<p>Python 邮件测试</p> <br />' \
                   '<p><a href = \'https://www.wuliuzongbu.com\'></a></p>'

        message = MIMEText(mail_msg,'plain','utf-8');
        message['From'] = Header(self.sender,'utf-8');
        message['To'] = Header('测试','utf-8');
        #设置主题
        subject = 'Python发送HTML格式邮件';
        message['Subject'] = Header(subject,'utf-8');

        try:
            smtpObj = smtplib.SMTP();
            smtpObj.connect(self.mail_host,25);
            smtpObj.login(self.mail_user, self.mail_pass);
            smtpObj.sendmail(self.sender,self.receivers,message.as_string());
            print('发送成功!')
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件 error:%s" % (e));

    #Python 发送带附件的邮件
    def send_email_by_file(self):
        message = MIMEMultipart();
        message = MIMEMultipart();
        # 构建附件函数
        self.build_email_enclosure(message);
        # 邮件头设置
        message['From'] = Header(self.sender, 'utf-8');
        message['To'] = Header('测试', 'utf-8');
        # 主题设置
        subject = 'Python 发送带附件的邮件';
        message['Subject'] = Header(subject, 'utf-8');
        try:
            smtp = smtplib.SMTP();
            smtp.connect(self.mail_host);
            smtp.login(self.mail_user,self.mail_pass);
            smtp.sendmail(self.sender,self.receivers,message.as_string())
            print('发送成功!')
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件 error:%s" % (e));

    # 构建附件
    def build_email_enclosure(self,message):
        path_list = list(self.enclosure_path_list);
        message.attach(MIMEText('Python 发送带附件的邮件测试……', 'plain', 'utf-8'));
        for item_path in path_list:
            try:
                file = open(item_path,'rb')
            except FileNotFoundError:
                print('this file is not exit!')
            path_str = str(item_path);
            print(path_str.split('\\')[-1]);
            # 邮件正文内容
            # 构造附件1，传送文件
            att = MIMEText(file.read(), 'base64', 'utf-8');
            att['Content-Type'] = 'application/octet-stream';
            att["Content-Disposition"] = 'attachment; filename=%s' %(path_str.split('\\')[-1]);
            message.attach(att);



if __name__ == '__main__':
    sender_email = '1482795788@qq.com';
    to_email = ['14789854931@163.com','3251128558@qq.com','mcyy99@gmail.com'];
    file_list_path = ['E:\\pythonCharts\\image\\1.jpeg','E:\\pythonCharts\\image\\2.jpg','E:\\pythonCharts\\image\\3.jpg']
    email = email_test(sender_email,to_email,file_list_path);
    email.send_email_by_file();
