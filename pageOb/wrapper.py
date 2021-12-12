import logging

import allure
from selenium.webdriver.common.by import By

#忽略弹窗黑名单
def hande_black(func):
    logging.basicConfig(level=logging.INFO)
    def wrapper(*args,**kwargs):
        from pageOb.basepage import BasePage
        _black_list = [
            (By.XPATH, "//*[@text='确认']"),
            (By.XPATH, "//*[@text='确定']"),
        ]

        _max_num = 3
        _error_num = 0
        instance:BasePage = args[0]
        try:
            logging.info("run"+func.__name__+"\n args:\n"+repr(args[1:])+"\n"+repr(kwargs))
            element = func(*args, **kwargs)
            _error_num = 0
            instance._driver.implicitly_wait(5)
            return element
        except Exception as e:
            instance.screen_shot("tmp.png")
            with open("tmp.png","rb")as f:
                contend = f.read()
            allure.attach(contend,attachment_type=allure.attachment_type.PNG)
            logging.error("element not found,handle black list")
            instance._driver.implicitly_wait(3)
            if _error_num > _max_num:
                raise e
            _error_num += 1
            for ele in _black_list:
                elelist = instance.finds(*ele)
                if len(elelist) > 0:
                    elelist[0].click()
                    return wrapper(*args, **kwargs)
            raise e

    return wrapper



