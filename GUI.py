from customtkinter import *
from EmbeddingExtractingPart import embedding_to_img, extracting_embedded_data
from cv2 import imwrite
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import string

class MyApp(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
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

    def create_extracting_tab(self):
        self.extracted_information_frame = CTkFrame(master=self.extracting_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        self.extracting_image_frame = CTkFrame(master=self.extracting_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        
        self.extracted_information_frame.grid(row=0, column=1, padx=20, pady=20)
        self.extracting_image_frame.grid(row=0, column=0, padx=20, pady=(0,130))


        label = CTkLabel(master=self.extracted_information_frame, text="Extracted Information  ")
        self.show_name = CTkLabel(master=self.extracted_information_frame, text="Name:  ")
        if not self.name_entry.get().isascii() or not self.name_entry.get().isascii() :
            messagebox.showerror("Error", "Please enter English characters only.")
        self.show_surname = CTkLabel(master=self.extracted_information_frame, text="Surname:  ")
        self.show_tcno = CTkLabel(master=self.extracted_information_frame, text="Tcno:  ")
        self.submit_btn = CTkButton(master=self.extracted_information_frame, text="Extracting", command=self.perform_extracting)

        label.pack(anchor="s", expand=True, padx=30, pady=10)
        self.show_name.pack(anchor="s", expand=True, padx=30, pady=10)
        self.show_surname.pack(anchor="s", expand=True, padx=30, pady=10)
        self.show_tcno.pack(anchor="s", expand=True, padx=30, pady=10)
        self.submit_btn.pack(anchor="n", expand=True, padx=30, pady=20)

        refresh_button = CTkButton(master=self.extracting_tab, text="Refresh", command=self.perform_extracting_refresh)
        refresh_button.grid(row=0, column=1, padx=20, pady=(320,0))

        browse_button = CTkButton(self.extracting_image_frame, text="Choose Image", command=self.browse_extracting_image)
        browse_button.grid(row=0, column=0, pady=10)


    def perform_extracting_refresh(self):
        self.extracting_image_frame.destroy()
        self.extracted_information_frame.destroy()
        self.extraction_file_path = ""
        self.create_extracting_tab()

    def perform_embedding_refresh(self):
        self.image_frame.destroy()
        self.information_frame.destroy()
        self.create_embedding_tab()

    def browse_image(self):  
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                print("Dosya yolu:", file_path)
            else:
                print("Dosya seçilmedi veya işlem iptal edildi.")
            self.image_path = file_path
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.image_frame.grid(row=0, column=1, padx=20, pady=10)
            self.display_embedding_image(photo, self.image_frame)
        except Exception as e:
            messagebox.showerror("Error", "Dosya seçilmedi veya işlem iptal edildi.")


    def browse_extracting_image(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                print("Dosya yolu:", file_path)
            else:
                print("Dosya seçilmedi veya işlem iptal edildi.")
            self.extraction_file_path = file_path
            image = Image.open(file_path)
            image.thumbnail((400, 400)) 
            photo = ImageTk.PhotoImage(image)
            self.extracting_image_frame.grid(row=0, column=0, padx=20, pady=10)
            self.display_extracting_image(photo, self.extracting_image_frame)
        except Exception as e:
            messagebox.showerror("Error", "Dosya seçilmedi veya işlem iptal edildi.")

    def validate_english_characters(self, new_text):
        if not all(char in string.ascii_letters for char in new_text):
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
                self.display_embedded_image(photo, self.new_image_frame)

                messagebox.showinfo("Embedding", "The operation has been completed successfully.")

                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
                if file_path:
                    imwrite(file_path, new_img)
                    print(f"Resim başarıyla kaydedildi: {file_path}")
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
                self.show_name.destroy()
                self.show_surname.destroy()
                self.show_tcno.destroy()
                self.submit_btn.destroy()
                self.show_name = CTkLabel(master=self.extracted_information_frame, text="Name:  " + self.name) 
                self.show_surname = CTkLabel(master=self.extracted_information_frame, text="Surname:  " + self.surname) 
                self.show_tcno = CTkLabel(master=self.extracted_information_frame, text="Tcno:  " + self.tcno)
                self.submit_btn = CTkButton(master=self.extracted_information_frame, text="Extracting", command=self.perform_extracting)
                self.show_name.pack(anchor="s", expand=True, padx=30, pady=10)
                self.show_surname.pack(anchor="s", expand=True, padx=30, pady=10)
                self.show_tcno.pack(anchor="s", expand=True, padx=30, pady=10)
                self.submit_btn.pack(anchor="n", expand=True, padx=30, pady=20)
                messagebox.showinfo("Extracting", "The operation has been completed successfully.")
            except Exception as e:
                self.perform_extracting_refresh()
                messagebox.showerror("Error", f"Information could not be extracted from the image")

    def display_embedding_image(self, photo, frame):
        if hasattr(self, "embedding_label"):
            self.embedding_label.destroy()
        self.embedding_label = CTkLabel(frame, image=photo, text="")
        self.embedding_label.image = photo
        self.embedding_label.grid(row=1, column=0, pady=10, padx=10)

    def display_extracting_image(self, photo, frame):
        if hasattr(self, "extracting_label"):
            self.extracting_label.destroy()
        self.extracting_label = CTkLabel(frame, image=photo, text="")
        self.extracting_label.image = photo
        self.extracting_label.grid(row=1, column=0, pady=10, padx=10)

    def display_embedded_image(self, photo, frame):
        if hasattr(self, "embedded_label"):
            self.embedded_label.destroy()
        self.embedded_label = CTkLabel(frame, image=photo, text="")
        self.embedded_label.image = photo
        self.embedded_label.grid(row=1, column=0, pady=10, padx=10)
        

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
