import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
import os

# Setup output and templates folder
OUTPUT_DIR = "card_outputs"
TEMPLATE_DIR = "templates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Jinja2 Environment
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_card_pdf(data, template_name):
    template = env.get_template(template_name)
    html_out = template.render(data)

    file_name = f"{data['name'].replace(' ', '_')}_card.pdf"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    HTML(string=html_out, base_url=os.getcwd()).write_pdf(
        file_path,
        stylesheets=[],
        presentational_hints=True
    )

    try:
        os.startfile(file_path)
    except:
        print("PDF generated:", file_path)

def preview_card(data, template_name):
    template = env.get_template(template_name)
    html_out = template.render(data)
    temp_file = os.path.join(OUTPUT_DIR, "preview_card.html")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(html_out)
    os.startfile(temp_file)

# GUI Setup
root = tk.Tk()
root.title("Visiting Card Generator")
root.geometry("500x600")

tk.Label(root, text="Visiting Card Generator", font=("Arial", 16, "bold")).pack(pady=10)
form = tk.Frame(root)
form.pack(padx=20, pady=10)

def make_entry(label, row):
    tk.Label(form, text=label, width=15, anchor='w').grid(row=row, column=0, sticky='w', pady=5)
    entry = tk.Entry(form, width=40)
    entry.grid(row=row, column=1, pady=5)
    return entry

entry_name = make_entry("Full Name:", 0)
entry_title = make_entry("Job Title:", 1)
entry_phone = make_entry("Phone:", 2)
entry_email = make_entry("Email:", 3)
entry_website = make_entry("Website:", 4)
entry_address = make_entry("Address:", 5)

# Template Dropdown
tk.Label(form, text="Card Template:", anchor="w", width=15).grid(row=6, column=0, sticky="w", pady=5)
template_var = tk.StringVar(value="black & gold geometric_card.html")

template_dropdown = ttk.Combobox(
    form,
    textvariable=template_var,
    values=["black & gold geometric_card.html",
            "red_modern_card.html",
            "blue_gradient_card.html",
            ],
             width=37
)
template_dropdown.grid(row=6, column=1, pady=5)

# Buttons
def get_data():
    selected_template = template_var.get()

    logo_file = {
        "black & gold geometric_card.html": "templates/tech_logo3.jpg",
        "red_modern_card.html": "templates/OIP.jpeg",
        "blue_gradient_card.html": "templates/big_bull.png",
    }.get(selected_template, "templates/default_logo.png")

    return {
        "name": entry_name.get(),
        "title": entry_title.get(),
        "phone": entry_phone.get(),
        "email": entry_email.get(),
        "website": entry_website.get(),
        "address": entry_address.get(),
        "logo_url": Path(logo_file).resolve().as_uri()
    }


tk.Button(root, text="Preview Card", command=lambda: preview_card(get_data(), template_var.get()), bg="#444", fg="white").pack(pady=10)
tk.Button(root, text="Generate PDF", command=lambda: generate_card_pdf(get_data(), template_var.get()), bg="#007BFF", fg="white").pack(pady=10)

root.mainloop()
