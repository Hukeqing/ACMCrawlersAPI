import json
import sys
import threading
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import Crawler.versionControl
from Crawler import *


def check_for_update():
    if update():
        if tkinter.messagebox.askquestion('Update', 'There is a new version: ' + laterVersion + '\nCheck Ok to Download') == 'yes':
            get_new_version()
    else:
        tkinter.messagebox.showinfo('Update', 'There is no new version or check fail')


ACMer = None


def thr(file: str = None):
    global log
    log.set("Crawling")
    if not set_acm_er(file=file, cr=True):
        return
    errorMsg = ""
    for item in ACMer.acm:
        if len(item.errorAccountList) != 0 or len(item.repeatAccountList) != 0:
            errorMsg += item.name + ":\n"
            if len(item.errorAccountList) != 0:
                errorMsg += "\tError Account:\n"
                for ac in item.errorAccountList:
                    errorMsg += "\t\t" + ac.oj + " : " + ac.username + "\n"
            if len(item.repeatAccountList) != 0:
                errorMsg += "\tRepeat Account:\n"
                for ac in item.repeatAccountList:
                    errorMsg += "\t\t" + ac[0] + " : " + ac[1] + "\n"
    if errorMsg != "":
        tkinter.messagebox.showerror('Error', errorMsg)
    for index, user in enumerate(ACMer.acm):
        if tkinter.messagebox.askyesno('Over', 'Name: ' + user.name +
                                               '\nSolved: ' + str(user.solvedCount) +
                                               '\nSubmissions: ' + str(user.submissions) +
                                               '\nLast query time: ' + ACMer.get_last_data(index)[0] + '\n\t' +
                                               str(ACMer.get_last_data(index)[1]['solved']) + '/' +
                                               str(ACMer.get_last_data(index)[1]['submissions']) +
                                               '\n\nAdd to database?'):
            ACMer.add_in_database(index)
    log.set("Crawled")


def crawler():
    try_api()
    msg_handle = threading.Thread(target=thr)
    msg_handle.daemon = True
    msg_handle.start()


def set_acm_er(file: str = None, cr: bool = False):
    global ACMer
    if file is None:
        file = tkinter.filedialog.askopenfilename(initialdir='.')
        if file == '':
            return False
    if cr:
        tkinter.messagebox.showinfo('running', 'Crawler is running, please wait for a minute\n爬虫正在工作，请耐心等待')
    try:
        ACMer = FileManager(file, cr)
    except json.decoder.JSONDecodeError:
        tkinter.messagebox.showerror('Error', 'JSON Error\nJSON编码出错')
        log.set("Crawl Error")
        return False
    except Exception:
        tkinter.messagebox.showerror('Error', 'Unknown Error')
        log.set("Crawl Error")
        return False
    return True


def history():
    if not set_acm_er():
        return
    tkinter.messagebox.showinfo('History', ACMer.get_history())


def account_data():
    if not set_acm_er():
        return
    tkinter.messagebox.showinfo('Account', ACMer.get_user())


mainWin = tkinter.Tk()
mainWin.title("ZJGSU OnlineJudge Counter " + Crawler.versionControl.version)
mainWin.minsize(600, 400)

mainLabel = tkinter.Label(mainWin, text='ZJGSU OnlineJudge Counter', font=('Arial', 20), height=2)
mainLabel.pack()

updateButton = tkinter.Button(mainWin, text='Check For Update', command=check_for_update)
updateButton.pack()

space1 = tkinter.Label(mainWin)
space1.pack()

crawlerButton = tkinter.Button(mainWin, text='Crawler', command=crawler)
crawlerButton.pack()

space2 = tkinter.Label(mainWin)
space2.pack()

historyButton = tkinter.Button(mainWin, text='Get Query History', command=history)
historyButton.pack()

space3 = tkinter.Label(mainWin)
space3.pack()

accountButton = tkinter.Button(mainWin, text='Get User Account', command=account_data)
accountButton.pack()

space4 = tkinter.Label(mainWin)
space4.pack()

log = tkinter.StringVar()
log.set("Welcome")

crawlerLog = tkinter.Label(textvariable=log, bg='blue', font=('Arial', 20))
crawlerLog.pack()

if len(sys.argv) > 1:
    if sys.argv[1] == '-d':
        pass
    elif sys.argv[1] == '-i':
        pass
    elif sys.argv[1] == '-u':
        pass
    elif sys.argv[1] == '-c':
        try_api()
        handle = threading.Thread(target=thr, kwargs={"file": sys.argv[2]})
        handle.daemon = True
        handle.start()
    elif sys.argv[1] == '-q':
        try:
            ACMer = FileManager(sys.argv[2], False)
        except json.decoder.JSONDecodeError:
            tkinter.messagebox.showerror('Error', 'JSON Error\nJSON编码出错')
            log.set("Crawl Error")
            exit(0)
        except Exception:
            tkinter.messagebox.showerror('Error', 'Unknown Error')
            log.set("Crawl Error")
            exit(0)
        tkinter.messagebox.showinfo('History', ACMer.get_history())

mainWin.mainloop()
