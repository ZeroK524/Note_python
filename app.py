from tkinter import *
from define import *
from tkinter import filedialog
import os
class App():
    def __init__(self, window):
        self.window = window
        
        #Set Window
        window.geometry(f"{window_width}x{window_height}+{window_position_right}+{window_position_down}")

        #Set Title
        window.title(title_name)

        #Set Icon
        window.iconbitmap("image/iconICO.ico")


        #On/Off resize
        window.resizable(True,True) # On/Off 

        #Text Widget
        self.inputtxt = Text(window, font=("Times New Roman", 12))
        self.inputtxt.pack(expand=True,fill='both')

        # Path

        self.save_directory = "save"
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        
        self.save_path = os.path.join(self.save_directory, "auto_save.txt")
        self.previous_save_path = ""

        #Auto save
        self.inactivity_counter = auto_save_time # time
        self.auto_save()
        # Restore notes
        self.restore_notes()
        # Handle window close event
        window.protocol("WM_DELETE_WINDOW", self.on_close)  

    def auto_save(self):
        current_content = self.inputtxt.get("1.0", END).strip()
        if current_content != self.previous_save_path:
            self.inactivity_counter = auto_save_time # Reset time
            if self.save_path:
                with open(self.save_path, "a", encoding="utf-8") as file:
                    if current_content:
                        file.write("New Auto Save:" + "\n" + current_content + "\n")
            self.previous_save_path = current_content
            print("Auto_save:",self.inactivity_counter)
            self.window.after(5000, self.auto_save)
        else:
            if self.inactivity_counter > 0:
                self.inactivity_counter -= 1
                print("Auto_save:",self.inactivity_counter)
                if self.inactivity_counter == 0: # 5 min => stop save
                    print("Auto-save stopped due to inactivity.")
                    return
        self.window.after(5000, self.auto_save)

    def check_file(self, base_name):
        cont = 0
        file_name, file_extension = os.path.splitext(base_name)
        while os.path.exists(os.path.join(self.save_directory, base_name)):
            cont += 1
            base_name = f"{file_name}{cont}{file_extension}"
        return base_name
    
    def select_file (self):
        initial_file = initial_file_name
        unique_file = self.check_file(initial_file + ".txt")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile = unique_file,
            initialdir=self.save_directory,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path = file_path
            print(f"File selected: {self.file_path}")
        return file_path
    
    def on_close(self):
        file_path = self.select_file()
        if file_path:
            content = self.inputtxt.get("1.0", END).strip()
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
        self.window.destroy() 
    
    def restore_notes(self):
        existing_files = [f for f in os.listdir(self.save_directory) if f.endswith('.txt')]
        if not existing_files:
            return
        #
        existing_files.sort()
        #
        latest_file = os.path.join(self.save_directory, existing_files[-1])
        with open(latest_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.inputtxt.delete(1.0, END)
            self.inputtxt.insert(END, content)
    