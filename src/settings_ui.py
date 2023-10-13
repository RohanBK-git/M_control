import tkinter as tk
import configparser

#loads the config file
config = configparser.ConfigParser()
config.read('src\config.ini')

#
def show_settings_window():
    def save_settings():
        #updates the new values into the config file
        config['MouseControl']['val_left'] = entry1.get()
        config['MouseControl']['val_right'] = entry2.get()
        config['MouseControl']['val_left_area'] = entry3.get()
        config['MouseControl']['val_right_area'] = entry4.get()
        config['MouseControl']['val_scrolling'] = entry5.get()

        with open('src\config.ini', 'w') as configfile:
            config.write(configfile)

        #message when save button clicked
        saved_label.config(text="Data has been saved")
        settings_window.after(5000, lambda: saved_label.config(text=""))

    def reset_settings():

        #restores the default values present in the config file
        config['MouseControl']['val_left'] = config['DefaultValues']['val_left']
        config['MouseControl']['val_right'] = config['DefaultValues']['val_right']
        config['MouseControl']['val_left_area'] = config['DefaultValues']['val_left_area']
        config['MouseControl']['val_right_area'] = config['DefaultValues']['val_right_area']
        config['MouseControl']['val_scrolling'] = config['DefaultValues']['val_scrolling']

        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)
        entry4.delete(0, tk.END)
        entry5.delete(0, tk.END)

        entry1.insert(0, config['MouseControl']['val_left'])
        entry2.insert(0, config['MouseControl']['val_right'])
        entry3.insert(0, config['MouseControl']['val_left_area'])
        entry4.insert(0, config['MouseControl']['val_right_area'])
        entry5.insert(0, config['MouseControl']['val_scrolling'])

        #message when reset button is pressed
        restored_label.config(text="Default values has been restored")
        settings_window.after(5000, lambda: restored_label.config(text=""))
        
    #to exit the window
    def cancel_settings():
        settings_window.destroy()

    #createing new settings window
    settings_window = tk.Toplevel()
    settings_window.title("Settings")

    settings_window.geometry("400x500")
    settings_window.resizable(width=False, height=False)

    #creating frame
    frame = tk.Frame(settings_window)
    frame.pack(side=tk.TOP, pady=20)

    #labels for input fields 
    labels = ["Left:", "Right:", "Left Area:", "Right Area:", "Mouth:"]
    entries = []

    for label_text in labels:
        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.TOP)

        entry = tk.Entry(frame)
        entry.pack(side=tk.TOP)

        entries.append(entry)

    entry1, entry2, entry3, entry4, entry5 = entries

    #inserting existing values in the config file to the input fields
    entry1.insert(0, config['MouseControl']['val_left'])
    entry2.insert(0, config['MouseControl']['val_right'])
    entry3.insert(0, config['MouseControl']['val_left_area'])
    entry4.insert(0, config['MouseControl']['val_right_area'])
    entry5.insert(0, config['MouseControl']['val_scrolling'])

    #frame for buttons
    button_frame = tk.Frame(settings_window)
    button_frame.pack(side=tk.BOTTOM, pady=20)

    #save button
    save_button = tk.Button(button_frame, text="Save", command=save_settings, height= 2, width = 7)
    save_button.pack(side=tk.RIGHT, padx=20)

    #reset button
    reset_button = tk.Button(button_frame, text="Reset", command=reset_settings, height= 2, width = 7)
    reset_button.pack(side=tk.RIGHT, padx= 20)

    #cancel button
    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_settings, height= 2, width = 7)
    cancel_button.pack(side=tk.LEFT, padx=20)

    #label displayed after saving
    saved_label = tk.Label(settings_window, text="", fg="green")
    saved_label.pack(side=tk.BOTTOM, pady=10)

    #label displayed after restoring default values
    restored_label = tk.Label(settings_window, text="", fg="green")
    restored_label.pack(side=tk.BOTTOM, pady=10)

    settings_window.mainloop()

if __name__ == "__main__":
    show_settings_window()
