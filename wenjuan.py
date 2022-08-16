import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import random


def my_main():
    # 绕过验证的原理是刷新界面时置空webdriver对象,参考网址:https://blog.csdn.net/qq_45717425/article/details/119737648
    # 给出所需的url和option参数
    url_survey = "https://www.wjx.cn/vm/t9RscYU.aspx"  # 根据需要填写url
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    driver.get(url_survey)
    time.sleep(1)  # 使置空类可以充分由缓存写入
    # 先初始化对象
    # driver.maximize_window() #调试用的全屏化

    # 核心规则函数
    wenjuanxing_0(driver)  # 每个网页有自己的格式,需要重新找xpath


def wenjuanxing_unit(driver: webdriver, m: int = 1, n: int = 1):
    # driver.find_element(by=By.XPATH,value='').click()
    # m代表第几题,n代表第几个选项
    driver.find_element(by=By.XPATH,
                        value=f'/html/body/div[2]/form/div[6]/div[3]/fieldset/div[{m}]/div[2]/div[{n}]/span/a').click()


def wenjuanxing_0(driver: webdriver):
    for m in range(1, 16):
        # 根据题的类型分类
        # 2个选项的单选
        if m == 1:
            n = random.randint(1, 2)
            wenjuanxing_unit(driver, m, n)
        # 3单
        if m == 12:
            n = random.randint(1, 3)
            wenjuanxing_unit(driver, m, n)
        # 4个选项的单选
        if m == 2 or m == 6 or 10 >= m >= 9:
            n = random.randint(1, 4)
            wenjuanxing_unit(driver, m, n)
        # 7个选项的多选
        if 4 >= m >= 3 or 8 >= m >= 7:
            for i in range(1, 8):
                n = random.randint(1, 7)
                wenjuanxing_unit(driver, m, n)
        # 5个选项的多选
        if m == 5 or 14 >= m >= 13:
            for i in range(1, 6):
                n = random.randint(1, 5)
                wenjuanxing_unit(driver, m, n)
        # 4个选项的多选
        if m == 11:
            for i in range(1, 6):  # 奇数为了防止最后空选项
                n = random.randint(1, 4)
                wenjuanxing_unit(driver, m, n)
        if m == 15:
            wenjuanxing_unit(driver, 15, 3)
        # time.sleep(0.5)  #循环阀
    driver.find_element(by=By.XPATH, value='/html/body/div[2]/form/div[6]/div[7]/div[3]/div/div/div').click()

    time.sleep(1)  # 等待弹窗
    driver.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/div[2]/button').click()
    driver.find_element(by=By.XPATH,
                        value='/html/body/div[2]/form/div[6]/div[7]/div[2]/div/div/div/div[1]/div[1]/div[4]').click()
    time.sleep(5)  # 生存5秒来显示结果,取决于网络状态
    # 调试断点
    driver.close()


if __name__ == '__main__':
    # 可以改进的方向,把单选,多选单独定义个单元,然后可以爬取class=qtypetip的元素来自动确定题的类型选择合适的方法
    # 然后根据元素内的class=ui-controlgroup column1内的class=ui-checkbox的数量来确定选项的个数,或者根据例:
    # <input type="checkbox" value="4" id="q11_4" name="q11" style="display:none;">中的id的qm_n来确定题量和选项数
    # 不可以采用多线程处理,因为chromedriver一直处于被占用
    a = input("start?y/n\n")
    if a == 'y' or a == 'Y':
        # 目前没有办法绕过问卷星的检查机制(已解决)
        for i in range(1):
            my_main()
    else:
        exit(0)
    # 本项目开源,
