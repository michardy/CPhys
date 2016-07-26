try:
    from tkinter import *
    import tkinter.filedialog as TKFD
    import tkinter.simpledialog as simpledialog
except ImportError:
    from Tkinter import *
    import tkFileDialog as TKFD

def openP():
    

def saveP():
    

def runP():
    

#needs cleaning
root = Tk()
mbar = Menu(root)
fm = Menu(mbar)
fm.add_command(label="Open Program", command=openP())
fm.add_command(label="Save Program", command=saveP())
fm.add_command(label="Run Program"command=runP())
mbar.add_cascade(label="File", menu=fm)
root.config(menu=mbar)
#mbar.pack()

text = Text(root)
text.pack()

f.pack()

root.mainloop()
