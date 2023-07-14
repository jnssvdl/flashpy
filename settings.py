# pip install customtkinter
import customtkinter as ctk

# pip install CTkMessagebox
from CTkMessagebox import CTkMessagebox

# other module
from PIL import Image

# other module
from infomanager import InformationManager


# UPDATE THE CARDS, ADD MORE CARDS, DELETE CARDS, DELETE THE ENTIRE SET
class Settings(ctk.CTkFrame):
    def __init__(self, master, flashcards, set_title, settings_to_library, settings_to_flashcards, cut_title):
        # INITIALIZING THIS CLASS
        ctk.CTkFrame.__init__(self, master, fg_color="#F5EDE3")
        self.master = master
        self.flashcards = flashcards
        self.set_title = set_title
        self.settings_to_library = settings_to_library
        self.settings_to_flashcards = settings_to_flashcards
        self.cut_title = cut_title
        self.design()

        # list for storing temporary terms/def data
        self.temp_lst = []

        # Initialize InformationManager and load sets from file
        self.info = InformationManager(".\\data\\sets.json", self.flashcards)
        self.info.loads_set_from_file()

        # Flashcard set's title will be displayed
        self.name_label = ctk.CTkLabel(self,
                                       text=self.cut_title(),
                                       font=("Montserrat", 35, "bold"),
                                       text_color="#003049")
        self.name_label.place(relx=0.5, rely=0.1, anchor='center')

        # right buttons
        self.library_btn = ctk.CTkButton(self,
                                         text="Library",
                                         command=self.settings_to_library,
                                         font=("Montserrat", 15, "bold"), fg_color="transparent", text_color="#013652",
                                         width=100, height=37, corner_radius=7,
                                         border_width=2, border_color="#013652", hover=False)
        self.library_btn.bind('<Enter>', lambda event: self.library_btn.configure(text_color="#F5EDE3", 
                                                                                  fg_color="#013652"))
        self.library_btn.bind('<Leave>', lambda event: self.library_btn.configure(text_color="#013652", 
                                                                                  fg_color="transparent"))
        self.library_btn.place(x=720, y=30)


        # left buttons
        self.delete_btn = ctk.CTkButton(self,
                                        text="Delete set",
                                        command=self.delete_set,
                                        width=100, height=37, corner_radius=7,
                                        font=("Montserrat", 15, "bold"), hover_color="#80393C",
                                        fg_color="#800000", text_color="#F5EDE3")
        self.delete_btn.place(x=35, y=180)

        self.add_btn = ctk.CTkButton(self, 
                                     text="Add card", 
                                     command=self.add_card, 
                                     width=100, corner_radius=7, height=37,
                                     font=("Montserrat", 15, "bold"),
                                     fg_color="#013652", text_color="#F5EDE3")
        self.add_btn.place(x=35, y=230)

        self.save_btn = ctk.CTkButton(self,
                                      text="Save set",
                                      command=self.save_set,
                                      width=100, height=37, corner_radius=7,
                                      font=("Montserrat", 15, "bold"),
                                      fg_color="#013652", text_color="#F5EDE3")
        self.save_btn.place(x=35, y=280)

        self.flashcards_btn = ctk.CTkButton(self,
                                            text="Flashcards",
                                            command=self.settings_to_flashcards,
                                            font=("Montserrat", 15, "bold"), fg_color="transparent", text_color="#013652",
                                            width=100, height=37, corner_radius=7,
                                            border_width=2, border_color="#013652", hover=False)
        self.flashcards_btn.bind('<Enter>', lambda event: self.flashcards_btn.configure(text_color="#F5EDE3", 
                                                                                        fg_color="#013652"))
        self.flashcards_btn.bind('<Leave>', lambda event: self.flashcards_btn.configure(text_color="#013652", 
                                                                                        fg_color="transparent"))
        self.flashcards_btn.place(x=35, y=330)

        # frame widgets
        self.termdef_frame = ctk.CTkScrollableFrame(self, 
                                                    width=500, 
                                                    height=340,
                                                    fg_color="#F6F6F6")
        self.termdef_frame.place(x=165, y=100)

        self.row_label = 0
        self.column_label = 0

        self.termdef_entries()
    
    def design(self):
        """DISPLAY THE BG IMAGE ON THE FLASHCARDS FRAME."""
        bg = ctk.CTkImage(Image.open(".\\images\\bg.png"), size=(854, 480))
        bg_display = ctk.CTkLabel(self, image=bg, text="")
        bg_display.pack()

    """UDPATE THE TERM AND DEFINITION ENTRIES IN THE FRAME WITH VALUES FROM THE FLASHCARDS."""
    def termdef_entries(self):
        self.temp_lst.clear()
        try:
            for term, definition in self.flashcards[self.set_title]:
                term_label = ctk.CTkLabel(self.termdef_frame, text="Term:",
                                          font=("Montserrat", 11, "bold"))
                term_label.grid(row=self.row_label,
                                column=self.column_label,
                                padx=2,
                                pady=10)

                term_entry = ctk.CTkEntry(self.termdef_frame, width=90)
                term_entry.insert(0, term)
                term_entry.grid(row=self.row_label,
                                column=self.column_label + 1,
                                pady=10)

                definition_label = ctk.CTkLabel(self.termdef_frame, text="Definition:",
                                                font=("Montserrat", 11, "bold"))
                definition_label.grid(row=self.row_label,
                                      column=self.column_label + 2,
                                      padx=2,
                                      pady=10)

                definition_entry = ctk.CTkEntry(self.termdef_frame, width=270)
                definition_entry.insert(0, definition)
                definition_entry.grid(row=self.row_label,
                                      column=self.column_label + 3,
                                      pady=10)

                del_btn = ctk.CTkButton(self.termdef_frame,
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
                
                self.temp_lst.append((term_entry, definition_entry))
                self.row_label += 1
        except:
            pass

    """THIS METHOD ALLOWS USER TO ADD MORE CARDS TO THE SET WHILE EDITING IT"""
    def add_card(self):
        term_label = ctk.CTkLabel(self.termdef_frame, text="Term:",
                                  font=("Montserrat", 11, "bold"))
        term_label.grid(row=self.row_label,
                        column=self.column_label,
                        padx=2,
                        pady=10)

        term_entry = ctk.CTkEntry(self.termdef_frame, width=90)
        term_entry.grid(row=self.row_label,
                        column=self.column_label + 1,
                        pady=10)

        definition_label = ctk.CTkLabel(self.termdef_frame, 
                                        text="Definition:",
                                        font=("Montserrat", 11, "bold"))
        
        definition_label.grid(row=self.row_label,
                              column=self.column_label + 2,
                              padx=2,
                              pady=10)

        definition_entry = ctk.CTkEntry(self.termdef_frame, 
                                        width=270)
        definition_entry.grid(row=self.row_label,
                              column=self.column_label + 3,
                              pady=10)
        
        del_btn = ctk.CTkButton(self.termdef_frame,
                                text="\u2573",
                                width=20,
                                fg_color="#88304E",
                                text_color="#F5EDE3",
                                    
                                command=lambda: self.delete_newcard(term_label,
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

    def delete_newcard(self, term_label, term_entry, definition_label, definition_entry, del_btn):
        self.temp_lst.remove((term_entry, definition_entry))
        term_label.destroy()
        term_entry.destroy()
        definition_label.destroy()
        definition_entry.destroy()
        del_btn.destroy()   


    def delete_card(self, term_label, term_entry, definition_label, definition_entry, del_btn):
        if len(self.flashcards[self.set_title]) > 1:
            self.delete_msgbox(term_label, term_entry, definition_label, definition_entry, del_btn)
        else:
            self.delete_set()

    def delete_msgbox(self, term_label, term_entry, definition_label, definition_entry, del_btn):
        self.delcard_msgbox = CTkMessagebox(title="Deleting Card.",
                                            message="Are you sure you want to delete this card?",
                                            option_1="No", 
                                            option_2="Yes", 
                                            button_color=("#1F538D", "#800000"), 
                                            icon="warning")
        response = self.delcard_msgbox.get()
        if response == "Yes":
            self.temp_lst.remove((term_entry, definition_entry))
            print(self.temp_lst)
            term_label.destroy()
            term_entry.destroy()
            definition_label.destroy()
            definition_entry.destroy()
            del_btn.destroy()
            self.save_set()

    """DELETE THE FLASHCARD SET FROM THE DICTIONARY AND UPDATE THE SETS FRAME."""
    def delete_set(self):
        self.msg_box = CTkMessagebox(title="Deleting Set.",
                                     message="Are you sure you want to delete this set?",
                                     option_1="No", 
                                     option_2="Yes", 
                                     button_color=("#1F538D", "#800000"), 
                                     icon="warning")
        response = self.msg_box.get()
        if response == "Yes":
            del self.flashcards[self.set_title]
            self.info.update_sets_to_file()
            self.settings_to_library()

    """SAVE THE CHANGES MADE TO THE FLASHCARD SET."""
    def save_set(self):
        self.entry_values = [(entry1.get(), entry2.get()) 
                             for entry1, entry2 in self.temp_lst 
                             if len(entry1.get()) > 0 and len(entry2.get()) > 0]
        self.flashcards[self.set_title] = self.entry_values
        print(len(self.flashcards[self.set_title]))
        if len(self.flashcards[self.set_title]) == 0:
            self.delete_set()
        else:
            self.update_sets_frame()
            self.info.update_sets_to_file()

    """UPDATE THE SETS FRAME WITH THE UPDATED FLASHCARD SET."""
    def update_sets_frame(self):
        for item in self.termdef_frame.winfo_children():
            item.destroy()
        self.info.update_sets_to_file()
        self.termdef_entries()
