import tkinter as tk
import settings_ui

def button_click(): 
    exec(open("src\control.py").read())

def open_settings_window():
    settings_ui.show_settings_window()

def close_main_window(root):
    root.destroy() 

def run_ui():
    #main window
    root = tk.Tk()
    root.title("Mouse Control")
    root.geometry("800x500")
    root.resizable(width=False, height=False)
    root.configure(bg="#EFDEFF")

    #frame
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, fill=tk.X, pady=75)
    frame.configure(bg="#EFDEFF")
    
    #button1 start button
    button1 = tk.Button(frame, text="Start", command=button_click, height=2, width=25)
    button1.pack(side=tk.TOP, pady=25)

    #button2 settings 
    button2 = tk.Button(frame, text="Settings", command=open_settings_window, height=2, width=25)
    button2.pack(side=tk.TOP, pady=25)

    #button3 exit 
    button3 = tk.Button(frame, text="Exit", command=lambda: close_main_window(root), height=2, width=25)
    button3.pack(side=tk.TOP, pady=25)

    root.mainloop()

if __name__ == "__main__":
    run_ui()
