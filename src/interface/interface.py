from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
root = Tk()
root.title('codemy.com Image Viewer')
root.iconbitmap('/Users/datle/Documents')
root.filename = filedialog.askopenfilename(initialdir = "/images",title="select a file",filetypes = (("png files","*.png"),("all files","*.*")))
my_label = Label(root,text=root.filename).pack()
my_image = ImageTk.PhotoImage(Image.open(root.filename))
my_image_label = Label(image = my_image).pack()
# root.mainloop()
print(root.filename)
