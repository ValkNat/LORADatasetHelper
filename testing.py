from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import os

class ImageResizerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Resizer and Annotator")

        self.target_directory = ""
        self.resized_images_dir = ""
        self.current_index = 0

        # Create GUI components
        self.label_image = tk.Label(master)
        self.label_image.pack()

        self.text_entry = tk.Entry(master)
        self.text_entry.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.submit_text)
        self.submit_button.pack()

        self.next_button = tk.Button(master, text="Next Image", command=self.show_next_image)
        self.next_button.pack()

        self.choose_directory_button = tk.Button(master, text="Choose Directory", command=self.choose_directory)
        self.choose_directory_button.pack()

        # Initialize the image list
        self.image_files = []

    def choose_directory(self):
        self.target_directory = filedialog.askdirectory()
        self.resized_images_dir = os.path.join(self.target_directory, "resized_images")
        os.makedirs(self.resized_images_dir, exist_ok=True)

        for index, filename in enumerate(os.listdir(self.target_directory)):
            input_path = os.path.join(self.target_directory, filename)
            if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                output_filename = f"{index + 1}.png"
                output_path = os.path.join(self.resized_images_dir, output_filename)

                with Image.open(input_path) as img:
                    resized_img = img.resize((512, 512))
                    resized_img.save(output_path)

        # Update the image_files list with the resized image files
        self.image_files = sorted([f for f in os.listdir(self.resized_images_dir) if f.lower().endswith('.png')])

        self.show_next_image()

    def show_next_image(self):
        if self.current_index < len(self.image_files):
            image_path = os.path.join(self.resized_images_dir, self.image_files[self.current_index])
            img = Image.open(image_path)
            tk_img = ImageTk.PhotoImage(img)

            self.label_image.config(image=tk_img)
            self.label_image.image = tk_img  # keep a reference to avoid garbage collection issues
            self.text_entry.delete(0, tk.END)  # clear the text entry
            self.current_index += 1
        else:
            tk.messagebox.showinfo("End of Images", "No more images to display.")

    def submit_text(self):
        if self.resized_images_dir and self.current_index > 0:
            current_image_name = str(self.current_index)
            text_content = self.text_entry.get()
            txt_file_path = os.path.join(self.resized_images_dir, current_image_name + ".txt")

            with open(txt_file_path, "w") as txt_file:
                txt_file.write(text_content)

            tk.messagebox.showinfo("Text Submitted", f"Text '{text_content}' saved to {current_image_name}.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerGUI(root)
    root.mainloop()
