import tkinter as tk
import tkinter.scrolledtext as tkst
import os

root = tk.Tk()
root.wm_attributes("-topmost", 1)
root.attributes("-alpha", 0.5)
root.title("Flext - A floting text box")

frame1 = tk.Frame(master = root)
editArea = tkst.ScrolledText(master = frame1, wrap = tk.WORD, width = 20, height = 10)


def on_focus_out(event):
    if event.widget == root:
        root.attributes("-alpha", 0.5)

def on_focus_in(event):
    if event.widget == root:
        root.attributes("-alpha", 1)

root.bind("<FocusIn>", on_focus_in)
root.bind("<FocusOut>", on_focus_out)        

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)    
        self.pack()
        self.create_widgets()
        self.read_file()      


    def create_widgets(self):
        frame1.pack(fill='both', expand='yes')
        editArea.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)
        editArea.bind("<KeyRelease-Return>", self.write_input)


    def read_file(self):
    	if os.path.isfile('flext.log'):
    	    with open("flext.log","r") as rf:
    		     for line in rf:
    			     editArea.insert(tk.INSERT,line)


    @staticmethod
    def write_input(self):
        of = open("flext.log","w")
        input = editArea.get("1.0",tk.END)
        of.write(input)


    @staticmethod
    def save_upon_exit():
        of = open("flext.log","w")
        input = editArea.get("1.0",tk.END)
        of.write(input)
        root.destroy
        exit()  



app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.save_upon_exit)
app.mainloop() 
