import basepage as basepage

# BasePage:MainPage.goto_second_page>Secondpage.goto_thirdpage->Thirdpage
from pageOb.secondpage import Secondpage


class MainPage(basepage):
    def goto_second_page(self):
        self.set_implicitly(10)
        #使用yaml方法示例
        self.steps("../pageOb/ylsteps/main.yaml")
        self.set_implicitly(3)
        return Secondpage(self._driver)
