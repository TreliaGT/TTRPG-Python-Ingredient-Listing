import tkinter as tk
import customtkinter as ctk

class EditDialog(ctk.CTkToplevel):
    def __init__(self, master, ingredient, on_save):
        super().__init__(master)

        self.title("Edit Ingredient")
        self.geometry("800x800")
        self.on_save = on_save

        # Create and pack widgets for editing
        self.fields = {}
        for field, value in ingredient.items():
            ctk.CTkLabel(self, text=field.capitalize()).pack(pady=(10, 0))
            entry = ctk.CTkEntry(self, placeholder_text=f"Enter {field.capitalize()}")
            entry.pack(padx=20, pady=(0, 10), fill=tk.X)
            entry.insert(0, value)
            self.fields[field] = entry

        self.save_button = ctk.CTkButton(self, text="Save Changes", command=self.save)
        self.save_button.pack(pady=10)

    def save(self):
        # Call the provided on_save callback with the updated values
        updated_values = {field: entry.get() for field, entry in self.fields.items()}
        self.on_save(updated_values)
        self.destroy()
