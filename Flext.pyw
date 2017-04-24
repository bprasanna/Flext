import tkinter as tk
import tkinter.scrolledtext as tkst
root = tk.Tk()
root.wm_attributes("-topmost", 1)
root.title("Flext - A floting text box")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()        

    def create_widgets(self):
      frame1 = tk.Frame(master = root)
      frame1.pack(fill='both', expand='yes')
      editArea = tkst.ScrolledText(master = frame1, wrap = tk.WORD, width = 20, height = 10)
      editArea.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)


app = Application(master=root)
app.mainloop() 
