import yaml
from appium import webdriver
from pageOb.basepage import BasePage
from pageOb.mainpageDemo import MainPage


class DriverInit(BasePage):

    def start(self):
        file = open('desired_caps.yaml', 'r')
        data = yaml.load(file, Loader=yaml.FullLoader)
        if self._driver is None:
            desired_caps = {}
            desired_caps['platformName'] = data['platformName']  # 设备系统
            desired_caps['platformVersion'] = data['platformVersion']  # 设备系统版本
            desired_caps['deviceName'] = data['deviceName']  # 设备名称
            desired_caps['appPackage'] = data['appPackage']
            desired_caps['appActivity'] = data['appActivity']
            desired_caps['noReset'] = data['noReset']
            desired_caps['skipServerInstallation'] = data['skipServerInstallation']
            desired_caps['unicodeKeyBoard'] = data['unicodeKeyBoard']
            desired_caps['resetKeyBoard'] = data['resetKeyBoard']
            desired_caps['autoGrantPermissions'] = data['autoGrantPermissions']

            self._driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        else:
            self._driver.start_activity(data['appPackage'],data['appActivity'])
        self._driver.implicitly_wait(3)
        return self

    def mainpage(self) -> MainPage:
        return MainPage(self._driver)

