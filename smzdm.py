from selenium import webdriver
import time
import multiprocessing
from selenium.webdriver.chrome.options import Options
import json
import os

configsJson = os.environ.get('SMZDM_COOKIES')


if(configsJson == "" or configsJson == None):
    configsJson = input("配置：")
    print(configsJson)
    configs = json.loads(configsJson)
    print(configs)

class SmzdmSpider():
    def __init__(self):
        """打开浏览器"""
        self.options = Options()        
        self.options.binary_location = '/usr/bin/google-chrome'
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=self.options)   
    
    def add_cookie(self, cookie):
        self.driver.add_cookie(cookie)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def open_url(self, url):
        """传入url"""
        self.driver.get(url)
        #self.driver.maximize_window()
        self.driver.refresh()
        #time.sleep(0.01)
        self.driver.implicitly_wait(3)       # todo implicitly隐式等待，等待元素可见

    def is_login(self):
        if '退出登录' in self.driver.page_source:            
            print('登录成功')
            return True
        else:
            print('登录失败')
            return False

    def check_in(self):
        self.driver.find_element_by_xpath('//*[@id="index-head"]/div[3]/div[2]/a').click()
        self.driver.refresh()
    
    def is_checked(self):
        if '签到领奖' in self.driver.page_source:
            print("未签到")
            return False
        else:
            print('已签到')
            return True

    def closed(self):
        """关闭浏览器"""
        time.sleep(1)
        self.driver.quit()

def main():
    # TODO 根据操作顺序，调用方法执行
    b = SmzdmSpider()
    
    for config in configs:
        b.open_url("https://www.smzdm.com/")
        print('开始:' + config['username'])
        items=config.items()       
        for key, value in items:
            cookie={"name":str(key),"value":str(value),"path":"/","domain":".smzdm.com"}            
            b.add_cookie(cookie)
        b.open_url("https://www.smzdm.com/")
        if(b.is_login()):
            b.check_in()
            b.is_checked()
        b.delete_all_cookies()

    b.closed()

if __name__ == '__main__':
    main()
