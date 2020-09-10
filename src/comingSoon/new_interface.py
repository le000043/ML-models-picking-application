from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
root = Tk()

# my_label = Label(root,text="hello").grid(row = 0,column = 0)
# my_label = Label(root,text="hi").grid(row = 1,column = 1)
# e = Entry(root, width=15,bg="white")
# e.grid(row = 0,column = 0)

# creating buttons
def getInputFile():
    # hello = "Hello "+e.get()
    # my_label01 = Label(root,text = hello).grid(row = 2,column = 0)
    root.filename = filedialog.askopenfilename(initialdir = ".",title="select a file",filetypes = (("all files","*.*")))
    # my_label01 = Label(root,text = root.filename).grid(row = 2,column = 0)
    print(root.filename)
    my_label01 = Label(root,text = root.filename).pack()

myButtons0 = Button(root,text= "click to choose input file",padx = 250,pady = 5, command = getInputFile, fg = "green",bg = "black").pack()

# myButtons0 = Button(root,text= "click to choose input file",padx = 250,pady = 5, command = getInputFile, fg = "green",bg = "black").grid(row = 1,column = 0)
# myButtons1 = Button(root,text= "click to choose output file",padx = 20,pady = 5, command = getOutputFile, fg = "green",bg = "black").grid(row = 1,column = 0)

# state = DISABLED
root.geometry("500x200")
root.mainloop()
print(name)
return name
