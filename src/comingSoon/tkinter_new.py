from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
root = Tk()

# my_label = Label(root,text="hello").grid(row = 0,column = 0)
# my_label = Label(root,text="hi").grid(row = 1,column = 1)
e = Entry(root, width=15,borderwidth = 5,bg="white")
e.grid(row = 0,column = 0)

# creating buttons
def myClick():
    hello = "Hello "+e.get()
    my_label01 = Label(root,text = hello).grid(row = 2,column = 0)
myButtons = Button(root,text= "click me",padx = 20,pady = 5, command = myClick, fg = "green",bg = "black").grid(row = 1,column = 0)

# state = DISABLED
root.mainloop()
