import tkinter
import tkinter.messagebox
import tkinter.filedialog
from Crawler import *
import threading


# import threading


def check_for_update():
    if update():
        if tkinter.messagebox.askquestion('Update', 'There is a new version: ' + laterVersion + '\nCheck Ok to Download') == 'yes':
            get_new_version()
    else:
        tkinter.messagebox.showinfo('Update', 'There is no new version or check fail')


# def thread_try():

ACMer = None
file = ""


def thr():
    global ACMer
    global log
    log.set("Crawling")
    ACMer = FileManager(file)
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
    global file
    file = tkinter.filedialog.askopenfilename(initialdir='.')
    if file == '':
        return
    msg_handle = threading.Thread(target=thr, args=())
    msg_handle.daemon = True
    msg_handle.start()
    tkinter.messagebox.showinfo('running', 'Crawler is running, please wait for a minute\n爬虫正在工作，请耐心等待')


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

log = tkinter.StringVar()
log.set("Welcome")

crawlerLog = tkinter.Label(textvariable=log, bg='blue', font=('Arial', 20))
crawlerLog.pack()

mainWin.mainloop()
