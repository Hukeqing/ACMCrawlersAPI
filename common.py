import requests
import json
from typing import Tuple, List, Optional, Union
import time

version = "1.0.0"
dataVersion = "1.0"


class API_control:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    ojList = []

    @staticmethod
    def init_oj():
        response = requests.get("https://new.npuacm.info/api/crawlers", headers=API_control.headers)
        data: dict = json.loads(response.text)
        API_control.ojList = data["data"].keys()

    @staticmethod
    def get_solved(oj: str, name: str) -> Tuple[int, Union[str, List]]:
        if oj not in API_control.ojList:
            return -1, "oj name error!"
        response = requests.get("https://new.npuacm.info/api/crawlers/" + oj + "/" + name, headers=API_control.headers)
        data: dict = json.loads(response.text)
        if data["error"]:
            return -1, data["message"]
        return data["data"]["solved"], data["data"]["submissions"]


class Account:
    def __init__(self, oj: str, name: str):
        self.oj: str = oj
        self.name: str = name
        self.error: bool = True
        self.solved: int = 0
        self.submissions: list = []
        self.message: str = ""
        self.get_data()

    def get_data(self):
        res = API_control.get_solved(self.oj, self.name)
        if res[0] != -1:
            self.solved, self.submissions = res
            self.error = False
        else:
            self.message = res[1]

    def __eq__(self, other):
        return self.name == other.name and self.oj == other.oj


class ACMer:
    def __init__(self, name):
        self.name: str = name
        self.solvedCount: int = -1
        self.accountList: List[Account] = []
        self.errorAccountList: List[Account] = []
        self.repeatAccountList: List[Tuple[str, str]] = []

    def __iadd__(self, other: Tuple[str, str]):
        newAccount = Account(*other)
        if newAccount in self.accountList or newAccount in self.errorAccountList:
            self.repeatAccountList.append(other)
            return
        if not newAccount.error:
            self.solvedCount += newAccount.solved
            self.accountList.append(Account(*other))
        else:
            self.errorAccountList.append(newAccount)


class FileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Optional[dict] = None
        self.acm: Optional[ACMer] = None
        self.curTime: int = int(time.time())
        self.init_data()

    def init_data(self):
        f = open(self.file_path, "r")
        self.data = json.load(f)
        if self.data["version"] == dataVersion:
            self.acm = ACMer(self.data["name"])
            for ojName, userName in self.data["account"].items():
                self.acm += (ojName, userName)
            self.data["database"][str(self.curTime)] = self.acm.solvedCount
        f.close()
        f = open(self.file_path, "w")
        json.dump(f, self.data)

    def get_last_data(self) -> Tuple[str, int]:
        lastData = (0, 0)
        for times, value in self.data["database"].items():
            if int(times) > lastData[0] and times != self.curTime:
                lastData = (int(times), value)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastData[0])), lastData[1]


API_control.init_oj()

if __name__ == '__main__':
    # 时间戳： time.time()
    # 时间戳解析： time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1576847361))
    test = FileManager("test.json")
    print(test.acm.solvedCount)
    print(test.data)
    print(test.get_last_data())
    pass
