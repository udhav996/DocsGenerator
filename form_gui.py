import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from generator import generate_tc

def submit_form():
    data = {
        "name": entry_name.get(),
        "mother_name": entry_mother.get(),
        "religion": entry_religion.get(),
        "dob": entry_dob.get(),
        "nationality": entry_nationality.get(),
        "leaving_date": entry_leaving.get(),
        "reason": reason_var.get(),
        "student_class": class_var.get(),
        # "tc_no" is now auto-generated in generator.py
    }

    missing_fields = []

    if not data["name"]:
        missing_fields.append("Student Name")
    if not data["mother_name"]:
        missing_fields.append("Mother's Name")
    if not data["dob"]:
        missing_fields.append("Date of Birth")
    if not data["religion"]:
        missing_fields.append("Religion")
    if not data["nationality"]:
        missing_fields.append("Nationality")
    if not data["leaving_date"]:
        missing_fields.append("Date of Leaving")
    if not data["reason"]:
        missing_fields.append("Reason for Leaving")
    if not data["student_class"]:
        missing_fields.append("Class")

    if missing_fields:
        messagebox.showerror("Missing Fields", "Please fill the following fields:\n" + "\n".join(missing_fields))
        return

    generate_tc(data)
    messagebox.showinfo("Success", "Transfer Certificate generated successfully!")

# GUI Window
root = tk.Tk()
root.title("Transfer Certificate Generator - Udhav Academy")
root.geometry("650x600")
root.configure(bg="#f0f8ff")

tk.Label(root, text="Transfer Certificate Form", bg="#f0f8ff", font=("Arial", 14, "bold")).pack(pady=10)

form_frame = tk.Frame(root, bg="#f0f8ff")
form_frame.pack()

# Create input fields
def create_field(label, row):
    tk.Label(form_frame, text=label, bg="#f0f8ff", font=("Arial", 10, "bold"), anchor="e", width=22).grid(row=row, column=0, padx=10, pady=5)
    entry = tk.Entry(form_frame, width=40)
    entry.grid(row=row, column=1, padx=10, pady=5)
    return entry

entry_name = create_field("1. Student Full Name:", 0)
entry_mother = create_field("2. Mother's Name:", 1)
entry_religion = create_field("3. Religion:", 2)

# Date of Birth
tk.Label(form_frame, text="4. Date of Birth:", bg="#f0f8ff", font=("Arial", 10, "bold"), anchor="e", width=22).grid(row=3, column=0, padx=10, pady=5)
entry_dob = DateEntry(form_frame, width=37, date_pattern='dd/mm/yyyy')
entry_dob.grid(row=3, column=1, padx=10, pady=5)

entry_nationality = create_field("5. Nationality:", 4)

# Date of Leaving
tk.Label(form_frame, text="6. Date of Leaving:", bg="#f0f8ff", font=("Arial", 10, "bold"), anchor="e", width=22).grid(row=5, column=0, padx=10, pady=5)
entry_leaving = DateEntry(form_frame, width=37, date_pattern='dd/mm/yyyy')
entry_leaving.grid(row=5, column=1, padx=10, pady=5)

# Reason Dropdown
reason_var = tk.StringVar()
tk.Label(form_frame, text="7. Reason for Leaving:", bg="#f0f8ff", font=("Arial", 10, "bold"), anchor="e", width=22).grid(row=6, column=0, padx=10, pady=5)
reason_dropdown = ttk.Combobox(form_frame, textvariable=reason_var,
                               values=["Completed Course", "Personal Reason", "Transfer", "Medical Reason", "Other"],
                               width=37)
reason_dropdown.grid(row=6, column=1, padx=10, pady=5)

# Class Dropdown
tk.Label(form_frame, text="8. Class:", bg="#f0f8ff", font=("Arial", 10, "bold"), anchor="e", width=22).grid(row=7, column=0, padx=10, pady=5)
class_var = tk.StringVar()
class_dropdown = ttk.Combobox(form_frame, textvariable=class_var,
                              values=["10th", "12th", "BCA I YEAR", "BCA II YEAR", "BCA III YEAR"],
                              width=37)
class_dropdown.grid(row=7, column=1, padx=10, pady=5)

# Submit Button
tk.Button(
    root,
    text="Generate TC",
    command=submit_form,
    bg="#003366",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=5
).pack(pady=20)

root.mainloop()
