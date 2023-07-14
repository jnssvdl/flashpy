# pip install customtkinter
import customtkinter as ctk

# other modules
import random as rnd
from PIL import Image


class Flashcards(ctk.CTkFrame):
    def __init__(self, master, flashcards, set_title, flashcards_to_library, cut_title):
        # INITIALIZING THIS CLASS
        ctk.CTkFrame.__init__(self, master, fg_color="#F5EDE3")
        self.master = master
        self.flashcards = flashcards
        self.set_title = set_title
        self.flashcards_to_library = flashcards_to_library
        self.cut_title = cut_title

        # DISPLAYING LOGO
        self.design()

        # CURRENT INDEX
        # IF THE CARD IF FLIPPED
        self.card_index = 0
        self.is_flipped = False

        # SELECTED SET BY USER
        self.selected_set = self.flashcards[self.set_title]
        self.length = len(self.selected_set)

        # SHUFFLING CARDS
        rnd.shuffle(self.selected_set)

        # UNPACKING TERM AND DEFINITION
        self.term, self.definition = self.selected_set[self.card_index]

        # MAIN FLASHCARD
        # displaying set title
        self.name_label = ctk.CTkLabel(self,
                                       text=self.cut_title(),
                                       font=("Montserrat", 35, "bold"),
                                       text_color="#003049")
        self.name_label.place(relx=0.5, rely=0.1, anchor='center')

        # library button
        self.library_btn = ctk.CTkButton(self,
                                         text="Library", fg_color="transparent", text_color="#013652",
                                         command=self.flashcards_to_library,
                                         font=("Montserrat", 15, "bold"),
                                         width=100, height=37, corner_radius=7,
                                         border_width=2, border_color="#013652", hover=False)

        # hover functionality
        self.library_btn.bind('<Enter>', lambda event: self.library_btn.configure(
            text_color="#F5EDE3", fg_color="#013652"))
        self.library_btn.bind('<Leave>', lambda event: self.library_btn.configure(
            text_color="#013652", fg_color="transparent"))
        self.library_btn.place(x=720, y=30)

        # frame of the flashcard
        self.card_frame = ctk.CTkFrame(self,
                                       width=500,
                                       height=330, border_width=1, border_color='#888888',
                                       corner_radius=7)

        # text of the flashcard
        self.card_label = ctk.CTkLabel(self.card_frame,
                                       text_color="black",
                                       font=("Montserrat", 22))

        # display settings
        self.card_label.place(relx=0.5, rely=0.5, anchor='center')
        self.card_frame.place(x=175, y=90)
        self.display_text()

        # Flip button
        self.flip_btn = ctk.CTkButton(self,
                                      text="Flip", text_color="#F5EDE3", fg_color="#013652",
                                      font=("Montserrat", 15, "bold"),
                                      width=100, height=37, corner_radius=7,
                                      border_width=2, border_color="#013652", hover=True)
        self.flip_btn.place(x=375, y=430)
        self.flip_btn.configure(command=self.flip_card)

        y_position_btn = 250
        # Previous button
        self.prev_btn = ctk.CTkButton(self,
                                      text="<<",
                                      command=self.previous_card, text_color="#013652", fg_color="transparent",
                                      font=("Montserrat", 15, "bold"),
                                      width=50, height=37, corner_radius=7,
                                      border_width=2, border_color="#013652", hover=False)

        # hover functionality
        self.prev_btn.bind('<Enter>', lambda event: self.prev_btn.configure(
            text_color="#F5EDE3", fg_color="#013652"))
        self.prev_btn.bind('<Leave>', lambda event: self.prev_btn.configure(
            text_color="#013652", fg_color="transparent"))
        self.prev_btn.place(x=110, y=y_position_btn)

        # Next button
        self.next_btn = ctk.CTkButton(self,
                                      text=">>",
                                      command=self.next_card, text_color="#013652", fg_color="transparent",
                                      font=("Montserrat", 15, "bold"),
                                      width=50, height=37, corner_radius=7,
                                      border_width=2, border_color="#013652", hover=False)

        # hover functionality
        self.next_btn.bind('<Enter>', lambda event: self.next_btn.configure(
            text_color="#F5EDE3", fg_color="#013652"))
        self.next_btn.bind('<Leave>', lambda event: self.next_btn.configure(
            text_color="#013652", fg_color="transparent"))
        self.next_btn.place(x=695, y=y_position_btn)

        # key functionality
        self.master.bind('<Up>', lambda event: self.flip_card())
        self.master.bind('<Down>', lambda event: self.flip_card())
        self.master.bind('<space>', lambda event: self.flip_card())
        self.master.bind('<Left>', lambda event: self.previous_card())
        self.master.bind('<Right>', lambda event: self.next_card())

    def design(self):
        """DISPLAY THE BG/IMAGELOGO ON THE FLASHCARDS FRAME."""
        bg = ctk.CTkImage(Image.open(".\\images\\bg.png"), size=(854, 480))
        bg_display = ctk.CTkLabel(self, image=bg, text="")
        bg_display.pack()

        bg_logo = ctk.CTkImage(Image.open(".\\images\\1.png"), size=(200, 50))
        bg_logo_display = ctk.CTkLabel(
            self, image=bg_logo, text="", bg_color="transparent")
        bg_logo_display.place(x=15, y=30)

    def flip_card(self, event=None):
        """Function to flip the card."""
        self.is_flipped = not self.is_flipped
        self.display_text()

    def next_card(self):
        """DISPLAY THE NEXT FLASHCARD IN THE SET."""
        self.card_index = (self.card_index + 1) % self.length
        self.term, self.definition = self.selected_set[self.card_index]
        self.is_flipped = False
        self.display_text()

    def previous_card(self):
        """DISPLAY THE PREVIOUS FLASHCARD IN THE SET."""
        self.card_index = (self.card_index - 1) % self.length
        self.term, self.definition = self.selected_set[self.card_index]
        self.is_flipped = False
        self.display_text()

    def display_text(self):
        """DIPLAY THE TEXT ON THE FLASHCARD."""
        if self.is_flipped:
            text = self.term
            color = "#F5F5F5"
            if len(text) > 35:
                text = self.newline_text(text)
        else:
            text = self.definition
            color = "#FEFEFE"
            if len(text) > 35:
                text = self.newline_text(text)
        self.card_frame.configure(fg_color=color)
        self.card_label.configure(text=text)

    def newline_text(self, text):
        # """ADD NEWLINE CHARACTERS TO LONG TEXT TO FIT WITHIN THE FLASHCARD WIDTH."""
        result = ""
        for i in range(len(text)):
            result += text[i]
            if (i + 1) % 34 == 0:
                if i < len(text) - 1 and text[i + 1] != " " and text[i] != " ":
                    result += "-\n"
                else:
                    result += "\n"
        return result