import basepage as basepage
from selenium.webdriver.common.by import By
from pageOb.thirdpage import Thirdpage

class Secondpage(basepage):
    def goto_thirdpage(self):
        #使用find示例
        self.find(By.XPATH,"//*[@reource-id='com.xueqiu.android:id/action_search']").click()
        return Thirdpage(self._driver)