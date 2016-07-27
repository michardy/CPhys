try:
    from tkinter import *
    import tkinter.filedialog as TKFD
    import tkinter.simpledialog as simpledialog
#    import ScrolledText as tkst
#    from tkconstants import END
except ImportError:
    from Tkinter import *
    import tkFileDialog as TKFD
    import ScrolledText as tkst
    from Tkconstants import END

from S2mms import spin

root = Tk()
text = Text(root)

def openP():
   text.insert(INSERT, "test text")

def saveP():
    print("test")

def runP():
    print(text.get(0, END))

#needs cleaning
mbar = Menu(root)
fm = Menu(mbar)
fm.add_command(label="Open Program", command=openP)
fm.add_command(label="Save Program", command=saveP)
fm.add_command(label="Run Program", command=runP)
mbar.add_cascade(label="File", menu=fm)
root.config(menu=mbar)
#mbar.pack()

text.pack()

#f.pack()

root.mainloop()
