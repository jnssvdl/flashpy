# pip install customtkinter
import customtkinter as ctk

# pip install CTkMessagebox
from CTkMessagebox import CTkMessagebox

# other module
from PIL import Image

# other classes
from infomanager import InformationManager

# CREATING A SET CLASS
class CreateSet(ctk.CTkFrame):
    def __init__(self, master, flashcards, to_library):
        # INITIALIZING THIS CLASS
        ctk.CTkFrame.__init__(self, master, fg_color="#F5EDE3")
        self.master = master
        self.flashcards = flashcards
        self.to_library = to_library
        self.design()

        # Initialize InformationManager and load sets from file
        self.info = InformationManager(".\\data\\sets.json", self.flashcards)
        self.info.loads_set_from_file()

        # List to store entries
        self.temp_lst = []

        # Library button
        self.library_button = ctk.CTkButton(self,
                                            text="Library", command=self.to_library,
                                            fg_color="transparent", text_color="#013652",
                                            font=("Montserrat", 15, "bold"),
                                            width=100, height=37, corner_radius=7,
                                            border_width=2, border_color="#013652", hover=False)
        self.library_button.bind('<Enter>', lambda event: self.library_button.configure(text_color="#F5EDE3", 
                                                                                        fg_color="#013652"))
        self.library_button.bind('<Leave>', lambda event: self.library_button.configure(text_color="#013652", 
                                                                                        fg_color="transparent"))
        self.library_button.place(x=35, y=30)

        # List to store entries
        self.frame_scroll = ctk.CTkScrollableFrame(self, 
                                                   width=500, 
                                                   height=340,
                                                   fg_color="#F6F6F6")
        self.frame_scroll.place(x=165, y=100)

        # Title entry
        self.title_entry = ctk.CTkEntry(self, 
                                        width=260, 
                                        height=35, 
                                        placeholder_text="Title of your set")
        self.title_entry.place(x=300, y=40)

        # Add button
        self.add_button = ctk.CTkButton(self,
                                        text="Add card",
                                        command=self.add,
                                        width=100, height=37, corner_radius=7,
                                        font=("Montserrat", 15, "bold"),
                                        fg_color="#013652", text_color="#F5EDE3")
        self.add_button.place(x=720, y=200)

        # Save button
        self.save_btn = ctk.CTkButton(self,
                                      text="Save set",
                                      command=self.save,
                                      width=100, height=37, corner_radius=7,
                                      font=("Montserrat", 15, "bold"),
                                      fg_color="#013652", text_color="#F5EDE3")
        self.save_btn.place(x=720, y=250)

        # New button
        self.new_btn = ctk.CTkButton(self,
                                     text="New set",
                                     command=self.new,
                                     width=100, height=37, corner_radius=7,
                                     font=("Montserrat", 15, "bold"),
                                     fg_color="#013652", text_color="#F5EDE3")
        self.new_btn.place(x=720, y=300)

        # Counter variables for grid positioning
        self.row_label = 0
        self.column_label = 0
    
    def design(self):
        """DISPLAY THE BG IMAGE ON THE FLASHCARDS FRAME."""
        bg = ctk.CTkImage(Image.open(".\\images\\bg.png"), size=(854, 480))
        bg_display = ctk.CTkLabel(self, image=bg, text="")
        bg_display.pack()

    # COMMAND THAT GETS EXECUTED WHEN THE add_button IS CLICKED
    """THIS COMMAND ADDS AND PLACES WIDGETS INSIDE THE SCROLLABLE FRAME - frame_scroll"""
    def add(self):
        term_label = ctk.CTkLabel(self.frame_scroll, 
                                  text="Term:", 
                                  font=("Montserrat", 11, "bold"))
        term_label.grid(row=self.row_label,
                        column=self.column_label,
                        padx=2,
                        pady=10)

        term_entry = ctk.CTkEntry(self.frame_scroll, width=90)
        term_entry.grid(row=self.row_label,
                        column=self.column_label + 1,
                        pady=10)

        definition_label = ctk.CTkLabel(self.frame_scroll,
                                        text="Definition:", 
                                        font=("Montserrat", 11, "bold"))
        
        definition_label.grid(row=self.row_label,
                              column=self.column_label + 2,
                              padx=2,
                              pady=10)

        definition_entry = ctk.CTkEntry(self.frame_scroll, 
                                        width=270)
        definition_entry.grid(row=self.row_label,
                              column=self.column_label + 3,
                              pady=10)
        
        del_btn = ctk.CTkButton(self.frame_scroll,
                                text="\u2573",
                                width=20,
                                fg_color="#88304E",
                                text_color="#F5EDE3",
                                hover_color="#800000",
                                command=lambda: self.delete_card(term_label,
                                                                 term_entry,
                                                                 definition_label,
                                                                 definition_entry,
                                                                 del_btn))
        del_btn.grid(row=self.row_label,
                     column=self.column_label + 4,
                     padx=2,
                     pady=10)

        self.row_label += 1
        self.temp_lst.append((term_entry, definition_entry))


    def delete_card(self, term_label, term_entry, definition_label, definition_entry, del_btn):
        self.temp_lst.remove((term_entry, definition_entry))
        term_label.destroy()
        term_entry.destroy()
        definition_label.destroy()
        definition_entry.destroy()
        del_btn.destroy()
        
        

    # COMMAND THAT GETS EXECUTED WHEN THE save BUTTON IS CLICKED
    """WHEN THIS METHOD GETS EXECUTED, THE ENTRIES FROM THE ADD METHOD ARE STORED IN A LIST
    AND THAT LIST BECOMES THE VALUE OF A KEY WHICH IS THE VALUE FROM title_entry"""
    def save(self):
        self.entry_values = [(term_entry.get(), definition_entry.get()) 
                             for term_entry, definition_entry in self.temp_lst 
                             if len(term_entry.get()) > 0 and len(definition_entry.get()) > 0]
        self.title = self.title_entry.get()
        if self.title in self.flashcards:
            self.msg_overwrite = CTkMessagebox(title="Warning!",
                                               message=f"{self.title} is already existing. Do you want to overwrite it?",
                                               option_1="No", 
                                               option_2="Yes", 
                                               icon="question")
            response = self.msg_overwrite.get()
            if response == "Yes":
                if len(self.entry_values) > 0:
                    if len(self.title) > 0:
                        if self.title not in self.flashcards:
                            self.flashcards[self.title] = []
                        self.flashcards[self.title] = self.entry_values
                        self.info.update_sets_to_file()
                print(self.temp_lst)
        else:
            if len(self.entry_values) > 0:
                if len(self.title) > 0:
                    if self.title not in self.flashcards:
                        self.flashcards[self.title] = []
                    self.flashcards[self.title] = self.entry_values
                    self.info.update_sets_to_file()
            print(self.temp_lst)

    # COMMAND THAT GETS EXECUTED WHEN THE new_button IS CLICKED
    """THIS METHOD DELETES THE STRING IN THE TITLE ENTRY AND
    REMOVES ALL THE WIDGETS(Labels and Entries) INSIDE THE FRAME_SCROLL"""
    def new(self):
        self.title_entry.delete(0, ctk.END)
        for item in self.frame_scroll.winfo_children():
            item.destroy()
        self.temp_lst.clear()
