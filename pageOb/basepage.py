import inspect
import json
import time
from typing import Tuple, Union, Dict, List, NoReturn, Optional
from venv import logger

import yaml
from appium.webdriver import webdriver, WebElement
from selenium.webdriver.common.by import By
from appium.webdriver.webelement import WebElement as MobileWebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pageOb.wrapper import hande_black


class BasePage:
    _params = {}

    _black_list = [
        (By.XPATH, "//*[@text='确认']"),
        (By.XPATH, "//*[@text='确定']"),
    ]
    _max_num = 3
    _error_num = 0

    def __init__(self, driver: webdriver = None):
        self._driver = driver

    def set_implicitly(self,time):
        self._driver.implicitly_wait(time)

    def screen_shot(self,name):
        self._driver.save_screenshot(name)
    # 定位一个元素
    def finds(self, locator, value: str = None):
        elements: list
        if isinstance(locator, tuple):
            elements = self._driver.find_elements(*locator)
        else:
            elements = self._driver.find_elements(locator, value)

        return elements
    # 定位多个元素
    @hande_black
    def find(self, locator, value: str = None):
        element: WebElement

        if not isinstance(locator, tuple):
            element = self._driver.find_element(locator)
        else:
            element = self._driver.find_element(*locator,value)
        return element
    #定位元素并获取文本
    @hande_black
    def find_and_get_text(self, locator, value: str=None):
        element: WebElement
        if isinstance(locator, tuple):
            element_text = self._driver.find_element(*locator).text
        else:
            element_text = self._driver.find_element(locator,value).text
        return element_text

    # 解析yaml文件中的步骤 方法名需与yaml文件函数名一致
    def steps(self,path,name):
        with open(path, encoding="utf-8") as f:
            # 通过栈查主调方，以实现方法名定位yaml中的函数名
            name = inspect.stack()[1].function
            steps = yaml.safe_load(f)[name]
        # yaml文件中变量替换方法
        raw = json.dumps(steps)
        for key,value in self._params.items():
            raw = raw.replace(f'${{{key}}}',value)
            steps = json.loads(raw)

        for step in steps:
            if "action" in step.keys():
                action = step["action"]
                if "click" == action:
                    self.find(step["by"], step["locator"]).click()
                if "send" == action:
                    value = step["value"]
                    self.find(step["by"], step["locator"]).send_keys(step["value"])
                if "len > 0" == action:
                    eles = self.finds(step["by"], step["locator"])
                    return len(eles) > 0

    def find_element(self, element: Tuple[str, Union[str, Dict]]) -> MobileWebElement:
        """
        寻找元素
        """
        by = element[0]
        value = element[1]
        try:
            if self.is_element_exist(element):
                if by == "id":
                    return self._driver.find_element(By.ID, value)
                elif by == "name":
                    return self._driver.find_element(By.NAME, value)
                elif by == "class":
                    return self._driver.find_element(By.CLASS_NAME, value)
                elif by == "text":
                    return self._driver.find_element(By.LINK_TEXT, value)
                elif by == "partial_text":
                    return self._driver.find_element(By.PARTIAL_LINK_TEXT, value)
                elif by == "xpath":
                    return self._driver.find_element(By.XPATH, value)
                elif by == "css":
                    return self._driver.find_element(By.CSS_SELECTOR, value)
                elif by == "tag":
                    return self._driver.find_element(By.TAG_NAME, value)
                else:
                    raise NameError(
                        "Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except Exception as e:
            logger.error(">>>>>>>> failed to find element: %s is %s. Error: %s" % (by, value, e))

    def is_element_exist(self, element: Tuple[str, Union[str, Dict]], wait_seconds: int = 10) -> bool:
        """
        判断元素是否存在
        """
        by = element[0]
        value = element[1]

        try:
            if by == "id":
                WebDriverWait(self._driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self._driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self._driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "text":
                WebDriverWait(self._driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "partial_text":
                WebDriverWait(self._driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self._driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self._driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "tag":
                WebDriverWait(self._driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.TAG_NAME, value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except:
            return False
        return True

    def find_elements(self, element: Tuple[str, Union[str, Dict]]) -> Union[List[MobileWebElement], List]:
        """
        寻找一组元素
        """
        by = element[0]
        value = element[1]
        try:
            if self.is_element_exist(element):
                if by == "id":
                    return self._driver.find_elements(By.ID, value)
                elif by == "name":
                    return self._driver.find_elements(By.NAME, value)
                elif by == "class":
                    return self._driver.find_elements(By.CLASS_NAME, value)
                elif by == "text":
                    return self._driver.find_elements(By.LINK_TEXT, value)
                elif by == "partial_text":
                    return self._driver.find_elements(By.PARTIAL_LINK_TEXT, value)
                elif by == "xpath":
                    return self._driver.find_elements(By.XPATH, value)
                elif by == "css":
                    return self._driver.find_elements(By.CSS_SELECTOR, value)
                elif by == "tag":
                    return self._driver.find_elements(By.TAG_NAME, value)
                else:
                    raise NameError(
                        "Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except Exception as e:
            logger.error(">>>>>>>> failed to find elements: %s is %s. Error: %s" % (by, value, e))

    def find_all_child_element_by_xpath(self, element: Tuple[str, Union[str, Dict]]) -> Union[
        List[MobileWebElement], List]:
        """
        寻找元素的所有子元素
        """
        by = element[0]
        value = element[1]
        try:
            if self.is_element_exist(element):
                if by == "xpath":
                    child_value = value + '/child::*'
                    return self._driver.find_elements(By.XPATH, child_value)
                else:
                    raise NameError("Please enter the correct targeting elements 'xpath'.")
        except Exception as e:
            logger.error(">>>>>>>> failed to find elements: %s is %s. Error: %s" % (by, value, e))

    def save_screenshot(self, picture_name: str) -> NoReturn:
        """
        获取屏幕截图
        """
        fmt = '%Y%m%d%H%M%S'  # 定义时间显示格式
        date = time.strftime(fmt, time.localtime(time.time()))  # 把传入的元组按照格式，输出字符串
        picture_name = "../Result/" + picture_name + "-" + date + ".jpg"
        self._driver.get_screenshot_as_file(picture_name)

    def get_screen_size(self) -> Tuple[int, int]:
        """
        获取手机屏幕大小
        """
        x = self._driver.get_window_size()['width']
        y = self._driver.get_window_size()['height']
        return x, y

    def swipe_screen(self, direction: str, duration_ms: int = 800) -> NoReturn:
        """
        屏幕向上滑动
        """
        location = self.get_screen_size()
        if direction.lower() == "up":
            x = int(location[0] * 0.5)
            start_y = int(location[1] * 0.75)
            end_y = int(location[1] * 0.25)
            self._driver.swipe(x, start_y, x, end_y, duration_ms)
        elif direction.lower() == "down":
            x = int(location[0] * 0.5)
            start_y = int(location[1] * 0.25)
            end_y = int(location[1] * 0.75)
            self._driver.swipe(x, start_y, x, end_y, duration_ms)
        elif direction.lower() == "left":
            start_x = int(location[0] * 0.75)
            y = int(location[1] * 0.5)
            end_x = int(location[0] * 0.05)
            self._driver.swipe(start_x, y, end_x, y, duration_ms)
        elif direction.lower() == "right":
            start_x = int(location[0] * 0.05)
            y = int(location[1] * 0.5)
            end_x = int(location[0] * 0.75)
            self._driver.swipe(start_x, y, end_x, y, duration_ms)
        else:
            print("请输入正确的方向")

    def tap_screen(self, positions: List[Tuple[int, int]], duration: Optional[int] = None) -> NoReturn:
        """
        用最多五个手指轻拍一个特定的地方，保持一定的时间
        用法：tap_screen([(100, 20), (100, 60), (100, 100)], 500)
        """
        self._driver.tap(positions, duration)

    def click(self, element: Tuple[str, Union[str, Dict]], found_index: int = -1) -> NoReturn:
        """
        点击按钮
        """
        if found_index == -1:
            self.find_element(element).click()
        else:
            self.find_elements(element)[found_index].click()

    def send_keys(self, element: Tuple[str, Union[str, Dict]], value: str, clear_first: bool = False,
                  click_first: bool = False, found_index: int = -1) -> NoReturn:
        """
        键盘输入
        """
        if found_index == -1:
            if click_first:
                self.find_element(element).click()
            if clear_first:
                self.find_element(element).clear()
            self.find_element(element).send_keys(value)
        else:
            if click_first:
                self.find_elements(element)[found_index].click()
            if clear_first:
                self.find_elements(element)[found_index].clear()
            self.find_elements(element)[found_index].send_keys(value)

    def scroll_to_text(self, text) -> NoReturn:
        """
        滚动到指定的text
        """
        uiautomator_cmd = "new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text(\"%s\").instance(0))" % text
        self._driver.find_element_by_android_uiautomator(uiautomator_cmd)

    def get_attribute(self, element: Tuple[str, Union[str, Dict]], attribute_name: str = 'text',
                      found_index: int = -1) -> Optional[Union[str, Dict]]:
        """
        获取元素属性
        """
        if found_index == -1:
            return self.find_element(element).get_attribute(attribute_name)
        else:
            return self.find_elements(element)[found_index].get_attribute(attribute_name)

    def is_text_exist(self, text: str, wait_seconds: int = 10) -> bool:
        """
        判断text是否于当前页面存在
        """
        for i in range(wait_seconds):
            if text in self._driver.page_source:
                return True
            time.sleep(1)
        return False