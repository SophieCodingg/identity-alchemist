import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import json
import csv
import sqlite3
from fake_identity_system import FakeIdentitySystem

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Identity Alchemist")
        self.geometry("1000x600")
        self.configure(fg_color="#1a1a2e")
        
        self.system = FakeIdentitySystem()
        
        self.load_and_set_icon()
        self.create_widgets()
        
    def load_and_set_icon(self):
        icon = Image.open("identity-alchemist-cover.png")
        icon = icon.resize((64, 64))
        self.icon = ImageTk.PhotoImage(icon)
        self.iconphoto(True, self.icon)
        
    def create_widgets(self):
        self.create_header()
        self.create_notebook()
        self.create_status_bar()
        
    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#0f3460")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        logo = ctk.CTkLabel(header_frame, image=self.icon, text="")
        logo.pack(side="left", padx=10)
        
        title = ctk.CTkLabel(header_frame, text="Identity Alchemist", font=("Roboto", 24, "bold"), text_color="#e94560")
        title.pack(side="left", padx=10)
        
    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.create_generate_tab()
        self.create_enhance_tab()
        self.create_analyze_tab()
        self.create_export_import_tab()
        self.create_encrypt_decrypt_tab()
        
    def create_generate_tab(self):
        generate_frame = ctk.CTkFrame(self.notebook, fg_color="#16213e")
        self.notebook.add(generate_frame, text="Generate")
        
        generate_frame.grid_columnconfigure(0, weight=1)
        generate_frame.grid_columnconfigure(1, weight=1)
        
        num_identities_label = ctk.CTkLabel(generate_frame, text="Number of Identities:", font=("Roboto", 14), text_color="white")
        num_identities_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.num_identities_entry = ctk.CTkEntry(generate_frame, font=("Roboto", 14))
        self.num_identities_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        generate_button = ctk.CTkButton(generate_frame, text="Generate Identities", font=("Roboto", 14), command=self.generate_identities)
        generate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(generate_frame)
        self.progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.progress_bar.set(0)
        
        columns = ("Name", "Age", "Gender", "Country")
        self.identity_tree = ttk.Treeview(generate_frame, columns=columns, show="headings")
        for col in columns:
            self.identity_tree.heading(col, text=col)
            self.identity_tree.column(col, width=100)
        self.identity_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(generate_frame, orient="vertical", command=self.identity_tree.yview)
        scrollbar.grid(row=3, column=2, sticky="ns")
        self.identity_tree.configure(yscrollcommand=scrollbar.set)
        
        generate_frame.grid_rowconfigure(3, weight=1)
        
        search_label = ctk.CTkLabel(generate_frame, text="Search:", font=("Roboto", 14))
        search_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        
        self.search_entry = ctk.CTkEntry(generate_frame, font=("Roboto", 14))
        self.search_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.search_identities)
        
    def create_enhance_tab(self):
        enhance_frame = ctk.CTkFrame(self.notebook, fg_color="#16213e")
        self.notebook.add(enhance_frame, text="Enhance")
        
        train_button = ctk.CTkButton(enhance_frame, text="Train Model", font=("Roboto", 14), command=self.train_model)
        train_button.pack(padx=10, pady=10)
        
        enhance_button = ctk.CTkButton(enhance_frame, text="Generate Enhanced Identity", font=("Roboto", 14), command=self.generate_enhanced_identity)
        enhance_button.pack(padx=10, pady=10)
        
        self.enhanced_identity_text = ctk.CTkTextbox(enhance_frame, font=("Roboto", 12), fg_color="#1a1a2e", text_color="#e94560")
        self.enhanced_identity_text.pack(expand=True, fill="both", padx=10, pady=10)
        
    def create_analyze_tab(self):
        analyze_frame = ctk.CTkFrame(self.notebook, fg_color="#16213e")
        self.notebook.add(analyze_frame, text="Analyze")
        
        analyze_button = ctk.CTkButton(analyze_frame, text="Analyze Identities", font=("Roboto", 14), command=self.analyze_identities)
        analyze_button.pack(padx=10, pady=10)
        
        self.analysis_text = ctk.CTkTextbox(analyze_frame, font=("Roboto", 12), fg_color="#1a1a2e", text_color="#e94560")
        self.analysis_text.pack(expand=True, fill="both", padx=10, pady=10)
        
    def create_export_import_tab(self):
        export_import_frame = ctk.CTkFrame(self.notebook, fg_color="#16213e")
        self.notebook.add(export_import_frame, text="Export/Import")
        
        export_label = ctk.CTkLabel(export_import_frame, text="Export:", font=("Roboto", 14, "bold"))
        export_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.export_format_var = tk.StringVar(value="csv")
        export_formats = ctk.CTkOptionMenu(export_import_frame, values=["csv", "json", "sql"], variable=self.export_format_var)
        export_formats.grid(row=0, column=1, padx=10, pady=10)
        
        export_button = ctk.CTkButton(export_import_frame, text="Export", font=("Roboto", 14), command=self.export_identities)
        export_button.grid(row=0, column=2, padx=10, pady=10)
        
        import_label = ctk.CTkLabel(export_import_frame, text="Import:", font=("Roboto", 14, "bold"))
        import_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.import_format_var = tk.StringVar(value="csv")
        import_formats = ctk.CTkOptionMenu(export_import_frame, values=["csv", "json", "sql"], variable=self.import_format_var)
        import_formats.grid(row=1, column=1, padx=10, pady=10)
        
        import_button = ctk.CTkButton(export_import_frame, text="Import", font=("Roboto", 14), command=self.import_identities)
        import_button.grid(row=1, column=2, padx=10, pady=10)
        
        export_import_frame.grid_columnconfigure(3, weight=1)
        
    def create_encrypt_decrypt_tab(self):
        encrypt_decrypt_frame = ctk.CTkFrame(self.notebook, fg_color="#16213e")
        self.notebook.add(encrypt_decrypt_frame, text="Encrypt/Decrypt")
        
        encrypt_button = ctk.CTkButton(encrypt_decrypt_frame, text="Encrypt Identities", font=("Roboto", 14), command=self.encrypt_identities)
        encrypt_button.pack(padx=10, pady=10)
        
        decrypt_button = ctk.CTkButton(encrypt_decrypt_frame, text="Decrypt Identities", font=("Roboto", 14), command=self.decrypt_identities)
        decrypt_button.pack(padx=10, pady=10)
        
        self.encrypt_decrypt_text = ctk.CTkTextbox(encrypt_decrypt_frame, font=("Roboto", 12), fg_color="#1a1a2e", text_color="#e94560")
        self.encrypt_decrypt_text.pack(expand=True, fill="both", padx=10, pady=10)
        
    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ctk.CTkLabel(self, textvariable=self.status_var, font=("Roboto", 10), anchor="w")
        status_bar.pack(side="bottom", fill="x", padx=10, pady=5)
        
    def generate_identities(self):
        try:
            num_identities = int(self.num_identities_entry.get())
            if num_identities <= 0:
                raise ValueError("Number of identities must be positive")
            
            self.progress_bar.set(0)
            self.update_idletasks()
            
            self.system.generate_identities(num_identities)
            self.update_identity_treeview()
            
            self.progress_bar.set(1)
            self.status_var.set(f"Generated {num_identities} identities")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        
    def update_identity_treeview(self):
        self.identity_tree.delete(*self.identity_tree.get_children())
        for i, identity in enumerate(self.system.generated_identities):
            self.identity_tree.insert("", "end", values=(
                f"{identity['first_name']} {identity['last_name']}",
                identity['age'],
                identity['gender'],
                identity['country']
            ))
        
    def train_model(self):
        try:
            self.system.train_model()
            self.status_var.set("Model trained successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def generate_enhanced_identity(self):
        try:
            enhanced_identity = self.system.generate_enhanced_identity()
            self.enhanced_identity_text.delete("1.0", tk.END)
            for key, value in enhanced_identity.items():
                self.enhanced_identity_text.insert(tk.END, f"{key}: {value}\n")
            self.status_var.set("Enhanced identity generated")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def analyze_identities(self):
        try:
            self.system.analyze_identities()
            self.analysis_text.delete("1.0", tk.END)
            age_distribution = self.system.identity_analyzer.get_age_distribution()
            gender_distribution = self.system.identity_analyzer.get_gender_distribution()
            country_distribution = self.system.identity_analyzer.get_country_distribution()
            common_names = self.system.identity_analyzer.get_most_common_names()
            
            self.analysis_text.insert(tk.END, "Age Distribution:\n")
            self.analysis_text.insert(tk.END, json.dumps(age_distribution, indent=2) + "\n\n")
            self.analysis_text.insert(tk.END, "Gender Distribution:\n")
            self.analysis_text.insert(tk.END, json.dumps(gender_distribution, indent=2) + "\n\n")
            self.analysis_text.insert(tk.END, "Country Distribution:\n")
            self.analysis_text.insert(tk.END, json.dumps(country_distribution, indent=2) + "\n\n")
            self.analysis_text.insert(tk.END, "Most Common Names:\n")
            self.analysis_text.insert(tk.END, json.dumps(common_names, indent=2) + "\n")
            
            self.status_var.set("Identity analysis completed")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def export_identities(self):
        try:
            format = self.export_format_var.get()
            filename = filedialog.asksaveasfilename(defaultextension=f".{format}")
            if filename:
                self.system.export_identities(format, filename)
                self.status_var.set(f"Identities exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def import_identities(self):
        try:
            format = self.import_format_var.get()
            filename = filedialog.askopenfilename(filetypes=[(f"{format.upper()} files", f"*.{format}")])
            if filename:
                self.system.import_identities(format, filename)
                self.update_identity_treeview()
                self.status_var.set(f"Identities imported from {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def encrypt_identities(self):
        try:
            self.system.encrypt_identities()
            self.encrypt_decrypt_text.delete("1.0", tk.END)
            self.encrypt_decrypt_text.insert(tk.END, "Identities encrypted successfully.\n")
            for i, identity in enumerate(self.system.encrypted_identities):
                self.encrypt_decrypt_text.insert(tk.END, f"Encrypted Identity {i+1}:\n")
                self.encrypt_decrypt_text.insert(tk.END, json.dumps(identity, indent=2) + "\n\n")
            self.status_var.set("Identities encrypted")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def decrypt_identities(self):
        try:
            self.encrypt_decrypt_text.delete("1.0", tk.END)
            self.encrypt_decrypt_text.insert(tk.END, "Identities decrypted successfully.\n")

            self.system.decrypted_identities = []
            for encrypted_identity in self.system.encrypted_identities:
                decrypted_identity = self.system.identity_encryptor.decrypt_identity(encrypted_identity)  # Pass encrypted_identity
                self.system.decrypted_identities.append(decrypted_identity)

            for i, identity in enumerate(self.system.decrypted_identities):
                self.encrypt_decrypt_text.insert(tk.END, f"Decrypted Identity {i+1}:\n")
                self.encrypt_decrypt_text.insert(tk.END, json.dumps(identity, indent=2) + "\n\n")
            self.status_var.set("Identities decrypted")
        except Exception as e:
            messagebox.showerror("Error", str(e))

        
    def search_identities(self, event):
        search_term = self.search_entry.get().lower()
        self.identity_tree.delete(*self.identity_tree.get_children())
        for identity in self.system.generated_identities:
            if search_term in f"{identity['first_name']} {identity['last_name']}".lower():
                self.identity_tree.insert("", "end", values=(
                    f"{identity['first_name']} {identity['last_name']}",
                    identity['age'],
                    identity['gender'],
                    identity['country']
                ))

if __name__ == "__main__":
    app = GUI()
    app.mainloop()