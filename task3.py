import tkinter as tk
from tkinter import messagebox
import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.contacts = load_contacts()

        # Set up the main frame
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Contact list display
        self.contact_listbox = tk.Listbox(self.main_frame, height=10, width=50)
        self.contact_listbox.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        self.update_contact_listbox()

        # Buttons
        tk.Button(self.main_frame, text="Add Contact", command=self.add_contact_window).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.main_frame, text="View Contact", command=self.view_contact).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.main_frame, text="Edit Contact", command=self.edit_contact_window).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.main_frame, text="Delete Contact", command=self.delete_contact).grid(row=1, column=3, padx=5, pady=5)

    def update_contact_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, contact["name"])

    def add_contact_window(self):
        self.new_window("Add Contact", self.add_contact)

    def edit_contact_window(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            self.new_window("Edit Contact", self.edit_contact, selected_index[0])
        else:
            messagebox.showwarning("Edit Contact", "Please select a contact to edit.")

    def view_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            contact = self.contacts[selected_index[0]]
            contact_info = f"Name: {contact['name']}\nPhone: {contact['phone']}\nEmail: {contact['email']}"
            messagebox.showinfo("View Contact", contact_info)
        else:
            messagebox.showwarning("View Contact", "Please select a contact to view.")

    def add_contact(self, name, phone, email):
        if name and phone and email:
            self.contacts.append({"name": name, "phone": phone, "email": email})
            save_contacts(self.contacts)
            self.update_contact_listbox()
            messagebox.showinfo("Add Contact", "Contact added successfully.")
        else:
            messagebox.showwarning("Add Contact", "All fields are required.")

    def edit_contact(self, name, phone, email, index):
        if name and phone and email:
            self.contacts[index] = {"name": name, "phone": phone, "email": email}
            save_contacts(self.contacts)
            self.update_contact_listbox()
            messagebox.showinfo("Edit Contact", "Contact updated successfully.")
        else:
            messagebox.showwarning("Edit Contact", "All fields are required.")

    def delete_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            confirm = messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact?")
            if confirm:
                deleted_contact = self.contacts.pop(selected_index[0])
                save_contacts(self.contacts)
                self.update_contact_listbox()
                messagebox.showinfo("Delete Contact", f"Contact '{deleted_contact['name']}' deleted successfully.")
        else:
            messagebox.showwarning("Delete Contact", "Please select a contact to delete.")

    def new_window(self, title, action, index=None):
        window = tk.Toplevel(self.root)
        window.title(title)

        tk.Label(window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(window, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(window)
        phone_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        email_entry = tk.Entry(window)
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        if index is not None:
            contact = self.contacts[index]
            name_entry.insert(0, contact["name"])
            phone_entry.insert(0, contact["phone"])
            email_entry.insert(0, contact["email"])

        tk.Button(window, text="Save", command=lambda: self.save_and_close(window, action, name_entry.get(), phone_entry.get(), email_entry.get(), index)).grid(row=3, column=0, columnspan=2, pady=10)

    def save_and_close(self, window, action, name, phone, email, index):
        if index is not None:
            action(name, phone, email, index)
        else:
            action(name, phone, email)
        window.destroy()

def main():
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
