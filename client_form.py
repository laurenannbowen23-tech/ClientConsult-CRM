# client_form.py
# This module contains the form for adding and editing clients.

import customtkinter as ctk
from datetime import date
from . import database

class ClientForm(ctk.CTkToplevel):
    def __init__(self, master, client_id=None):
        super().__init__(master)
        self.master = master
        self.client_id = client_id

        if self.client_id:
            self.title("Edit Client")
        else:
            self.title("Add Client")

        self.geometry("700x850")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Add tabs
        self.tabview.add("Details")
        self.tabview.add("Interactions")

        # Configure the Details tab
        self.details_tab = self.tabview.tab("Details")
        self.details_tab.grid_columnconfigure(1, weight=1)
        self._create_details_form()

        # Configure the Interactions tab
        self.interactions_tab = self.tabview.tab("Interactions")
        self.interactions_tab.grid_columnconfigure(0, weight=1)
        self.interactions_tab.grid_rowconfigure(1, weight=1)
        self._create_interactions_tab()

        # Load data if editing
        if self.client_id:
            self.load_client_data()
            self.refresh_interactions_list()

    def _create_details_form(self):
        """Creates the form fields in the Details tab."""
        tab = self.details_tab

        # Form fields
        self.client_name_label = ctk.CTkLabel(tab, text="Client Name")
        self.client_name_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.client_name_entry = ctk.CTkEntry(tab)
        self.client_name_entry.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="ew")

        self.business_name_label = ctk.CTkLabel(tab, text="Business Name")
        self.business_name_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.business_name_entry = ctk.CTkEntry(tab)
        self.business_name_entry.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        self.business_type_label = ctk.CTkLabel(tab, text="Business Type")
        self.business_type_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.business_type_menu = ctk.CTkOptionMenu(tab, values=["E-commerce", "Brick and Mortar", "Service-based", "Other"])
        self.business_type_menu.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        self.email_label = ctk.CTkLabel(tab, text="Email")
        self.email_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.email_entry = ctk.CTkEntry(tab)
        self.email_entry.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        self.phone_label = ctk.CTkLabel(tab, text="Phone")
        self.phone_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.phone_entry = ctk.CTkEntry(tab)
        self.phone_entry.grid(row=4, column=1, padx=20, pady=5, sticky="ew")

        self.address_label = ctk.CTkLabel(tab, text="Mailing Address")
        self.address_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        self.address_entry = ctk.CTkEntry(tab)
        self.address_entry.grid(row=5, column=1, padx=20, pady=5, sticky="ew")

        self.needs_label = ctk.CTkLabel(tab, text="Client Needs")
        self.needs_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        self.needs_frame = ctk.CTkFrame(tab)
        self.needs_frame.grid(row=6, column=1, padx=20, pady=5, sticky="ew")
        self.db_setup_check = ctk.CTkCheckBox(self.needs_frame, text="DB Setup")
        self.db_setup_check.pack(side="left", padx=5)
        self.ai_integration_check = ctk.CTkCheckBox(self.needs_frame, text="AI Integration")
        self.ai_integration_check.pack(side="left", padx=5)
        self.training_check = ctk.CTkCheckBox(self.needs_frame, text="Training")
        self.training_check.pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(tab, text="Status")
        self.status_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        self.status_menu = ctk.CTkOptionMenu(tab, values=["Lead", "Active", "Completed"])
        self.status_menu.grid(row=7, column=1, padx=20, pady=5, sticky="ew")

        self.notes_label = ctk.CTkLabel(tab, text="Notes")
        self.notes_label.grid(row=8, column=0, padx=20, pady=5, sticky="w")
        self.notes_textbox = ctk.CTkTextbox(tab, height=100)
        self.notes_textbox.grid(row=8, column=1, padx=20, pady=5, sticky="ew")

        self.save_button = ctk.CTkButton(tab, text="Save Client", command=self.save_client)
        self.save_button.grid(row=9, column=1, padx=20, pady=20, sticky="e")

    def _create_interactions_tab(self):
        """Creates the interactions list and add form in the Interactions tab."""
        tab = self.interactions_tab

        # -- Add Interaction Form --
        add_frame = ctk.CTkFrame(tab)
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        add_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(add_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.interaction_type_menu = ctk.CTkOptionMenu(add_frame, values=["Call", "Email", "Meeting", "Note"], width=100)
        self.interaction_type_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(add_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.interaction_date_entry = ctk.CTkEntry(add_frame, width=120)
        self.interaction_date_entry.insert(0, date.today().isoformat())
        self.interaction_date_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(add_frame, text="Summary:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.interaction_summary_entry = ctk.CTkEntry(add_frame)
        self.interaction_summary_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(add_frame, text="Next Steps:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.interaction_next_steps_entry = ctk.CTkEntry(add_frame)
        self.interaction_next_steps_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        self.add_interaction_button = ctk.CTkButton(add_frame, text="Add Interaction", command=self.add_interaction)
        self.add_interaction_button.grid(row=3, column=3, padx=5, pady=10, sticky="e")

        # -- Interactions List --
        self.interactions_list_frame = ctk.CTkScrollableFrame(tab, label_text="Interaction History")
        self.interactions_list_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def load_client_data(self):
        """Loads existing client data into the form."""
        client = database.get_client_by_id(self.client_id)
        if client:
            # Use helper to safely insert, handling None values
            self._safe_insert(self.client_name_entry, client['client_name'])
            self._safe_insert(self.business_name_entry, client['business_name'])
            if client['business_type']:
                self.business_type_menu.set(client['business_type'])
            self._safe_insert(self.email_entry, client['email'])
            self._safe_insert(self.phone_entry, client['phone'])
            self._safe_insert(self.address_entry, client['address'])
            if client['status']:
                self.status_menu.set(client['status'])
            if client['notes']:
                self.notes_textbox.insert("1.0", client['notes'])

            needs = (client['needs'] or '').split(', ')
            if "DB Setup" in needs: self.db_setup_check.select()
            if "AI Integration" in needs: self.ai_integration_check.select()
            if "Training" in needs: self.training_check.select()

    def _safe_insert(self, widget, value):
        """Inserts value into an entry widget, handling None gracefully."""
        if value:
            widget.insert(0, value)

    def refresh_interactions_list(self):
        """Fetches and displays interactions for the current client."""
        # Clear existing
        for widget in self.interactions_list_frame.winfo_children():
            widget.destroy()

        if not self.client_id:
            ctk.CTkLabel(self.interactions_list_frame, text="Save the client first to add interactions.").pack(pady=20)
            return

        interactions = database.get_interactions(self.client_id)
        if not interactions:
            ctk.CTkLabel(self.interactions_list_frame, text="No interactions yet.").pack(pady=20)
            return

        for interaction in interactions:
            frame = ctk.CTkFrame(self.interactions_list_frame)
            frame.pack(fill="x", padx=5, pady=5)

            type_label = ctk.CTkLabel(frame, text=f"[{interaction['interaction_type']}]", font=ctk.CTkFont(weight="bold"), width=60)
            type_label.pack(side="left", padx=5)

            date_label = ctk.CTkLabel(frame, text=interaction['interaction_date'], width=100)
            date_label.pack(side="left", padx=5)

            summary_label = ctk.CTkLabel(frame, text=interaction['summary'] or "", anchor="w")
            summary_label.pack(side="left", padx=5, fill="x", expand=True)

            delete_btn = ctk.CTkButton(frame, text="X", width=30, fg_color="transparent", border_width=1,
                                       command=lambda i=interaction: self.delete_interaction(i['id']))
            delete_btn.pack(side="right", padx=5)

    def add_interaction(self):
        """Adds a new interaction for the client."""
        if not self.client_id:
            # Client must be saved first
            return

        interaction_type = self.interaction_type_menu.get()
        interaction_date = self.interaction_date_entry.get()
        summary = self.interaction_summary_entry.get()
        next_steps = self.interaction_next_steps_entry.get()

        database.add_interaction(self.client_id, interaction_date, interaction_type, summary, next_steps)

        # Clear the form
        self.interaction_summary_entry.delete(0, "end")
        self.interaction_next_steps_entry.delete(0, "end")

        self.refresh_interactions_list()

    def delete_interaction(self, interaction_id):
        """Deletes an interaction."""
        database.delete_interaction(interaction_id)
        self.refresh_interactions_list()

    def save_client(self):
        """Saves the client (add or update)."""
        needs = []
        if self.db_setup_check.get(): needs.append("DB Setup")
        if self.ai_integration_check.get(): needs.append("AI Integration")
        if self.training_check.get(): needs.append("Training")

        client_data = {
            "client_name": self.client_name_entry.get() or "",
            "business_name": self.business_name_entry.get() or "",
            "business_type": self.business_type_menu.get() or "",
            "email": self.email_entry.get() or "",
            "phone": self.phone_entry.get() or "",
            "address": self.address_entry.get() or "",
            "needs": ", ".join(needs),
            "status": self.status_menu.get() or "",
            "notes": self.notes_textbox.get("1.0", "end-1c") or ""
        }

        if self.client_id:
            # Update existing client
            database.update_client(self.client_id, client_data)
        else:
            # Add new client
            database.add_client(client_data)

        self.master.refresh_client_list()
        self.destroy()
