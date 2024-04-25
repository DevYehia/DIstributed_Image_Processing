import tkinter as tk
from tkinter import  filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from client import *

def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename(title="Select a Photo", filetypes=[("Image Files", "*.png; *.jpg; *.jpeg")])
    if file_path:
        global uploaded_image
        uploaded_image = Image.open(file_path)
        display_image(uploaded_image)
        operation_frame.pack(pady=5)
        apply_button.pack(pady=5)


def display_image(image):
    image.thumbnail((350, 350))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo


def apply_operation(image, operation):
    if operation == "None":
        return image
    elif operation == "gray":
        return image.convert("L")
    elif operation == "Rotate 90°":
        return image.rotate(90)


def apply_operation_and_display():
    operation = selected_operation.get()
    if uploaded_image:
        global modified_image
        send_image(operation,file_path)
        modified_image = apply_operation(uploaded_image, operation)
        display_image(modified_image)
        save_button.pack(pady=5)


def save_image():
    if modified_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("JPEG files", "*.jpeg")])
        if save_path:
            modified_image.save(save_path)


root = tk.Tk()
root.title("Photo Uploader")
root.geometry("650x550")
upload_button = ttk.Button(root, text="Upload Photo", command=open_file_dialog)
upload_button.pack(pady=10)

operation_frame = ttk.Frame(root)
# operation_frame.pack(pady=5)

operation_label = ttk.Label(operation_frame, text="Operation:")
operation_label.pack(side="left", padx=10, pady=5)

operations = ["None", "GrayScale","Invert", "Rotate 90°", ""]
selected_operation = tk.StringVar(root)
selected_operation.set(operations[0])
operation_menu = ttk.OptionMenu(operation_frame, selected_operation, *operations)
operation_menu.pack(side="left", padx=5, pady=5)

apply_button = ttk.Button(root, text="Apply Operation", command=apply_operation_and_display)
# apply_button.pack(pady=5)

# save or download image
save_button = ttk.Button(root, text="Save Image", command=save_image)


image_label = ttk.Label(root)
image_label.pack()

root.mainloop()
