import json
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from Crawler import *
import threading


def check_for_update():
    if update():
        if tkinter.messagebox.askquestion('Update', 'There is a new version: ' + laterVersion + '\nCheck Ok to Download') == 'yes':
            get_new_version()
    else:
        tkinter.messagebox.showinfo('Update', 'There is no new version or check fail')


# def thread_try():

ACMer = None


def thr(file_name):
    global ACMer
    global log
    log.set("Crawling")
    try:
        ACMer = FileManager(file_name)
    except json.decoder.JSONDecodeError as e:
        tkinter.messagebox.showerror('Error', 'JSON Error\nJSON编码出错')
        log.set("Crawl Error")
        exit(0)
    if tkinter.messagebox.askyesno('Over', 'Name: ' + str(ACMer.acm.name) +
                                           '\nSolved: ' + str(ACMer.acm.solvedCount) +
                                           '\nSubmissions: ' + str(ACMer.acm.submissions) +
                                           '\nLast query time: ' + ACMer.get_last_data()[0] + '\n\t' +
                                           str(ACMer.get_last_data()[1]['solved']) + '/' +
                                           str(ACMer.get_last_data()[1]['submissions']) +
                                           '\n\nAdd to database?'):
        ACMer.add_in_database()
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


mainWin = tkinter.Tk()
mainWin.title("ZJGSU OnlineJudge Counter")
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

# historyButton = tkinter.Button(mainWin, text='Get Query History')
# historyButton.pack()
#
# space3 = tkinter.Label(mainWin)
# space3.pack()

log = tkinter.StringVar()
log.set("Welcome")

crawlerLog = tkinter.Label(textvariable=log, bg='blue', font=('Arial', 20))
crawlerLog.pack()

mainWin.mainloop()
