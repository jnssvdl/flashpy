# pip install customtkinter
import customtkinter as ctk

# other module
from PIL import Image


class Library(ctk.CTkFrame):
    def __init__(self, master, flashcards, to_set, to_settings):
        # INITIALIZING THIS CLASS
        ctk.CTkFrame.__init__(self, master, fg_color="#F5EDE3")
        self.master = master
        self.flashcards = flashcards
        self.to_set = to_set
        self.to_settings = to_settings
        self.design ()

        # DELCARE THE WIDGETS IN THE LIBRAY FRAME
        self.lib_label = ctk.CTkLabel(self, 
                                      text="LIBRARY", 
                                      font=("Montserrat", 42, "bold"),
                                      text_color="#003049")
        
        self.lib_label.place(relx=0.5, rely=0.1, anchor='center')

        # Create set button
        self.set_button = ctk.CTkButton(self,
                                        text="Create set",
                                        command=self.to_set, fg_color="transparent", text_color="#013652",
                                        font=("Montserrat", 15, "bold"),
                                        width=100, height=37, corner_radius=7,
                                        border_width=2, border_color="#013652", hover=False)
        
        # hover functionality
        self.set_button.bind('<Enter>', lambda event: self.set_button.configure(text_color="#F5EDE3", fg_color="#013652"))
        self.set_button.bind('<Leave>', lambda event: self.set_button.configure(text_color="#013652", fg_color="transparent"))

        self.set_button.place(x=720, y=30)

        # Scrollable frame
        self.sets_frame = ctk.CTkScrollableFrame(self,
                                                 width=500,
                                                 height=320,
                                                 fg_color="#F6F6F6")
        self.sets_frame.place(x=165, y=100)

        self.update_sets_frame()

    """DISPLAY THE LOGO ON THE FLASHCARDS FRAME."""
    def design(self):
        """DISPLAY THE BG/IMAGELOGO ON THE FLASHCARDS FRAME."""
        bg = ctk.CTkImage(Image.open(".\\images\\bg.png"), size=(854, 480))
        bg_display = ctk.CTkLabel(self, image=bg, text="")
        bg_display.pack()

        bg_logo = ctk.CTkImage(Image.open(".\\images\\1.png"), size=(200, 50))
        bg_logo_display = ctk.CTkLabel(
            self, image=bg_logo, text="", bg_color="transparent")
        bg_logo_display.place(x=15, y=30)

    def cut_title(self, title):
        if len(title) > 55:
            return title[:52] + "..."
        return title


    def update_sets_frame(self):
        # THIS METHOD UPADTES THE sets_frame WHEN A NEW SET IS ADDED
        """THIS WORKS BY REMOVING ALL THE PRIOR WIDGETS (button) INSIDE THE sets_frame 
        THEN FILLS IT AGAIN WITH NEW BUTTONS WITH UPDATED KEY-VALUE IN THE DICTIONARY"""
        for item in self.sets_frame.winfo_children():
            item.destroy()
        for i, set_title in enumerate(self.flashcards):
            set_btn = ctk.CTkButton(self.sets_frame,
                                    text=self.cut_title(set_title),
                                    command=lambda set_title=set_title: self.to_settings(set_title),
                                    width=450,
                                    height=35,
                                    corner_radius=7,
                                    font=("Montserrat", 15, "bold"),
                                    fg_color="#6096B4", text_color="white")
            if i % 2:
                set_btn.configure(fg_color="#669BBC")
                set_btn.pack(pady=3)
            else:
                set_btn.configure(fg_color="#93BFCF")
                set_btn.pack(pady=3)