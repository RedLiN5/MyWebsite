import datetime
import time
import codecs
import urllib.request
from selenium import webdriver
import selenium.webdriver.support.ui as ui

driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver,5)

for i in range(100):
    try:
        driver.get("http://login.weibo.cn/login/")
        elem_user = driver.find_element_by_name("mobile")
        elem_user.send_keys('username')
        elem_pwd = driver.find_element_by_xpath("/html/body/div[2]/form/div/input[2]")
        elem_pwd.send_keys('password')

        img = driver.find_element_by_xpath('/html/body/div[2]/form/div/img[1]')
        src = img.get_attribute('src')
        name = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        urllib.request.urlretrieve(src, "ValidationImages/" +\
                                   name +\
                                   ".jpg")

        driver.refresh()
        time.sleep(2)

    except Exception as e:
        print('Error:', e)

driver.quit()
print(u'End Security Codes Retrieving!\n\n')
