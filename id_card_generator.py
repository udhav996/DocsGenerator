import tkinter as tk
from tkinter import filedialog, messagebox
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
import os

# Setup paths
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "card_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# ------------------ Core Functions ------------------

def generate_id_card(data):
    template = env.get_template("id_card.html")
    html_out = template.render(data)

    file_name = f"{data['name'].replace(' ', '_')}_id_card.pdf"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    # Render and write the PDF
    HTML(string=html_out, base_url=os.getcwd()).write_pdf(file_path)

    try:
        os.startfile(file_path)
    except:
        messagebox.showinfo("Success", f"PDF saved: {file_path}")

def preview_card(data):
    template = env.get_template("id_card.html")
    html_out = template.render(data)
    temp_file = os.path.join(OUTPUT_DIR, "preview_card.html")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(html_out)
    os.startfile(temp_file)

def get_image_path(entry_field):
    path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp")]
    )
    if path:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, os.path.abspath(path))  # insert full path

# ------------------ GUI Setup ------------------

root = tk.Tk()
root.title("Student ID Card Generator")
root.geometry("520x600")

tk.Label(root, text="College ID Card Generator", font=("Arial", 16, "bold")).pack(pady=10)

form = tk.Frame(root)
form.pack(padx=20, pady=10)

def make_entry(label, row):
    tk.Label(form, text=label, width=15, anchor='w').grid(row=row, column=0, sticky='w', pady=5)
    entry = tk.Entry(form, width=40)
    entry.grid(row=row, column=1, pady=5)
    return entry

entry_name = make_entry("Full Name:", 0)
entry_dob = make_entry("Date of Birth:", 1)
entry_admission = make_entry("Admission Date:", 2)
entry_address = make_entry("Address:", 3)
entry_class = make_entry("Class:", 4)
entry_id = make_entry("ID Number:", 5)

entry_photo = make_entry("Student Photo:", 6)
tk.Button(form, text="Choose Photo", command=lambda: get_image_path(entry_photo)).grid(row=6, column=2)

entry_barcode = make_entry("Barcode Image:", 7)
tk.Button(form, text="Choose Barcode", command=lambda: get_image_path(entry_barcode)).grid(row=7, column=2)

# ------------------ Get Data ------------------

def get_data(preview=False):
    def convert(p): return Path(p).resolve()
    def uri(p): return convert(p).as_uri()
    def path_str(p): return str(convert(p))

    photo = entry_photo.get()
    barcode = entry_barcode.get()
    logo = "assets/shahu_logo.png"

    return {
        "name": entry_name.get(),
        "dob": entry_dob.get(),
        "admission_date": entry_admission.get(),
        "address": entry_address.get(),
        "course": entry_class.get(),
        "id_no": entry_id.get(),
        "photo": path_str(photo) if preview else uri(photo),
        "barcode_url": path_str(barcode) if preview else uri(barcode),
        "college_logo": path_str(logo) if preview else uri(logo),
        "signature_url": Path("assets/tc3.png").resolve().as_uri() if not preview else str(
            Path("assets/tc3.png").resolve())

    }


# ------------------ Buttons ------------------
tk.Button(root, text="Preview ID Card", command=lambda: preview_card(get_data(preview=True)),
          bg="#6c757d", fg="white", font=("Arial", 11)).pack(pady=10)

tk.Button(root, text="Generate PDF", command=lambda: generate_id_card(get_data(preview=False)),
          bg="#28a745", fg="white", font=("Arial", 12, "bold")).pack(pady=10)


root.mainloop()
