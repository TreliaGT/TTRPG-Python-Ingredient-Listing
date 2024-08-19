import customtkinter as ctk  # Use an alias for clarity
from classes.ui.tabView import MyTabView

class App(ctk.CTk):  # Use CTk from customtkinter
    def __init__(self):
        super().__init__()
        self.title("DND Ingredients")
        self.geometry("1000x800")
    
        self.tab_view = MyTabView(master=self)
        self.tab_view.pack(fill="both", expand=True)

app = App()
#app.set_appearance_mode("dark")  # CustomTkinter method
#app.set_default_color_theme(r"styles/style.json")  # Corrected path
app.mainloop()
