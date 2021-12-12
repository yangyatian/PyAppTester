import pytest
import yaml

from pageOb.driverinit import DriverInit


class TestcaseDemo():
    def setup(self):
        DriverInit().mainpage().goto_second_page().goto_thirdpage()

    @pytest.mark.parametrize("name",yaml.safe_load(open("./test_search.yaml",encoding="utf-8")))
    def test_search(self,name):
        self.search.search(name)
        if self.search.is_choose(name):
            self.search.reset(name)
        self.search.add(name)
        assert self.search.is_choose(name)