#!/usr/bin/env python
# encoding: utf-8
"""
@author: liuyw
"""
from splinter.browser import Browser
from time import sleep
import random
import traceback
import time, sys

from bs4 import BeautifulSoup
import requests

import re

class TemMail():

    def __init__(self):
        self.driver_name='chrome'
        self.executable_path='/usr/local/bin/chromedriver'

        self.driver=Browser(driver_name=self.driver_name,executable_path=self.executable_path)
        self.driver.driver.set_window_size(800, 800)
        self.driver.visit('https://www.moakt.com')
        self.driver.find_by_name('random').click();
        while self.driver.url=='https://www.moakt.com/zh/mail':
            return ;

    def getMailName(self):
        sleep(1);
        self.driver.execute_script('changeAddress();')
        sleep(1);
        mailname =  self.driver.find_by_id('email-address').text
        return mailname

    def getEmail(self):

        while True:
            self.driver.find_by_text(u"刷新列表").click()
            temdata = self.driver.find_by_text(u"激活您的ProcessOn帐号")
            if len(temdata)==0:
                sleep(2)
            else:
                em = self.driver.find_by_text(u"激活您的ProcessOn帐号").first
                url = em["href"]+'/content';
                self.getEmailDea(url)
                break

    def getEmailDea(self,emlurl):

        self.driver.visit(emlurl)
        temtext  = self.driver.html
        url_verify = re.findall(
            r"https://www.processon.com/signup/verification/\w+", temtext
        )
        ss_mail = requests.Session()
        rsp_verify = ss_mail.get(url_verify[0])

        if rsp_verify.status_code == 200:
            self.driver.quit()
        else:
            print("failure："+ rsp_verify.status_code)

class ProcessOn():

    def __init__(self,url):
        try:
            self.driver_name='chrome'
            self.executable_path='/usr/local/bin/chromedriver'

            self.driver=Browser(driver_name=self.driver_name,executable_path=self.executable_path)
            self.driver.driver.set_window_size(800, 800)
            self.driver.visit(url)
            self.driver.cookies.delete("processon_userKey")
            self.driver.find_by_text(u"注册").click()
            sleep(1);
            if self.driver.url=='https://www.processon.com/signup':
                return

        except Exception as e:
            print(e)
            self.driver.quit()

    def getrandomstr(self):
        randomstr = str(random.randint(1000000, 9999999))
        return randomstr;

    def signup(self,email):
        try:
            self.driver.fill("email", email)
            self.driver.fill("pass", self.getrandomstr())
            self.driver.fill("fullname", self.getrandomstr())
            self.driver.find_by_text(u"点击验证").click()

            print("\r请手动输入验证码");

            while True:
                if self.driver.url != 'https://www.processon.com/signup/submit':

                    sleep(1)
                else:
                    self.driver.cookies.delete()
                    self.driver.quit()
                    break


        except Exception as e:
            print(e)
            self.driver.quit()

class Runlop():

    def __init__(self,url):

        self.runlop(url)

    def runlop(self,url):

        temmail = TemMail()

        mailadds = temmail.getMailName();

        processOn = ProcessOn(url);

        processOn.signup(mailadds)

        temmail.getEmail()

        print("\r【OK】");
        self.runlop(url)

if __name__ == '__main__':


    url = "https://www.processon.com/i/5b57f34ae4b0edb750e966c3";
    print("======ProcessOn 邀请增加文件数量======")
    print("|     根据提示：                     |")
    print("|     1：输入你的邀请链接             |")
    print("|     2：手动处理ProcessOn注册验证    |")
    print("===================================")
    print("  请输入你的邀请链接:")
    # url = raw_input()
    try:
        runlop = Runlop(url)
    except Exception as e:
        print("================end================")


