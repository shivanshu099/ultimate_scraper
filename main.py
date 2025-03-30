from PIL import Image
Image.CUBIC = Image.BICUBIC

import tkinter as tk
from ttkbootstrap import Window, Label, Entry, Button, Combobox
from ttkbootstrap.constants import *
from flip import scrape_flipkart_products  # Ensure these functions accept an output_csv parameter
from dry import scrape_amazon_products

def scrape_flipkart(query, page_size, filename):
    scrape_flipkart_products(query, page_size, output_csv=filename)
    return f"Data scrape successful! Saved to {filename}"

def scrape_amazon(query, page_size, filename):
    scrape_amazon_products(query, page_size, output_csv=filename)
    return f"Data scrape successful! Saved to {filename}"

def on_scrape():
    website_choice = website_combo.get()
    query_text = query_var.get().strip()
    file_name = filename_var.get().strip()
    
    if not query_text:
        status_label.config(text="Enter a search query!")
        return
    if not file_name:
        status_label.config(text="Enter a file name (e.g., results.csv)!")
        return
    try:
        pages = int(page_var.get().strip())
    except ValueError:
        status_label.config(text="Pages must be an integer!")
        return
    
    if website_choice == "Flipkart":
        message = scrape_flipkart(query_text, pages, file_name)
    elif website_choice == "Amazon":
        message = scrape_amazon(query_text, pages, file_name)
    else:
        message = "Invalid website choice!"
        
    status_label.config(text=message)

# Main window setup using the vapor theme
root = Window(themename="vapor")
root.title("Ultimate Scraper")
root.geometry("400x540")
root.resizable(False, False)
default_font = ("Segoe UI", 11)

# Header label with white text
header_label = Label(root, text="Ultimate Scraper", font=("jokerman", 21), foreground="white")
header_label.pack(pady=10)

# Prominent animated name label at the top
name_label = Label(root, text="(Made by Shivanshu Prajapati)", font=("Segoe UI", 11, "bold"))
name_label.pack(pady=5)

# Animation: cycle through bright colors for a "shining" effect on the name label
colors = ["#FFD700", "#FFA500", "#FF4500", "#FF00FF", "#00FFFF"]  # gold, orange, orange-red, magenta, cyan
color_index = 0
def animate_name():
    global color_index
    name_label.config(foreground=colors[color_index])
    color_index = (color_index + 1) % len(colors)
    root.after(500, animate_name)
animate_name()

# Website dropdown
website_label = Label(root, text="Select Website:", font=default_font, foreground="white")
website_label.pack(pady=5)
website_combo = Combobox(root, values=["Flipkart", "Amazon"], font=default_font, state="readonly")
website_combo.current(0)
website_combo.pack(pady=5)

# Search query input
query_label = Label(root, text="Search Query:", font=default_font, foreground="white")
query_label.pack(pady=5)
query_var = tk.StringVar()
query_entry = Entry(root, textvariable=query_var, font=default_font, foreground="white", background="#333333")
query_entry.pack(pady=5)

# Pages input
pages_label = Label(root, text="Pages to Scrape:", font=default_font, foreground="white")
pages_label.pack(pady=5)
page_var = tk.StringVar(value="2")
pages_entry = Entry(root, textvariable=page_var, font=default_font, foreground="white", background="#333333")
pages_entry.pack(pady=5)

# Output file name input
filename_label = Label(root, text="Output File Name (with .csv):", font=default_font, foreground="white")
filename_label.pack(pady=5)
filename_var = tk.StringVar()
filename_entry = Entry(root, textvariable=filename_var, font=default_font, foreground="white", background="#333333")
filename_entry.pack(pady=5)

# Scrape button
scrape_button = Button(root, text="Scrape", bootstyle="light", command=on_scrape)
scrape_button.pack(pady=15)

# Status label for feedback with white text
status_label = Label(root, text="", font=("Segoe UI", 12), foreground="white")
status_label.pack(pady=10)

# Prominent footer credit with center alignment
#footer_label = Label(root, text="Made by Shivanshu Prajapati", font=("Segoe UI", 12, "bold"), bootstyle="warning", foreground="white")
#footer_label.pack(side="bottom", fill="x", pady=10)

root.mainloop()


#pyinstaller --onefile --windowed --add-data "hacker.png;images" main.py
#pyinstaller --onefile --windowed --name "Ultimate Scraper" --add-data "hacker.png;images" main.py






