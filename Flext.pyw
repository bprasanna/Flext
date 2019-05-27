import tkinter as tk                    # Main GUI framework
import tkinter.scrolledtext as tkst     # Scrollable text area
import os                               # To peform OS related operations, in our case reading/writing files
import webbrowser                       # To open URLs
import datetime                         # To get current date & time
import csv                              # For reading and writing csv file
import shutil                           # Used to take clone of backup file, in case of data loss at backup, clone can be used

root = tk.Tk()

# Handle always on top
root.wm_attributes("-topmost", 1)
always_on_top = tk.BooleanVar()
always_on_top.set(True)
# Handle transparency
root.attributes("-alpha", 0.5)
enable_transparency = tk.BooleanVar()
enable_transparency.set(True)

# Title
root.title("Flext - Floating text box")

# Global Variables
all_widgets_loaded = 0
hide_lines_string = ""

# Global settings for widgets
frame1 = tk.Frame(master = root)
editArea = tkst.ScrolledText(master = frame1, wrap = tk.WORD, width = 20, height = 10)
popup_menu = tk.Menu(master=editArea, tearoff=0)


# Global functions
def on_focus_out(event):
    if event.widget == root:
        if enable_transparency:
           root.attributes("-alpha", 0.5)

def on_focus_in(event):
    if event.widget == root:
        if enable_transparency:
           root.attributes("-alpha", 1)

# Global associations
root.bind("<FocusIn>", on_focus_in)
root.bind("<FocusOut>", on_focus_out) 


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.pack() 
        self.read_conf() 
        self.read_file()
               


    def create_widgets(self):
        # Adding Menu
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        # create the About menu
        entry1 = tk.Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        entry1.add_command(label="Help", command=self.display_help)
        menu.add_cascade(label="About", menu=entry1)

        # Create the Settings menu
        entry2 = tk.Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        entry2.add_checkbutton(label="Always on top", onvalue=1, offvalue=False, variable=always_on_top, command=self.toggle_always_on_top)
        entry2.add_checkbutton(label="Transparent", onvalue=1, offvalue=False, variable=enable_transparency, command=self.toggle_enable_transparency)
        entry2.add_command(label="Preferences", command=self.open_settings)
        menu.add_cascade(label="Settings", menu=entry2)


        # Content area widgets definition
        frame1.pack(fill='both', expand='yes')
        editArea.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)
        editArea.bind("<Control-s>", self.write_input)


    def read_file(self):
        # First read the contents from sync file
    	if os.path.isfile('flext.log'):
            # Create clone
            shutil.copyfile('flext.log','flext_backup.log')
            with open("flext.log","r") as rf:
                 for line in rf:
                    if line:
                        if len(hide_lines_string) > 0:
                            if hide_lines_string not in line:
                                editArea.insert(tk.INSERT,line)
                        else:
                            editArea.insert(tk.INSERT,line)


    # Read configuration
    def read_conf(self):
        cm_found = 0
        if os.path.isfile('flext.conf'):
            with open("flext.conf","r") as rf:
                 for line in rf:
                     #print("Checking if %s is in %s"% ("HIDE_LINES:", line))
                     if "CONTEXT_MENU:" in line:
                         cm_found = 1
                         cm_all = line[len("CONTEXT_MENU:"):]
                         hash_pos = cm_all.index("#")
                         cm_label = cm_all[:hash_pos]
                         cm_url = cm_all[hash_pos+1:]
                         #print("cm_label: %s \n" % cm_label)
                         #print("cm_url: %s \n" % cm_url)
                         popup_menu.add_command(label=cm_label, command=lambda cm_url=cm_url : self.open_url(cm_url))
                     elif "HIDE_LINES:" in line:
                         global hide_lines_string
                         hluf = line[len("HIDE_LINES:"):]
                         hide_lines_string = hluf.rstrip()
                         #print("hide_lines %s"%hide_lines_string)
        if cm_found == 1:
            editArea.bind("<Button-3>", self.popup)
        global all_widgets_loaded
        all_widgets_loaded = 1                         


    def popup(self, event):
        try:
            popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            popup_menu.grab_release()


    # Method to open url in browser
    def open_url(self,url):
        print("%d \n"%all_widgets_loaded)        
        if (len(url) > 0 and all_widgets_loaded==1):
            #print("%s\n" %url)
            selected_text = editArea.selection_get()
            webbrowser.open_new_tab(url+selected_text)


    # Method to display help
    def display_help(self):
        # Displays help text in modal box
        htxt = tk.Toplevel(self)
        htxt.wm_title("About")
        txt_to_display = "A simple floating text box, which can be used for generic purposes. \n"
        txt_to_display += "Main intent is to keep always-on-top text box to display \nthe list of things which needs attention. \n"
        txt_to_display += "User can toggle: always-on-top, transparency in Settings menu. \n"
        txt_to_display += "Also, one can hide the lines which are already finished in \ntask/work wise, by adding custom marking in Preferences. \n"
        txt_to_display += "To save/sync the text to file, once can press Ctrl+s.\n"
        txt_to_display += "To avoid unintended loss of data, the sync file gets cloned (_backup.log) \nwhile opening the application.\n"
        lab1 = tk.Label(htxt, text=txt_to_display, anchor="w")
        lab1.pack(side="top", fill="both", expand=True)


    # Method to manage settings
    def open_settings(self):
        pref = tk.Toplevel(self)
        pref.wm_title("Preferences")
        lab1 = tk.Label(pref, text="This is window ")
        lab1.pack(side="top", fill="both", expand=True, padx=100, pady=100)


    # Method toggle always on top setting
    def toggle_always_on_top(self):
        global always_on_top
        if always_on_top:
            root.wm_attributes("-topmost", 0)
        else:
            root.wm_attributes("-topmost", 1)

        always_on_top = not always_on_top


    # Method to toggle transparency
    def toggle_enable_transparency(self):
        global enable_transparency
        if enable_transparency:
            root.attributes("-alpha", 1)
        else:
            root.attributes("-alpha", 0.5)

        enable_transparency = not enable_transparency      


    @staticmethod
    def write_input(self):
        of = open("flext.log","w")
        input = editArea.get("1.0",tk.END)
        for line in input:
            if line:
                of.write(line)


    @staticmethod
    def save_upon_exit():
        global hide_lines_string
        of = open("flext.log","w")
        # Separate file to write contents of lines which need to be
        # hidden
        if len(hide_lines_string) > 0:
            hlf = open('done.csv','a', newline='')
            writer = csv.writer(hlf, delimiter=',')

        # Without splitlines the content will be read in character-by-character
        input = editArea.get("1.0",tk.END).splitlines()
        for line in input:
            if line:
                if len(hide_lines_string) > 0:
                    #print("Checking if %s is in %s"% (hide_lines_string.rstrip, line))
                    if hide_lines_string in line:
                        writer.writerow([datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') , line])
                    else:
                        of.write(line+"\n")
                else:
                    of.write(line+"\n")

        if len(hide_lines_string) > 0:
            hlf.close()

        of.close()
        root.destroy
        exit()  



app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.save_upon_exit)
app.mainloop() 
