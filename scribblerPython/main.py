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

program = spin()

root = Tk()
text = Text(root)

def openP():
    fname = TKFD.askopenfilename(title = "Open Program",filetypes = (("Scribbler Python File","*.pys"),("all files","*.*")))
    data = "File open error"
    with open(fname, "r") as f:
        data = f.read()
    text.insert(INSERT, data)

def saveP():
    fname = TKFD.asksaveasfilename(title = "Save Program",filetypes = (("Scribbler Python File","*.pys"),("all files","*.*")))
    with open(fname, "w") as f:
        f.write(text.get("1.0",END))

def runP():
    program.run(text.get("1.0",END))

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
