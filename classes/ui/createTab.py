import customtkinter as ctk
from classes.ingredients import Ingredient
import json

class CreateTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.type_var = ""
        self.environment_var = ""

        # add widgets onto the frame, for example:
        self.label = ctk.CTkLabel(self, text="Create New Ingredient")  
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.name = ctk.CTkEntry(self, placeholder_text="Enter The Name")
        self.name.grid(row=1, column=0, padx=20, pady=10, sticky="ew" ) 

        self.rare = ctk.CTkComboBox(self, values=["Select rarity", "Common", "Uncommon" ,"Rare", "Very Rare" , "Unique", "One Of A Kind"], command=self.select_type)
        self.rare.grid(row=2, column=0, padx=20, pady=10, sticky="ew" ) 

        self.effect = ctk.CTkEntry(self, placeholder_text="Enter The Effect")
        self.effect.grid(row=3, column=0, padx=20, pady=10, sticky="ew" ) 

        self.taste = ctk.CTkEntry(self, placeholder_text="Enter Taste")
        self.taste.grid(row=4, column=0, padx=20, pady=10, sticky="ew" )  

        self.description = ctk.CTkEntry(self, placeholder_text="Enter Description")
        self.description.grid(row=5, column=0, padx=20, pady=10, sticky="ew" ) 

        self.type = ctk.CTkComboBox(self, values=["Select Type", "Herb", "Spice" ,"Meat", "Fruit" , "Nut", "Oil", "Fungi", "Grain" , "Vegetable" , "Other"], command=self.select_type)
        self.type.grid(row=6, column=0, padx=20, pady=10, sticky="ew" ) 

        self.environment = ctk.CTkComboBox(self, values=["Select Environment","Forest", "Desert" ,"Lava", "Ocean", "Dungeon", "Monster", "Mountain" , "Swamp", "City", "Cave", "Sky" ], command=self.select_environment)
        self.environment.grid(row=7, column=0, padx=20, pady=10, sticky="ew" ) 

        self.add = ctk.CTkButton(self, text="Add", command=self.create_ingredient)
        self.add.grid(row=8, column=0, padx=20, pady=10, sticky="ew" ) 

        self.confirmlabel = ctk.CTkLabel(self, text="")
        self.confirmlabel.grid(row=9, column=0, padx=20, pady=10, sticky="ew" ) 

        self.grid_columnconfigure(0, weight=1)

    def select_type(self , choice):
        self.type_var = choice
        print("Type dropdown clicked:", choice)

    
    def select_environment(self, choice):
        self.environment_var = choice
        print("Environment dropdown clicked:", choice)


    def create_ingredient(self):
        # Create a new ingredient dictionary
        new_ingredient = {
            "name": self.name.get(),
            "effect": self.effect.get(),
            "type": self.type_var,  # Assuming type_var is a StringVar or similar
            "taste": self.taste.get(),
            "description": self.description.get(),
            "environment": self.environment_var  # Assuming environment_var is a StringVar or similar
        }
        
        file_path = "ingredient_data.json"
        
        # Try to read the existing data from the JSON file
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If the file does not exist, initialize with an empty dictionary
            data = {}
        
        # Initialize ingredients list if it doesn't exist
        if "ingredients" not in data:
            data["ingredients"] = []

        # Append the new ingredient to the list
        data["ingredients"].append(new_ingredient)
        
        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        print("Ingredient Created")
        self.reset_form()
        self.confirmlabel.configure(text="Ingredient Created")


    def reset_form(self):
        self.name.delete(0, ctk.END)
        self.rare.set("Select rarity")
        self.taste.delete(0, ctk.END)
        self.effect.delete(0, ctk.END)
        self.description.delete(0, ctk.END)
        self.type.set("Select Type")
        self.environment.set("Select Environment")