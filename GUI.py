import tkinter
import tkinter.messagebox
import tkinter.filedialog
from Crawler import *


# import threading


def check_for_update():
    if update():
        if tkinter.messagebox.askquestion('Update', 'There is a new version: ' + laterVersion + '\nCheck Ok to Download') == 'yes':
            get_new_version()
    else:
        tkinter.messagebox.showinfo('Update', 'There is no new version or check fail')


# def thread_try():


def crawler():
    try_api()
    tkinter.messagebox.showinfo('ready to run', 'When on crawling\nSystem may not respond!')
    ACMer = FileManager(tkinter.filedialog.askopenfilename(initialdir='.'))
    if tkinter.messagebox.askyesno('Over', 'Name: ' + str(ACMer.acm.name) +
                                           '\nSolved: ' + str(ACMer.acm.solvedCount) +
                                           '\nSubmissions: ' + str(ACMer.acm.submissions) +
                                           '\nLast query time: ' + ACMer.get_last_data()[0] + '\n\t' +
                                           str(ACMer.get_last_data()[1]['solved']) + '/' +
                                           str(ACMer.get_last_data()[1]['submissions']) +
                                           '\n\nAdd to database?'):
        ACMer.add_in_database()


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
crawlerCheckButton = tkinter.Checkbutton(mainWin, text='use API', command=change_try_mode)
crawlerCheckButton.pack()

space2 = tkinter.Label(mainWin)
space2.pack()

mainWin.mainloop()
