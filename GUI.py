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


def thr(file_name):
    global ACMer
    global log
    log.set("Crawling")
    try:
        ACMer = FileManager(file_name)
    except json.decoder.JSONDecodeError:
        tkinter.messagebox.showerror('Error', 'JSON Error\nJSON编码出错')
        log.set("Crawl Error")
        exit(0)
    except Exception as e:
        tkinter.messagebox.showerror('Error', 'Unknown Error')
        log.set("Crawl Error")
        exit(0)
    # errorMsg = ""
    # if len(ACMer.acm.errorAccountList) != 0:
    #     errorMsg += "Error Account:\n"
    #     for item in ACMer.acm.errorAccountList:
    #         errorMsg += '\t' + item.oj + ' : ' + item.username + '\n'
    # if len(ACMer.acm.repeatAccountList) != 0:
    #     errorMsg += "Repeat Account:\n"
    #     for item in ACMer.acm.repeatAccountList:
    #         errorMsg += '\t' + item[0] + ' : ' + item[1] + '\n'
    # if errorMsg != "":
    #     tkinter.messagebox.showerror('Error', errorMsg)
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
    file = tkinter.filedialog.askopenfilename(initialdir='.')
    if file == '':
        return
    msg_handle = threading.Thread(target=thr, kwargs={"file_name": file})
    msg_handle.daemon = True
    tkinter.messagebox.showinfo('running', 'Crawler is running, please wait for a minute\n爬虫正在工作，请耐心等待')
    msg_handle.start()


def history():
    global ACMer
    file = tkinter.filedialog.askopenfilename(initialdir='.')
    if file == '':
        return
    try:
        ACMer = FileManager(file, False)
    except json.decoder.JSONDecodeError:
        tkinter.messagebox.showerror('Error', 'JSON Error\nJSON编码出错')
        log.set("Crawl Error")
        exit(0)
    except Exception:
        tkinter.messagebox.showerror('Error', 'Unknown Error')
        log.set("Crawl Error")
        exit(0)
    tkinter.messagebox.showinfo('History', ACMer.get_history())


if len(sys.argv) > 1:
    Crawler.versionControl.version_fun(sys.argv)

mainWin = tkinter.Tk()
mainWin.title("ZJGSU OnlineJudge Counter " + Crawler.versionControl.version)
mainWin.minsize(500, 300)

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

log = tkinter.StringVar()
log.set("Welcome")

crawlerLog = tkinter.Label(textvariable=log, bg='blue', font=('Arial', 20))
crawlerLog.pack()

mainWin.mainloop()
