import tkinter as tk
from tkinter import messagebox
import subprocess


# Define your tool paths (make sure these Python files exist)
tools = {
    "TC Generator": "form_gui.py",
    "ID card Generator": "id_card_generator.py",
    "visiting Card Creator": "card_maker.py"
}

# Function to launch tools
def launch_tool(script):
    try:
        subprocess.Popen(["python", script], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open {script}\n{e}")

# Tkinter GUI setup
root = tk.Tk()
root.title("Document Tools Launcher")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

tk.Label(root, text="📄 Welcome to Document Tools", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

# Buttons for each tool
for tool_name, script_name in tools.items():
    tk.Button(
        root,
        text=tool_name,
        command=lambda s=script_name: launch_tool(s),
        font=("Arial", 12),
        width=30,
        bg="#007BFF",
        fg="white",
        relief="raised",
        bd=2
    ).pack(pady=10)

# Exit Button
tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), bg="gray", fg="white", width=15).pack(pady=20)

root.mainloop()
