import requests
import json
from typing import Tuple, List, Optional, Union
import time
from Crawler.basic import crawlerRes
from Crawler.Crawlers import *

version = "1.0.0"
dataVersion = "1.0"
tryUseAPI = True


class API_control:
    """
    Thanks to https://new.npuacm.info
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    ojList = []

    @staticmethod
    def init_oj():
        # response = requests.get("https://new.npuacm.info/api/crawlers/", headers=API_control.headers)
        response = requests.get("http://119.3.172.223:3000/api/crawlers/", headers=API_control.headers)
        # print(response.text)
        data: dict = json.loads(response.text)
        API_control.ojList = data["data"].keys()

    @staticmethod
    def get_solved(oj: str, name: str) -> crawlerRes:
        res = crawlerRes(oj, username=name, sync=False)
        if oj not in API_control.ojList:
            res.set_error("oj name error!")
        else:
            # response = requests.get("https://new.npuacm.info/api/crawlers/" + oj + "/" + name, headers=API_control.headers)
            response = requests.get("http://119.3.172.223:3000/api/crawlers/" + oj + "/" + name, headers=API_control.headers)
            data: dict = json.loads(response.text)
            if data["error"]:
                res.set_error(data["message"])
            else:
                res.submissions = data["data"]["submissions"]
                res.set_solved(data["data"]["solved"])
                res.set_solved_list(data["data"]["solvedList"])
        return res


class CrawlersControl:
    ojList = ['hdu']

    @staticmethod
    def get_solved(oj: str, name: str) -> crawlerRes:
        if oj in CrawlersControl.ojList:
            return eval(oj + '.get_solved(name)')
        res = crawlerRes('oj', username=name)
        res.set_error("oj name error!")
        return res


Call = API_control


class ACMer:
    def __init__(self):
        self.name: str = ""
        self.solvedCount: int = 0
        self.submissions: int = 0
        self.accountList: List[crawlerRes] = []
        self.errorAccountList: List[crawlerRes] = []
        self.repeatAccountList: List[Tuple[str, str]] = []

    def set_name(self, name):
        self.name = name

    def add_account(self, other: Tuple[str, str]):
        newAccount: crawlerRes = Call.get_solved(*other)
        if newAccount in self.accountList or newAccount in self.errorAccountList:
            self.repeatAccountList.append(other)
        elif not newAccount.error:
            self.solvedCount += newAccount.solved
            self.submissions += newAccount.submissions
            self.accountList.append(newAccount)
        else:
            self.errorAccountList.append(newAccount)


class FileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Optional[dict] = None
        self.acm: ACMer = ACMer()
        self.curTime: int = int(time.time())
        self.init_data()

    def init_data(self):
        f = open(self.file_path, "rb")
        self.data = json.loads(str(f.read(), encoding='utf-8'))
        if self.data["version"] == dataVersion:
            self.acm.set_name(self.data["name"])
            for item in self.data["account"].items():
                self.acm.add_account(item)
            if "database" not in self.data.keys():
                self.data["database"] = dict()
            self.data["database"][str(self.curTime)] = dict()
            self.data["database"][str(self.curTime)]["solved"] = self.acm.solvedCount
            self.data["database"][str(self.curTime)]["submissions"] = self.acm.submissions
        f.close()
        f = open(self.file_path, "w")
        f.write(json.dumps(self.data))
        f.close()

    def get_last_data(self) -> Tuple[str, dict]:
        lastData = (0, {})
        for times, value in self.data["database"].items():
            if int(times) > lastData[0] and int(times) != self.curTime:
                lastData = (int(times), value)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastData[0])), lastData[1]


def try_api():
    global Call
    if tryUseAPI:
        try:
            API_control.init_oj()
        except Exception as e:
            print(e)
            Call = CrawlersControl
    else:
        Call = CrawlersControl


if __name__ == '__main__':
    # 时间戳： time.time()
    # 时间戳解析： time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1576847361))
    try_api()
    test = FileManager("../test.json")
    print("全部OJ刷题数量统计\n姓名： ", test.acm.name, "\n解决/提交：", test.acm.solvedCount, "/", test.acm.submissions)
    print("上次查询：", test.get_last_data()[0], test.get_last_data()[1]["solved"], "/", test.get_last_data()[1]["submissions"])