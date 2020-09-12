import os
import subprocess
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
root = Tk()
in = ""
out = ""
def getOutputFile():
    root.filename = filedialog.askopenfilename(initialdir = ".",title="select a file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    out = "Output path: "+root.filename
    my_label01 = Label(root,text = out).pack()

def getInputFile():
    root.filename = filedialog.askopenfilename(initialdir = ".",title="select a file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    in = "Input path: "+root.filename
    my_label01 = Label(root,text = in).pack()
    os.system("gcc main.c")
    myButtons0 = Button(root,text= "Choose directory for output file",padx = 250,pady = 5, command = getOutputFile, fg = "green",bg = "black").pack()

    subprocess.Popen(["./a.out", (root.filename).split('/')[-1]])

    my_label02 = Label(root,text = out).pack()
    print("output saved to "+out)
    # print((root.filename).split('/')[-1])
# creating a file-selecting button
myButtons0 = Button(root,text= "Choose input file",padx = 250,pady = 5, command = getInputFile, fg = "green",bg = "black").pack()

root.geometry("500x200")
root.mainloop()

# subprocess.call(["gcc", "test.c"])
# subprocess.call(["./a.out"])
