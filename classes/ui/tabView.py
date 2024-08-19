
import customtkinter as ctk
from classes.ui.createTab import CreateTab
from classes.ui.showTab import ShowTab
import json
import os

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Create")
        self.add("Show")

        self.create_frame = CreateTab(master=self.tab("Create"))
        self.create_frame.pack(fill="both", expand=True)

        self.show_frame = ShowTab(master=self.tab("Show"))
        self.show_frame.pack(fill="both", expand=True)

    