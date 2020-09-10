from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
root = Tk()

def getInputFile():
    root.filename = filedialog.askopenfilename(initialdir = ".",title="select a file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    my_label01 = Label(root,text = root.filename).pack()
# creating a file-selecting button
myButtons0 = Button(root,text= "click to choose input file",padx = 250,pady = 5, command = getInputFile, fg = "green",bg = "black").pack()

root.geometry("500x200")
root.mainloop()
print((root.filename).split('/')[-1])
