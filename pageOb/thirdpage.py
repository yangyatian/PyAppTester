import basepage as basepage


class Thirdpage(basepage):

    def search(self,name):

        self._pamra["name"] = name
        self.steps("../page/ymlsteps/third.yaml")

    def add(self,name):

        self._params["name"] = name
        self.steps("../page/ymlsteps/third.yaml")

    def is_choose(self,name):
        self._params["name"] = name
        return self.steps("../ymlsteps/third.yaml")

    def reset(self,name):
        self._params["name"] = name
        self.steps("../ymlsteps/third.yaml")