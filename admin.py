"""
admin.py
================================================================
TourismeMaroc — Desktop Admin Dashboard (Python Tkinter)
----------------------------------------------------------------
Features:
  - Sidebar navigation (Users, Destinations, Hotels, Restaurants,
    Statistics)
  - Tables (ttk.Treeview) listing records from MySQL
  - Add / Delete destinations, hotels, restaurants
  - View registered users
  - Simple statistics dashboard

Requirements:
  pip install mysql-connector-python

Configure your MySQL credentials in the DB_CONFIG dict below.
The database must already exist — import database/tourisme.sql
first (see README.md).
================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    mysql = None
    MySQLError = Exception

# ----------------------------------------------------------------
# Database configuration — edit to match your environment
# ----------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "tourisme",
}

# ----------------------------------------------------------------
# Color palette — matches the website's Moroccan-inspired theme
# ----------------------------------------------------------------
COLOR_BG = "#f3ead9"          # sand
COLOR_SIDEBAR = "#163b35"     # dark teal
COLOR_SIDEBAR_TEXT = "#f3ead9"
COLOR_PRIMARY = "#2f3f9e"     # majorelle blue
COLOR_ACCENT = "#c1502e"      # terracotta
COLOR_GOLD = "#c9a227"
COLOR_WHITE = "#ffffff"


def get_connection():
    """Returns a new MySQL connection, or raises an exception on failure."""
    if mysql is None:
        raise RuntimeError(
            "Le module 'mysql-connector-python' n'est pas installé.\n"
            "Installez-le avec : pip install mysql-connector-python"
        )
    return mysql.connector.connect(**DB_CONFIG)


class AdminApp(tk.Tk):
    """Main application window with sidebar navigation."""

    def __init__(self):
        super().__init__()
        self.title("TourismeMaroc — Admin Dashboard")
        self.geometry("1080x650")
        self.configure(bg=COLOR_BG)
        self.minsize(900, 560)

        self._build_layout()
        self.show_statistics()  # default view

    # ------------------------------------------------------------
    # Layout: sidebar + main content area
    # ------------------------------------------------------------
    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=220)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self, bg=COLOR_BG)
        self.content.pack(side="right", fill="both", expand=True)

        # --- Sidebar header ---
        tk.Label(
            self.sidebar, text="🕌 TourismeMaroc", bg=COLOR_SIDEBAR,
            fg=COLOR_GOLD, font=("Georgia", 16, "bold"), pady=24
        ).pack()

        nav_items = [
            ("📊  Statistiques", self.show_statistics),
            ("👤  Utilisateurs", self.show_users),
            ("🏙️  Destinations", self.show_destinations),
            ("🏨  Hôtels", self.show_hotels),
            ("🍽️  Restaurants", self.show_restaurants),
        ]

        for label, command in nav_items:
            btn = tk.Button(
                self.sidebar, text=label, command=command,
                bg=COLOR_SIDEBAR, fg=COLOR_SIDEBAR_TEXT, bd=0,
                font=("Segoe UI", 12), anchor="w", padx=24, pady=12,
                activebackground=COLOR_PRIMARY, activeforeground="white",
                cursor="hand2"
            )
            btn.pack(fill="x")

        tk.Label(self.sidebar, bg=COLOR_SIDEBAR).pack(expand=True, fill="y")  # spacer

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def page_title(self, text):
        tk.Label(
            self.content, text=text, bg=COLOR_BG, fg=COLOR_PRIMARY,
            font=("Georgia", 20, "bold"), anchor="w"
        ).pack(fill="x", padx=30, pady=(24, 10))

    # ------------------------------------------------------------
    # Reusable table builder
    # ------------------------------------------------------------
    def build_table(self, columns, rows, parent=None):
        parent = parent or self.content
        frame = tk.Frame(parent, bg=COLOR_BG)
        frame.pack(fill="both", expand=True, padx=30, pady=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                         background=COLOR_PRIMARY, foreground="white")
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))

        tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=150, anchor="w")

        for row in rows:
            tree.insert("", "end", values=row)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return tree

    def safe_query(self, query, params=None, fetch=True):
        """Runs a query and returns rows, showing an error dialog on failure."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchall() if fetch else None
            if not fetch:
                conn.commit()
            cursor.close()
            conn.close()
            return result
        except (MySQLError, RuntimeError) as e:
            messagebox.showerror("Erreur base de données", str(e))
            return [] if fetch else None

    # ------------------------------------------------------------
    # VIEW: Statistics
    # ------------------------------------------------------------
    def show_statistics(self):
        self.clear_content()
        self.page_title("📊 Statistiques générales")

        counts = {
            "Utilisateurs": self.safe_query("SELECT COUNT(*) FROM users"),
            "Destinations": self.safe_query("SELECT COUNT(*) FROM destinations"),
            "Hôtels": self.safe_query("SELECT COUNT(*) FROM hotels"),
            "Restaurants": self.safe_query("SELECT COUNT(*) FROM restaurants"),
        }

        cards_frame = tk.Frame(self.content, bg=COLOR_BG)
        cards_frame.pack(fill="x", padx=30, pady=10)

        colors = [COLOR_PRIMARY, COLOR_ACCENT, COLOR_GOLD, "#1f6b3a"]
        for i, (label, value) in enumerate(counts.items()):
            count_val = value[0][0] if value else 0
            card = tk.Frame(cards_frame, bg=colors[i % len(colors)], width=200, height=110)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            cards_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=str(count_val), bg=colors[i % len(colors)], fg="white",
                     font=("Segoe UI", 24, "bold")).pack(pady=(18, 0))
            tk.Label(card, text=label, bg=colors[i % len(colors)], fg="white",
                     font=("Segoe UI", 11)).pack()

    # ------------------------------------------------------------
    # VIEW: Users (read-only)
    # ------------------------------------------------------------
    def show_users(self):
        self.clear_content()
        self.page_title("👤 Utilisateurs inscrits")
        rows = self.safe_query("SELECT id, nom, email, created_at FROM users ORDER BY created_at DESC")
        self.build_table(("id", "nom", "email", "inscrit le"), rows)

    # ------------------------------------------------------------
    # VIEW: Destinations (add / delete)
    # ------------------------------------------------------------
    def show_destinations(self):
        self.clear_content()
        self.page_title("🏙️ Gestion des destinations")
        self._build_crud_form(
            fields=[("Ville", "city"), ("Description", "description"), ("Image", "image")],
            insert_sql="INSERT INTO destinations (city, description, image) VALUES (%s, %s, %s)",
            list_sql="SELECT id, city, description, image FROM destinations ORDER BY id DESC",
            delete_sql="DELETE FROM destinations WHERE id = %s",
            columns=("id", "city", "description", "image"),
        )

    # ------------------------------------------------------------
    # VIEW: Hotels (add / delete)
    # ------------------------------------------------------------
    def show_hotels(self):
        self.clear_content()
        self.page_title("🏨 Gestion des hôtels")
        self._build_crud_form(
            fields=[("Nom", "name"), ("Prix (MAD)", "price"), ("Note (/5)", "rating")],
            insert_sql="INSERT INTO hotels (name, price, rating) VALUES (%s, %s, %s)",
            list_sql="SELECT id, name, price, rating FROM hotels ORDER BY id DESC",
            delete_sql="DELETE FROM hotels WHERE id = %s",
            columns=("id", "name", "price", "rating"),
        )

    # ------------------------------------------------------------
    # VIEW: Restaurants (add / delete)
    # ------------------------------------------------------------
    def show_restaurants(self):
        self.clear_content()
        self.page_title("🍽️ Gestion des restaurants")
        self._build_crud_form(
            fields=[("Nom", "name"), ("Type de cuisine", "type"), ("Note (/5)", "rating")],
            insert_sql="INSERT INTO restaurants (name, type, rating) VALUES (%s, %s, %s)",
            list_sql="SELECT id, name, type, rating FROM restaurants ORDER BY id DESC",
            delete_sql="DELETE FROM restaurants WHERE id = %s",
            columns=("id", "name", "type", "rating"),
        )

    # ------------------------------------------------------------
    # Generic CRUD form + table builder used by the 3 views above
    # ------------------------------------------------------------
    def _build_crud_form(self, fields, insert_sql, list_sql, delete_sql, columns):
        form_frame = tk.Frame(self.content, bg=COLOR_BG)
        form_frame.pack(fill="x", padx=30, pady=(0, 10))

        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=label, bg=COLOR_BG, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=i, sticky="w", padx=4
            )
            entry = tk.Entry(form_frame, width=20)
            entry.grid(row=1, column=i, padx=4, pady=4)
            entries[key] = entry

        def refresh_table():
            rows = self.safe_query(list_sql)
            for child in table_holder.winfo_children():
                child.destroy()
            tree_ref["tree"] = self.build_table(columns, rows, parent=table_holder)

        def add_record():
            values = [entries[key].get().strip() for _, key in fields]
            if not all(values):
                messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
                return
            self.safe_query(insert_sql, tuple(values), fetch=False)
            for entry in entries.values():
                entry.delete(0, tk.END)
            refresh_table()

        def delete_record():
            selected = tree_ref["tree"].selection() if "tree" in tree_ref else None
            if not selected:
                messagebox.showinfo("Sélection", "Sélectionnez une ligne à supprimer dans le tableau.")
                return
            item = tree_ref["tree"].item(selected[0])
            record_id = item["values"][0]
            if messagebox.askyesno("Confirmer", f"Supprimer l'enregistrement #{record_id} ?"):
                self.safe_query(delete_sql, (record_id,), fetch=False)
                refresh_table()

        tk.Button(
            form_frame, text="➕ Ajouter", command=add_record,
            bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 9, "bold"),
            padx=14, pady=6, bd=0, cursor="hand2"
        ).grid(row=1, column=len(fields), padx=10)

        tk.Button(
            form_frame, text="🗑️ Supprimer la sélection", command=delete_record,
            bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 9, "bold"),
            padx=14, pady=6, bd=0, cursor="hand2"
        ).grid(row=1, column=len(fields) + 1, padx=10)

        table_holder = tk.Frame(self.content, bg=COLOR_BG)
        table_holder.pack(fill="both", expand=True)

        tree_ref = {}
        rows = self.safe_query(list_sql)
        tree_ref["tree"] = self.build_table(columns, rows, parent=table_holder)


if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()
