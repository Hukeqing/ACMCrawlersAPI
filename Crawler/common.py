import time
from typing import Tuple, List, Optional
import threading

from Crawler.basic import crawlerRes
from Crawler.versionControl import *

tryUseAPI = True
API_check = False
API_url = ""


# noinspection PyBroadException
class API_control:
    """
    Thanks to https://github.com/Liu233w/acm-statistics
    """
    APIList = ['https://new.npuacm.info', 'http://119.3.172.223:3000']
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    ojList = []

    @staticmethod
    def init_oj():
        global API_url
        for url in API_control.APIList:
            try:
                response = requests.get(url + "/api/crawlers/", headers=API_control.headers)
                data: dict = json.loads(response.text)
            except Exception as e:
                continue
            else:
                API_control.ojList = data["data"].keys()
                API_url = url + "/api/crawlers/"
                break

    @staticmethod
    def get_solved(oj: str, name: str) -> crawlerRes:
        res = crawlerRes(oj, username=name, sync=False)
        if oj not in API_control.ojList:
            res.set_error("oj name error!")
        else:
            response = requests.get(API_url + oj + "/" + name, headers=API_control.headers)
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
    def __init__(self, file_path: str, check: bool = True):
        self.file_path = file_path
        self.data: Optional[dict] = None
        self.acm: List[ACMer] = list()
        self.curTime: int = int(time.time())
        self.end: bool = False
        f = open(self.file_path, "rb")
        a = f.read()
        a = str(a, encoding='utf-8')
        self.data = json.loads(a)
        f.close()
        if check:
            self.check = True
            self.init_data()

    def init_data(self):
        threadList = []
        if self.data["version"] == dataVersion:
            for index, user in enumerate(self.data["user"]):
                self.acm.append(ACMer())
                self.acm[-1].set_name(user["name"])
                for account in user["account"].items():
                    if isinstance(account[1], str):
                        threadList.append(threading.Thread(target=self.acm[-1].add_account, kwargs={"other": account}))
                        threadList[-1].start()
                    else:
                        for account_name in account[1]:
                            threadList.append(
                                threading.Thread(target=self.acm[-1].add_account, kwargs={"other": (account[0], account_name)}))
                            threadList[-1].start()
            for i in threadList:
                i.join()
            self.end = True

    def add_in_database(self, index: int):
        if not self.check:
            self.init_data()
        user = self.data["user"][index]
        if "database" not in user.keys():
            user["database"] = dict()
        user["database"][str(self.curTime)] = dict()
        user["database"][str(self.curTime)]["solved"] = self.acm[index].solvedCount
        user["database"][str(self.curTime)]["submissions"] = self.acm[index].submissions
        f = open(self.file_path, "w", encoding='utf-8')
        f.write(json.dumps(self.data, indent=2, ensure_ascii=False))
        f.close()

    def get_last_data(self, index: int) -> Tuple[str, dict]:
        lastData = (0, {"solved": 0, "submissions": 0})
        user = self.data['user'][index]
        if "database" not in user.keys():
            user["database"] = dict()
        for times, value in user["database"].items():
            if int(times) > lastData[0] and int(times) != self.curTime:
                lastData = (int(times), value)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastData[0])), lastData[1]

    def get_history(self):
        res = str()
        for user in self.data["user"]:
            if "database" not in user.keys():
                return None
            res += user["name"] + ":\n"
            for times, value in user["database"].items():
                res += time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(times))) + '\t' + str(value['solved']) + '/' + str(
                    value['submissions']) + '\n'
        return res


def try_api():
    global Call
    global API_check
    if API_check:
        return
    if tryUseAPI:
        try:
            API_control.init_oj()
        except Exception as e:
            print(e)
            Call = CrawlersControl
    else:
        Call = CrawlersControl
    API_check = True


def change_try_mode():
    global tryUseAPI
    global API_check
    tryUseAPI = not tryUseAPI
    API_check = False
    if tryUseAPI:
        try_api()

# if __name__ == '__main__':
#     # 时间戳： time.time()
#     # 时间戳解析： time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1576847361))
#     try_api()
#     test = FileManager("../test.json")
#     print("全部OJ刷题数量统计\n姓名： ", test.acm.name, "\n解决/提交：", test.acm.solvedCount, "/", test.acm.submissions)
#     print("上次查询：", test.get_last_data()[0], test.get_last_data()[1]["solved"], "/", test.get_last_data()[1]["submissions"])
#     print("more detail:")
#     for item in test.acm.accountList:
#         if item.error:
#             print("出错\tOJ:", item.oj, "name:", item.username, "message:", item.message)
#         else:
#             print("oj:", item.oj, "name:", item.username, "solved:", item.solved, "submissions:", item.submissions, "solved list:", item.solvedList)
