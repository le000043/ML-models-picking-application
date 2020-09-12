import os
import subprocess
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
root = Tk()
run = IntVar(0)
in_str = StringVar()
test = StringVar()
# out = StringVar()
e = Entry(root, width=25,borderwidth = 2,bg="white")



def runFile():
    my_label00 = Label(root,text = "Your file is being processed ! Just a few seconds left...")
    my_label00.pack()
    root.update()
    if my_label00.winfo_exists():
        a = subprocess.Popen(["./a.out", in_str.get(),test.get()])
        a.wait()
    # while a.poll() is None:
    #     time.sleep(1)
    my_label00.pack_forget()
    my_label04 = Label(root,text = "FINISHED !!").pack()
    my_label05 = Label(root,text = "Your file is saved in predictions folder").pack()
    my_label06 = Label(root,text = "Thank you for using my application !").pack()
    my_label07 = Label(root,text = "It would be greatly appreciated if you can leave a constructive feedback!").pack()


def getTestFile():
    root.filename = filedialog.askopenfilename(initialdir = "test_data",title="select a file",filetypes = (("txt files","*.txt"),("csv files","*.csv")))
    my_label02 = Label(root,text = (root.filename).split('/')[-1]).pack()
    # global run
    # global out
    run.set(1)
    test.set((root.filename).split('/')[-1])

    myButtons0 = Button(root,width = 10,text= "Click to Run",padx = 250,pady = 5, command = runFile, fg = "green",bg = "black").pack()
def getInputFile():
    root.filename = filedialog.askopenfilename(initialdir = ".",title="select a file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    # global run
    # global out
    my_label01 = Label(root,text = (root.filename).split('/')[-1]).pack()
    in_str.set((root.filename).split('/')[-1])
    os.system("gcc main.c")
    myButtons0 = Button(root,text= "Choose directory for test file",padx = 250,pady = 5, command = getTestFile, fg = "green",bg = "black").pack()
# creating a file-selecting button
myButtons0 = Button(root,text= "Choose input file",padx = 250,pady = 5, command = getInputFile, fg = "green",bg = "black").pack()

root.geometry("520x240")
# in = ""
# out = ""
root.mainloop()
