# This application can be used to convert private key files (*.p12) into *.key and *.cer files
#
# To execute from terminal or Git Bash, run the following command: python p12_converter.py
#
# Author: Alexander McLaughlin / September 2023

import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfile
import subprocess
from tkinter import messagebox
from pathlib import Path

# Beginning of window
root = tk.Tk()
root.eval("tk::PlaceWindow . center")
root.title("Private Key Converter Tool")

# Setting canvas size
canvas = tk.Canvas(root, width=200, height=100)

# Dialog Box Instuctions
converter = tk.Label(root, text="Upload a Private Key to Convert", font=("Raleway", 18))
converter.pack()

# Radio Button Function
def radio_btn_select():
    global platform
    if radio_buttons.get() == 0:
        platform = 0
    else:
        platform = 1
    return platform

# Set Radio Buttons
radio_buttons = tk.IntVar(value=3)
radio_btn_desc = tk.Label(root, text="Select a platform that the certificate is being used for: ", font=("Raleway", 8))
radio_btn_desc.pack()
radio_btn1 = tk.Radiobutton(root, text="AWS Certificate", value=0, variable=radio_buttons, font=("Raleway", 8), command=radio_btn_select)
radio_btn1.pack(anchor="center")
radio_btn2 = tk.Radiobutton(root, text="OCP Certificate", value=1, variable=radio_buttons, font=("Raleway", 8), command=radio_btn_select)
radio_btn2.pack(anchor="center")

# Browse for file and Convert
def open_file():
    browse_file.set("Loading...")
    pfx_file = askopenfile(parent=root, title="Choose a file", filetype=[("Personal Information Exchange", "*.p12")])
    file_name = Path(pfx_file.name).stem
    global cert_platform
    if platform == 0:
        cert_platform = "aws_gloo"
# Validate User Input for Environment  
        env = simpledialog.askstring(title="Environment", prompt="Enter the environment (ie: dev/test/prod):")
        env = env.lower()
        environments = ['dev', 'test', 'prod']
        for envCheck in environments:
            if env == 'dev':
                break
            elif env == 'test':
                break
            elif env == 'prod':
                break
            else:
                messagebox.showerror("Error", "Incorrect Input: Please re-enter the Environment (i.e. dev/test/prod): ")
                env = simpledialog.askstring(title="Environment", prompt="Enter the environment (ie: dev/test/prod):")
                env = env.lower()
            print(envCheck)
    else:
        platform == 1
        cert_platform = file_name
    if pfx_file:
# Prompt for Certificate Password
        pass_prompt = simpledialog.askstring(title="Passphrase", prompt="Enter the passphrase:")
# Clean up Radio Buttons
        converter.destroy()
        browse_btn.destroy()
        radio_btn1.destroy()
        radio_btn2.destroy()
        radio_btn_desc.destroy()
# Convert Certificates
        try:
            if platform == 0:
                subprocess.run("openssl pkcs12 -in " + pfx_file.name + " -nocerts -nodes -password pass:" + pass_prompt + " | openssl pkcs8 -nocrypt -out " + cert_platform + "_key_" + env + ".key", shell=True, check=True)
                subprocess.run("openssl pkcs12 -in " + pfx_file.name + " -nokeys -chain -out " + cert_platform + "_cert_" + env + ".cer -password pass:" + pass_prompt, shell=True, check=True)
            elif platform == 1:
                subprocess.run("openssl pkcs12 -in " + pfx_file.name + " -nocerts -nodes -password pass:" + pass_prompt + " | openssl pkcs8 -nocrypt -out " + cert_platform + "_key.key", shell=True, check=True)
                subprocess.run("openssl pkcs12 -in " + pfx_file.name + " -nokeys -chain -out " + cert_platform + "_cert.cer -password pass:" + pass_prompt, shell=True, check=True)
            exit_program()
        except subprocess.CalledProcessError as error_msg:
            error_msg = "Conversion failed. Ensure the password was entered correctly."
            messagebox.showerror("Error", error_msg)
            exit()

# Exit Program
def exit_program():
    exit_window_text = tk.StringVar()
    exit_window_btn = tk.Button(root, textvariable=exit_window_text, command=root.destroy, font="Arial", bg="chartreuse1", fg="black", height=2, width=35)
    exit_window_text.set("Success! Click here to close the window.")
    exit_window_btn.pack()

# Browse button
browse_file = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_file, command=lambda:open_file(), font="Arial", bg="azure4", fg="white", height=2, width=10)
browse_btn.pack()
browse_file.set("Browse")

# End of window
root.mainloop()