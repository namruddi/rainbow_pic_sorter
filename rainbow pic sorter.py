import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import os
import shutil

def get_dominant_color(image_path):
    # Открываем изображение и преобразуем в RGB
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = np.array(img)
    
    # Используем метод HSL для получения более точного анализа цвета
    avg_color = np.mean(pixels, axis=(0, 1))  # Средний цвет по всем пикселям
    return avg_color

def get_color_label(color):
    r, g, b = color
    # Определяем цвет на основе значений RGB
    if r > g and r > b:
        return 'Red'
    elif r > b and g > b:
        return 'Orange'
    elif g > r and g > b:
        return 'Yellow'
    elif g > r and b > g:
        return 'Green'
    elif b > g and b > r:
        return 'Blue'
    elif b > r and g > r:
        return 'Indigo'
    else:
        return 'Violet'

def sort_images_by_rainbow_color(directory):
    files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_colors = []

    for file in files:
        path = os.path.join(directory, file)
        color = get_dominant_color(path)
        label = get_color_label(color)
        image_colors.append((file, label))

    # Строгий порядок цветов радуги
    rainbow_order = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet']
    sorted_images = sorted(image_colors, key=lambda x: rainbow_order.index(x[1]))
    
    return sorted_images

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_label.config(text=folder_path)

def start_sorting():
    folder_path = folder_label.cget("text")
    if folder_path:
        sorted_images = sort_images_by_rainbow_color(folder_path)
        result_label.config(text=f"Sorting Complete! Found {len(sorted_images)} images.")
        return sorted_images
    else:
        result_label.config(text="No folder selected!")

def export_sorted_images(sorted_images):
    folder_path = folder_label.cget("text")
    export_folder = filedialog.askdirectory(title="Select Export Folder")
    if export_folder:
        count = 1
        for image, label in sorted_images:
            image_path = os.path.join(folder_path, image)
            base_name, ext = os.path.splitext(image)
            new_name = f"{count}_{base_name}{ext}"  # Цифра в начале
            count += 1
            new_path = os.path.join(export_folder, new_name)
            shutil.copy(image_path, new_path)

        result_label.config(text="Export Completed!")

# GUI setup
root = tk.Tk()
root.title("Photo Sorting by Rainbow Color")

# Folder selection label and button
folder_label = tk.Label(root, text="No folder selected", width=40, anchor='w')
folder_label.pack(pady=10)

select_button = tk.Button(root, text="Select Folder for Import/Export", command=select_folder)
select_button.pack(pady=5)

# Sorting and exporting buttons
sort_button = tk.Button(root, text="Start Sorting", command=lambda: start_sorting())
sort_button.pack(pady=5)

export_button = tk.Button(root, text="Export Sorted Images", command=lambda: export_sorted_images(start_sorting()))
export_button.pack(pady=5)

# Result label
result_label = tk.Label(root, text="", width=40, anchor='w')
result_label.pack(pady=10)

# Color palette display
color_palette_frame = tk.Frame(root)
color_palette_frame.pack(pady=20)

# Correct color names for the rainbow order
rainbow_colors = {
    'Red': '#FF0000',
    'Orange': '#FFA500',
    'Yellow': '#FFFF00',
    'Green': '#008000',
    'Blue': '#0000FF',
    'Indigo': '#4B0082',
    'Violet': '#8A2BE2'
}

def display_palette():
    for widget in color_palette_frame.winfo_children():
        widget.destroy()

    for color, hex_code in rainbow_colors.items():
        color_label = tk.Label(color_palette_frame, text=color, width=10, height=2, bg=hex_code)
        color_label.pack(side="left", padx=5)

display_palette()

root.mainloop()
