# gui.py
# This module will contain the main application window and GUI logic.

import customtkinter as ctk
from . import database
from .client_form import ClientForm

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ClientConsult CRM")
        self.geometry("1024x768")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create a sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ClientConsult", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.add_client_button = ctk.CTkButton(self.sidebar_frame, text="Add Client", command=self.open_client_form)
        self.add_client_button.grid(row=1, column=0, padx=20, pady=10)

        self.refresh_button = ctk.CTkButton(self.sidebar_frame, text="Refresh", command=self.refresh_client_list)
        self.refresh_button.grid(row=2, column=0, padx=20, pady=10)


        # Create main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Search bar
        self.search_bar = ctk.CTkEntry(self.main_frame, placeholder_text="Search clients...")
        self.search_bar.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.search_bar.bind("<Return>", self.search_clients)


        # Client list
        self.client_list_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Clients")
        self.client_list_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        self.refresh_client_list()

    def open_client_form(self, client_id=None):
        self.client_form = ClientForm(self, client_id=client_id)
        self.client_form.grab_set()

    def refresh_client_list(self):
        # Clear existing client frames
        for widget in self.client_list_frame.winfo_children():
            widget.destroy()

        clients = database.get_all_clients()
        for i, client in enumerate(clients):
            client_frame = ctk.CTkFrame(self.client_list_frame)
            client_frame.pack(fill="x", padx=10, pady=5)

            # Make name a clickable button
            name_button = ctk.CTkButton(client_frame, text=f"{client['client_name']}", 
                                        font=ctk.CTkFont(weight="bold"),
                                        fg_color="transparent", hover_color=("gray70", "gray30"),
                                        text_color=("gray10", "#DCE4EE"), anchor="w",
                                        command=lambda c=client: self.open_client_form(c['id']))
            name_button.pack(side="left", padx=10)

            business_label = ctk.CTkLabel(client_frame, text=f"{client['business_name'] or ''}")
            business_label.pack(side="left", padx=10)

            # Add View/Edit/Delete buttons
            delete_button = ctk.CTkButton(client_frame, text="Delete", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda c=client: self.delete_client(c['id']))
            delete_button.pack(side="right", padx=10)
            edit_button = ctk.CTkButton(client_frame, text="Edit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda c=client: self.open_client_form(c['id']))
            edit_button.pack(side="right", padx=10)


    def search_clients(self, event=None):
        search_term = self.search_bar.get()
        # Clear existing client frames
        for widget in self.client_list_frame.winfo_children():
            widget.destroy()

        clients = database.search_clients(search_term)
        for i, client in enumerate(clients):
            client_frame = ctk.CTkFrame(self.client_list_frame)
            client_frame.pack(fill="x", padx=10, pady=5)

            # Make name a clickable button
            name_button = ctk.CTkButton(client_frame, text=f"{client['client_name']}", 
                                        font=ctk.CTkFont(weight="bold"),
                                        fg_color="transparent", hover_color=("gray70", "gray30"),
                                        text_color=("gray10", "#DCE4EE"), anchor="w",
                                        command=lambda c=client: self.open_client_form(c['id']))
            name_button.pack(side="left", padx=10)

            business_label = ctk.CTkLabel(client_frame, text=f"{client['business_name'] or ''}")
            business_label.pack(side="left", padx=10)
            
            # Add View/Edit/Delete buttons
            delete_button = ctk.CTkButton(client_frame, text="Delete", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda c=client: self.delete_client(c['id']))
            delete_button.pack(side="right", padx=10)
            edit_button = ctk.CTkButton(client_frame, text="Edit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda c=client: self.open_client_form(c['id']))
            edit_button.pack(side="right", padx=10)

    def delete_client(self, client_id):
        database.delete_client(client_id)
        self.refresh_client_list()

if __name__ == "__main__":
    database.create_table()
    app = App()
    app.mainloop()
