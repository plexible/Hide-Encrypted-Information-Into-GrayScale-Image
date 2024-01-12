from customtkinter import *
from EmbeddingExtractingPart import embedding_to_img, extracting_embedded_data
from cv2 import imwrite
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import string
import warnings
import easygui
warnings.simplefilter("ignore")

class MyApp(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        self.title("Embedding-Extracting")
        self.name = ""
        self.surname = ""
        self.tcno = ""
        self.image_path = None
        self.extraction_file_path = None
        self.tabview = CTkTabview(master=self)
        self.tabview.pack(padx=20, pady=20)

        self.embedding_tab = self.tabview.add("Embedding")
        self.extracting_tab = self.tabview.add("Extracting")

        self.create_embedding_tab()
        self.create_extracting_tab()
    
    def create_embedding_tab(self):
        self.information_frame = CTkFrame(master=self.embedding_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        self.image_frame = CTkFrame(master=self.embedding_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)

        self.information_frame.grid(row=0, column=0, padx=20, pady=20)
        self.image_frame.grid(row=0, column=1, padx=20, pady=(0,200))

        label = CTkLabel(master=self.information_frame, text="Information")
        self.name_entry = CTkEntry(master=self.information_frame, placeholder_text="Name")
        self.surname_entry = CTkEntry(master=self.information_frame, placeholder_text="Surname")
        self.tcno_entry = CTkEntry(master=self.information_frame, placeholder_text="Tcno")


        submit_btn = CTkButton(master=self.information_frame, text="Embedding", command=self.perform_embedding)

        label.pack(anchor="s", expand=True, padx=30, pady=10)
        self.name_entry.pack(anchor="s", expand=True, padx=30, pady=10)
        self.surname_entry.pack(anchor="s", expand=True, padx=30, pady=10)
        self.tcno_entry.pack(anchor="s", expand=True, padx=30, pady=10)
        submit_btn.pack(anchor="n", expand=True, padx=30, pady=20)

        refresh_button = CTkButton(master=self.embedding_tab, text="Refresh", command=self.perform_embedding_refresh)
        refresh_button.grid(row=0, column=0, padx=20, pady=(320,0))

        browse_button = CTkButton(self.image_frame, text="Choose Image", command=self.browse_image)
        browse_button.grid(row=0, column=0, pady=10)

    def create_extracted_information_widgets(self):
        self.show_name = CTkLabel(master=self.extracted_information_frame, text="Name:  " + self.name)
        self.show_surname = CTkLabel(master=self.extracted_information_frame, text="Surname:  " + self.surname)
        self.show_tcno = CTkLabel(master=self.extracted_information_frame, text="Tcno:  " + self.tcno)
        self.submit_btn = CTkButton(master=self.extracted_information_frame, text="Extracting", command=self.perform_extracting)

        self.show_name.pack(anchor="s", expand=True, padx=30, pady=10)
        self.show_surname.pack(anchor="s", expand=True, padx=30, pady=10)
        self.show_tcno.pack(anchor="s", expand=True, padx=30, pady=10)
        self.submit_btn.pack(anchor="n", expand=True, padx=30, pady=20)

    def create_extracting_tab(self):
        self.extracted_information_frame = CTkFrame(master=self.extracting_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        self.extracting_image_frame = CTkFrame(master=self.extracting_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        
        self.extracted_information_frame.grid(row=0, column=1, padx=20, pady=20)
        self.extracting_image_frame.grid(row=0, column=0, padx=20, pady=(0,200))

        label = CTkLabel(master=self.extracted_information_frame, text="Extracted Information  ")
        label.pack(anchor="s", expand=True, padx=30, pady=10)
        
        self.create_extracted_information_widgets()

        refresh_button = CTkButton(master=self.extracting_tab, text="Refresh", command=self.perform_extracting_refresh)
        refresh_button.grid(row=0, column=1, padx=20, pady=(320,0))

        browse_button = CTkButton(self.extracting_image_frame, text="Choose Image", command=self.browse_extracting_image)
        browse_button.grid(row=0, column=0, pady=10)


    def perform_extracting_refresh(self):
        self.name = ""
        self.surname = ""
        self.tcno = ""
        self.extracting_image_frame.destroy()
        self.extracted_information_frame.destroy()
        self.extraction_file_path = ""
        self.create_extracting_tab()

    def perform_embedding_refresh(self):
        self.image_frame.destroy()
        self.information_frame.destroy()
        if hasattr(self, "new_image_frame"):
            getattr(self, "new_image_frame").destroy()
        self.image_path = ""
        self.create_embedding_tab()

    def browse_image(self):  
        try:
            file_path = easygui.fileopenbox(default="*.png;*.jpg;*.jpeg", filetypes=["*.png", "*.jpg", "*.jpeg"])
            if file_path:
                self.image_path = file_path
            else:
                print("The file was not selected or the operation was cancelled.")
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.image_frame.grid(row=0, column=1, padx=20, pady=10)
            self.display_image(photo, self.image_frame, "embedding_label")
        except Exception as e:
            messagebox.showerror("Error", "The file was not selected or the operation was cancelled.")


    def browse_extracting_image(self):
        try:
            file_path = easygui.fileopenbox(default="*.png;*.jpg;*.jpeg", filetypes=["*.png", "*.jpg", "*.jpeg"])
            if file_path:
                self.extraction_file_path = file_path
            else:
                print("The file was not selected or the operation was cancelled.")
            image = Image.open(file_path)
            image.thumbnail((400, 400)) 
            photo = ImageTk.PhotoImage(image)
            self.extracting_image_frame.grid(row=0, column=0, padx=20, pady=10)
            self.display_image(photo, self.extracting_image_frame, "extracting_label")
        except Exception as e:
            messagebox.showerror("Error", "The file was not selected or the operation was cancelled.")

    def validate_english_characters(self, new_text):
        if not all(char in string.ascii_letters + " " for char in new_text):
            self.error_message = "Error: User English characters are allowed."
            return False
        return True

    def validate_tcno(self):
        if len(self.tcno_entry.get()) != 11 or not self.tcno_entry.get().isdigit():
            self.error_message = "Error", "Error: TCNO must be an 11-digit number."
            return False
        return True 
        
    def validations(self):
        entry_name = self.name_entry.get()
        entry_surname = self.surname_entry.get()
        if not entry_name:
            messagebox.showerror("Error", "Name is required.")
            return False
        elif not entry_surname:
            messagebox.showerror("Error", "Surname is required.")
            return False
        elif not self.tcno_entry.get():
            messagebox.showerror("Error", "Tcno is required.")
            return False
        elif (not self.validate_english_characters(entry_name)) or (not self.validate_english_characters(entry_surname)) or (not self.validate_tcno()):
            messagebox.showerror("Error", self.error_message)
            return False
        return True

    def perform_embedding(self):
        if not self.validations():
            return
        if not self.image_path:
            messagebox.showerror("Error", "Choose an image.")
            return 0
        else:
            try:
                info = {"name": self.name_entry.get(), "surname": self.surname_entry.get(), "tcno": self.tcno_entry.get()}
                new_img = embedding_to_img(self.image_path, info)
                
                self.new_image_frame = CTkFrame(master=self.embedding_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
                self.new_image_frame.grid(row=0, column=2, padx=20)
                new_image_label = CTkLabel(master=self.new_image_frame, text="Embedded Image")
                new_image_label.grid(row=0, column=0, pady=10, padx=10)

                img = Image.fromarray(new_img)
                img.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(img)
                self.display_image(photo, self.new_image_frame, "embedded_label")

                messagebox.showinfo("Embedding", "The operation has been completed successfully.")

                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
                if file_path:
                    imwrite(file_path, new_img)
                    messagebox.showinfo("Embedding", "The operation has been completed successfully.")
            except Exception as e:
                self.perform_embedding_refresh()
                messagebox.showerror("Error", f"Embedding operation is failed!")

    def perform_extracting(self):
        if not self.extraction_file_path:
            messagebox.showerror("Error", "Choose an image.")
        else:
            try:
                info = extracting_embedded_data(self.extraction_file_path)
                self.name = info['name']
                self.surname = info['surname']
                self.tcno = info['tcno']
                
                for widget in [self.show_name, self.show_surname, self.show_tcno, self.submit_btn]:
                    widget.destroy()
                    
                self.create_extracted_information_widgets()

                messagebox.showinfo("Extracting", "The operation has been completed successfully.")
            except Exception as e:
                self.perform_extracting_refresh()
                messagebox.showerror("Error", f"Information could not be extracted from the image")

    def display_image(self, photo, frame, label_name):
        if hasattr(self, label_name):
            getattr(self, label_name).destroy()
        new_label = CTkLabel(frame, image=photo, text="")
        warnings.resetwarnings()
        new_label.image = photo
        new_label.grid(row=1, column=0, pady=10, padx=10)

        setattr(self, label_name, new_label)


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()    