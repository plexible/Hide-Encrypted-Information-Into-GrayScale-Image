from EmbeddingExtractingPart import embedding_to_img, extracting_embedded_data

from cv2 import imwrite, imread
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Embedding and Extracting App")
        self.name = ""
        self.surname = ""
        self.tcno = ""
        # ThemedStyle for changing theme
        self.style = ThemedStyle(self.root)
        self.style.set_theme("ubuntu")  # Theme

        # Notebooks
        self.notebook = ttk.Notebook(root, style="TNotebook")
        self.notebook.pack(pady=10, expand=True, fill=tk.BOTH)

        # Frames for each page
        self.embedding_frame = ttk.Frame(self.notebook)
        self.extracting_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.embedding_frame, text="Embedding")
        self.notebook.add(self.extracting_frame, text="Extracting")

        # Embedding Page Content
        self.image_label = ttk.Label(self.embedding_frame, text="Image:")
        self.image_label.grid(row=3, column=0, padx=10, pady=10)
        self.browse_button = ttk.Button(self.embedding_frame, text="Choose Image", command=self.browse_image)
        self.browse_button.grid(row=3, column=1, padx=10, pady=10)

        # Panel for displaying selected image
        self.image_panel = ttk.LabelFrame(self.embedding_frame, text="Chosen Image", width=400, height=400)
        self.image_panel.grid(row=4, column=1, pady=20, padx=10, rowspan=2)

        # Information Frame
        self.information_frame = ttk.LabelFrame(self.embedding_frame, text="Information")
        self.information_frame.grid(row=4, column=0, pady=20, padx=10)

        self.information_name_label = ttk.Label(self.information_frame, text="Name:")
        self.information_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.information_name_entry = ttk.Entry(self.information_frame)
        self.information_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.information_surname_label = ttk.Label(self.information_frame, text="Surname:")
        self.information_surname_label.grid(row=1, column=0, padx=10, pady=10)
        self.information_surname_entry = ttk.Entry(self.information_frame)
        self.information_surname_entry.grid(row=1, column=1, padx=10, pady=10)

        self.information_tcno_label = ttk.Label(self.information_frame, text="TC No:")
        self.information_tcno_label.grid(row=2, column=0, padx=10, pady=10)
        self.information_tcno_entry = ttk.Entry(self.information_frame)
        self.information_tcno_entry.grid(row=2, column=1, padx=10, pady=10)

        # Image Path Label
        self.image_path_label = ttk.Label(self.image_panel, text="")
        self.image_path_label.grid(row=0, column=0, pady=10)

        # Embedding Button
        self.embedding_button = ttk.Button(self.embedding_frame, text="Embedding", command=self.perform_embedding)
        self.embedding_button.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Extracting Page Content
        self.extracting_image_label = ttk.Label(self.extracting_frame, text="Image:")
        self.extracting_image_label.grid(row=0, column=0, padx=10, pady=10)
        self.extracting_browse_button = ttk.Button(self.extracting_frame, text="Choose Image", command=self.browse_extracting_image)
        self.extracting_browse_button.grid(row=0, column=1, padx=10, pady=10)

        # Panel for displaying selected image in extracting frame
        self.extracting_image_panel = ttk.LabelFrame(self.extracting_frame, text="Chosen Image", width=400, height=400)
        self.extracting_image_panel.grid(row=1, column=1, pady=20, padx=10, rowspan=2)

        # Extracting Information Frame
        self.extracting_information_frame = ttk.LabelFrame(self.extracting_frame, text="Extracted Information")
        self.extracting_information_frame.grid(row=1, column=0, pady=20, padx=10)

        self.extracting_information_name_label = ttk.Label(self.extracting_information_frame, text="Name: ")
        self.extracting_information_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.extracting_information_surname_label = ttk.Label(self.extracting_information_frame, text="Surname: ")
        self.extracting_information_surname_label.grid(row=1, column=0, padx=10, pady=10)
        self.extracting_information_tcno_label = ttk.Label(self.extracting_information_frame, text="TC No: ")
        self.extracting_information_tcno_label.grid(row=2, column=0, padx=10, pady=10)

        # Extracting Image Path Label
        self.extracting_image_path_label = ttk.Label(self.extracting_image_panel, text="")
        self.extracting_image_path_label.grid(row=0, column=0, pady=10)

        # Extracting Button
        self.extracting_button = ttk.Button(self.extracting_frame, text="Extracting", command=self.perform_extracting)
        self.extracting_button.grid(row=3, column=0, columnspan=2, pady=10)

        
    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.image_path = file_path
        image = Image.open(file_path)
        image.thumbnail((400, 400))  
        photo = ImageTk.PhotoImage(image)

        self.display_image(photo, self.image_panel)

    def browse_extracting_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.extraction_file_path = file_path
        print(self.extraction_file_path)
        image = Image.open(file_path)
        image.thumbnail((400, 400)) 
        photo = ImageTk.PhotoImage(image)

        self.display_image(photo, self.extracting_image_panel)

    def perform_embedding(self):
        info = {"name": self.information_name_entry.get(), "surname": self.information_surname_entry.get(),
                "tcno": self.information_tcno_entry.get()}
        
        new_img = embedding_to_img(self.image_path, info)

        self.new_image_panel = ttk.LabelFrame(self.embedding_frame, text="Embedded Image", width=400, height=400)
        self.new_image_panel.grid(row=4, column=2, pady=20, padx=10, rowspan=2)

        image = Image.fromarray(new_img)
        image.thumbnail((400, 400)) 
        photo = ImageTk.PhotoImage(image)
        self.display_image(photo, self.new_image_panel)
        messagebox.showinfo("Embedding", "The operation has been completed successfully.")
        
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if not file_path:
            return
        imwrite(file_path, new_img)
        print(f"Resim başarıyla kaydedildi: {file_path}")
        messagebox.showinfo("Embedding", "The operation has been completed successfully.")

    def perform_extracting(self):
        info = extracting_embedded_data(self.extraction_file_path)
        self.name = info['name']
        self.surname = info['surname']
        self.tcno = info['tcno']
        self.extracting_information_name_label = ttk.Label(self.extracting_information_frame, text="Name: "+self.name)
        self.extracting_information_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.extracting_information_surname_label = ttk.Label(self.extracting_information_frame, text="Surname: "+self.surname)
        self.extracting_information_surname_label.grid(row=1, column=0, padx=10, pady=10)
        self.extracting_information_tcno_label = ttk.Label(self.extracting_information_frame, text="TC No: "+self.tcno)
        self.extracting_information_tcno_label.grid(row=2, column=0, padx=10, pady=10)
        messagebox.showinfo("Extracting", "The operation has been completed successfully.")

    def display_image(self, photo, panel):
        label = ttk.Label(panel, image=photo)
        label.image = photo  
        label.grid(row=0, column=0, pady=10, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
