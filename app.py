# pip install customtkinter
import customtkinter as ctk

# other classes
from library import Library
from createset import CreateSet
from settings import Settings
from flashcards import Flashcards
from infomanager import InformationManager  

# ROOT CLASS
class App(ctk.CTk):
    def __init__(self):
        # INITIALIZING THIS CLASS
        ctk.CTk.__init__(self)

        # DATA
        self.flashcards = {}

        # DECLARING THE ROOT ATTRIBTUES
        self.title("FlashPy")
        self.iconbitmap(".\\images\\2.ico")
        self.geometry("854x480")
        self.resizable(width=False, height=False)
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("light")

        # INSTANTIATING THE FRAME OBJECTS
        self.info = InformationManager(".\\data\\sets.json", self.flashcards)
        self.info.loads_set_from_file()

        self.library = Library(self, self.flashcards, 
                               self.library_to_createset, 
                               self.library_to_settings)
        self.create_set = CreateSet(self, self.flashcards,
                                    self.createset_to_library)
        self.createset_to_library()
    
        # DISPLAYING LIBRARY
        self.library.pack(expand=True, fill=ctk.BOTH)

    def library_to_createset(self):
        self.library.pack_forget()
        self.create_set.pack(expand=True, fill=ctk.BOTH)

    def createset_to_library(self):
        for item in self.create_set.frame_scroll.winfo_children():
            item.destroy()

        self.create_set.temp_lst.clear()
        self.create_set.title_entry.delete(0, ctk.END)
        self.create_set.pack_forget()

        self.library.update_sets_frame()
        self.library.pack(expand=True, fill=ctk.BOTH)

        print(self.flashcards)

    def library_to_settings(self, set_title):
        self.set_title = set_title

        # INSTANTIATING ANOTHER FRAME
        self.settings = Settings(self, self.flashcards, 
                                 set_title,
                                 self.settings_to_library, 
                                 self.settings_to_flascards,
                                 self.cut_title)

        self.library.pack_forget()
        self.settings.pack(expand=True, fill=ctk.BOTH)

    def settings_to_library(self):
        self.library.update_sets_frame()
        self.settings.pack_forget()
        self.library.pack(expand=True, fill=ctk.BOTH)

    def settings_to_flascards(self):
        self.flashcard_frame = Flashcards(self, 
                                          self.flashcards,
                                          self.set_title, 
                                          self.flashcards_to_library,
                                          self.cut_title)
        print(self.flashcards[self.set_title])
        self.settings.pack_forget()
        self.flashcard_frame.pack(expand=True, fill=ctk.BOTH)

    def flashcards_to_library(self):
        self.flashcard_frame.pack_forget()
        self.library.pack(expand=True, fill=ctk.BOTH)
    
    def cut_title(self):
        if len(self.set_title) > 18:
            return self.set_title[:15] + "..."
        return self.set_title

def main():
    App().mainloop()


if __name__ == "__main__":
    main()
