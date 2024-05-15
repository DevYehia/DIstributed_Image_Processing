import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from client import *

widgets = []
column_frames = []
def open_file_dialog():
    file_paths = filedialog.askopenfilenames(title="Select Photos", filetypes=[("Image Files", "*.png; *.jpg; *.jpeg")])
    if file_paths:
        global uploaded_images
        uploaded_images = list(file_paths)
        for widget_row in widgets:
            for widget in widget_row:
                widget.destroy()
        widgets.clear()
        display_images()

        operation_frame.pack(pady=5)
        apply_button.pack(pady=5)


server_images=[]
finished = False




def display_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((350, 350))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo



def display_images():
    global column_frames
    if len(column_frames) != 0:
        for frame in column_frames:
            frame.destroy()
    column_frames = [ttk.Frame(container_frame) for _ in range(3)]
    for frame in column_frames:
        # frame.pack_propagate(False)
        frame.pack(side='left', padx=20)
    for i, file_path in enumerate(uploaded_images):
        row_widgets = [
            ttk.Label(column_frames[0], text=f'{i + 1}- {file_path.split("/")[-1]}'),
            ttk.Label(column_frames[1], text='progress information ...'),
            ttk.Button(column_frames[2], text="Preview Image", command=lambda f=file_path: display_image(f))
        ]
        widgets.append(row_widgets)

    for row_widgets in widgets:
        for widget in row_widgets:
            widget.pack(padx=5, pady=5)


def change_label_value(index: int, text: str):
    widgets[index][2].configure(text=text)




def apply_operation_and_display():
    ...
    operation = selected_operation.get()

    if uploaded_images:
        server_images = applyImageOp(uploaded_images,operation)
        for row_widgets, image_path in zip(widgets, server_images):
            row_widgets[-1].configure(command=lambda f=image_path: display_image(f))
        uploaded_images.clear()




def save_image():
    ...
    # if modified_image:
    #     save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("JPEG files", "*.jpeg")])
    #     if save_path:
    #         modified_image.save(save_path)


WIDTH = 1000
HEIGHT = 650
POS_X = 400
POS_Y = 200

root = tk.Tk()
root.title("Distributed Computing Project")
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

upload_button = ttk.Button(root, text="Upload Photo", command=open_file_dialog)
upload_button.pack(pady=10)

operation_frame = ttk.Frame(root)
operation_frame.pack(pady=5)

# operation_frame.pack(pady=5)

operation_label = ttk.Label(operation_frame, text="Operation:")
operation_label.pack(side="left", padx=10, pady=5)

operations = ["None", "GrayScale", "Rotate 90°", "Invert","Edge Detection","Threshold","Contrast"]
selected_operation = tk.StringVar(root)
selected_operation.set(operations[0])
operation_menu = ttk.OptionMenu(operation_frame, selected_operation, *operations)
operation_menu.pack(side="left", padx=5, pady=5)

apply_button = ttk.Button(root, text="Apply Operation", command=apply_operation_and_display)
# apply_button.pack(pady=5)

# save or download image
save_button = ttk.Button(root, text="Save Image", command=save_image)

container_frame = ttk.Frame(root)
container_frame.pack(pady=20)

image_label = ttk.Label(root)
image_label.pack(pady=20)

if __name__ == '__main__':
    root.mainloop()
