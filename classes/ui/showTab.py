import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from classes.ingredients import Ingredient
from classes.ui.editDialog import EditDialog
import json
import os

class ShowTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Initialize the Treeview for displaying ingredients
        self.tree = ttk.Treeview(self, columns=("name","rare", "effect", "type", "taste", "description", "environment"), show='headings')
        self.tree.heading("name", text="Name")
        self.tree.heading("rare" , text="Rare")
        self.tree.heading("effect", text="Effect")
        self.tree.heading("type", text="Type")
        self.tree.heading("taste", text="Taste")
        self.tree.heading("description", text="Description")
        self.tree.heading("environment", text="Environment")
        self.tree.column("name", width=120)
        self.tree.column("rare", width=120)
        self.tree.column("effect", width=120)
        self.tree.column("type", width=120)
        self.tree.column("taste", width=120)
        self.tree.column("description", width=200)
        self.tree.column("environment", width=120)
        self.tree.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Configure row and column weights to make the widget expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add buttons for editing, deleting, and refreshing
        self.edit_button = ctk.CTkButton(self, text="Edit", command=self.edit_selected)
        self.edit_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.delete_button = ctk.CTkButton(self, text="Delete", command=self.delete_selected)
        self.delete_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh_data)
        self.refresh_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.tree.heading("environment", command=lambda: self.sort_by("environment"))
        self.tree.heading("rare", command=lambda: self.sort_by("rare"))
        self.tree.heading("name", command=lambda: self.sort_by("name"))
        self.tree.heading("effect", command=lambda: self.sort_by("effect"))
        self.tree.heading("type", command=lambda: self.sort_by("type"))
        self.tree.heading("taste", command=lambda: self.sort_by("taste"))
        
        # Load ingredients when initializing
        self.load_ingredients()

    def load_ingredients(self):
        file_path = "ingredient_data.json"

        # Clear existing data
        self.tree.delete(*self.tree.get_children())

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    ingredients = data.get("ingredients", [])

                    # Insert ingredients into the Treeview
                    for ingredient in ingredients:
                        self.tree.insert("", "end", iid=ingredient['name'], values=(
                            ingredient.get('name', 'N/A'),
                            ingredient.get('rare', 'N/A'),
                            ingredient.get('effect', 'N/A'),
                            ingredient.get('type', 'N/A'),
                            ingredient.get('taste', 'N/A'),
                            ingredient.get('description', 'N/A'),
                            ingredient.get('environment', 'N/A')
                        ))

            except json.JSONDecodeError:
                print("Error reading JSON file. The file may be corrupted or improperly formatted.")
            except FileNotFoundError:
                pass

       
    def sort_by(self, column):
        # Retrieve all items and their values
        data = [(self.tree.item(child)['values'], child) for child in self.tree.get_children()]

        # Determine sort index based on the column
        column_index = self.tree['columns'].index(column)
        
        # Sort data based on the selected column
        if column == "rare":
            # Assuming rare is numeric or boolean; adjust sorting as needed
            data.sort(key=lambda x: (x[0][column_index], x[1]))
        else:
            # For text columns, ensure sorting is done as strings
            data.sort(key=lambda x: (str(x[0][column_index]), x[1]))

        # Update Treeview with sorted data
        for index, (values, iid) in enumerate(data):
            self.tree.move(iid, '', index)


    def edit_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0], 'values')
            fields = ["name", "rare","effect", "type", "taste", "description", "environment"]
            ingredient = dict(zip(fields, item_values))

            # Open the edit dialog
            EditDialog(self, ingredient, self.save_changes)

    def save_changes(self, updated_values):
        # Update the Treeview item
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            self.tree.item(item_id, values=(
                updated_values.get('name', 'N/A'),
                updated_values.get('rare' , 'N/A'),
                updated_values.get('effect', 'N/A'),
                updated_values.get('type', 'N/A'),
                updated_values.get('taste', 'N/A'),
                updated_values.get('description', 'N/A'),
                updated_values.get('environment', 'N/A')
            ))

            # Update the JSON file
            file_path = "ingredient_data.json"
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        ingredients = data.get("ingredients", [])

                    # Find and update the ingredient
                    for ingredient in ingredients:
                        if ingredient['name'] == item_id:
                            ingredient.update(updated_values)
                            break

                    with open(file_path, 'w') as file:
                        json.dump(data, file, indent=4)

                except json.JSONDecodeError:
                    print("Error reading JSON file. The file may be corrupted or improperly formatted.")

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]

            # Confirm deletion
            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {item_id}?"):
                self.tree.delete(item_id)

                # Remove the ingredient from the JSON file
                file_path = "ingredient_data.json"
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            ingredients = data.get("ingredients", [])

                        # Remove the ingredient from the list
                        ingredients = [i for i in ingredients if i['name'] != item_id]

                        with open(file_path, 'w') as file:
                            json.dump({"ingredients": ingredients}, file, indent=4)

                    except json.JSONDecodeError:
                        print("Error reading JSON file. The file may be corrupted or improperly formatted.")

    def refresh_data(self):
        self.load_ingredients()
