import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date, datetime


# ── Data classes (inline so file is self-contained) ───────────────────────────

class Item:
    def __init__(self, item_id, title, item_type):
        self.item_id = item_id
        self.title = title
        self.item_type = item_type
        self.status = "available"
        self.due_date = None

    def __str__(self):
        due = f"  |  Due: {self.due_date}" if self.due_date else ""
        return f"[{self.item_id}]  {self.title}  ({self.item_type})  —  {self.status.upper()}{due}"

    def borrow(self, due_date):
        self.status = "borrowed"
        self.due_date = due_date

    def return_item(self):
        self.status = "available"
        self.due_date = None


class Borrower:
    def __init__(self, borrower_id, name):
        self.borrower_id = borrower_id
        self.name = name
        self.borrowed_items = []

    def __str__(self):
        return f"{self.name}  (ID: {self.borrower_id})"

    def borrow_item(self, item):
        self.borrowed_items.append(item)

    def return_item(self, item):
        if item in self.borrowed_items:
            self.borrowed_items.remove(item)

    def get_borrowed_items(self):
        return self.borrowed_items


class LoanManager:
    def __init__(self):
        self.items = {}
        self.borrowers = {}

    def add_item(self, item):
        self.items[item.item_id] = item

    def add_borrower(self, borrower):
        self.borrowers[borrower.borrower_id] = borrower

    def get_all_items(self):
        return list(self.items.values())

    def get_all_borrowers(self):
        return list(self.borrowers.values())

    def borrow_item(self, item_id, borrower_id, due_date_str):
        item = self.items.get(item_id)
        borrower = self.borrowers.get(borrower_id)
        if not item or not borrower:
            return False
        if item.status == "borrowed":
            return False
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return False
        item.borrow(due_date)
        borrower.borrow_item(item)
        return True

    def return_item(self, item_id):
        item = self.items.get(item_id)
        if not item or item.status != "borrowed":
            return False
        for borrower in self.borrowers.values():
            if item in borrower.get_borrowed_items():
                borrower.return_item(item)
                break
        item.return_item()
        return True

    def get_overdue_items(self):
        today = date.today()
        return [
            item for item in self.items.values()
            if item.status == "borrowed" and item.due_date and item.due_date < today
        ]


# ── GUI ───────────────────────────────────────────────────────────────────────

# Colour palette
BG         = "#F8F9FB"
CARD_BG    = "#FFFFFF"
ACCENT     = "#4F46E5"      # indigo
ACCENT_DK  = "#3730A3"
TEAL       = "#0D9488"
TEAL_DK    = "#0F766E"
DANGER     = "#EF4444"
TEXT_MAIN  = "#1E293B"
TEXT_SUB   = "#64748B"
BORDER     = "#E2E8F0"
TAG_GREEN  = "#D1FAE5"
TAG_AMBER  = "#FEF3C7"
TAG_RED    = "#FEE2E2"
TAG_GREEN_FG = "#065F46"
TAG_AMBER_FG = "#92400E"
TAG_RED_FG   = "#991B1B"

FONT_H1    = ("Segoe UI", 16, "bold")
FONT_H2    = ("Segoe UI", 11, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO  = ("Consolas", 9)


def styled_button(parent, text, command, color=ACCENT, hover=ACCENT_DK, fg="white", **kwargs):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg=fg, activebackground=hover, activeforeground=fg,
        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
        padx=16, pady=8, bd=0, **kwargs
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def label_entry(parent, label_text, row, var=None):
    tk.Label(parent, text=label_text, font=FONT_SMALL, fg=TEXT_SUB, bg=CARD_BG, anchor="w")\
        .grid(row=row, column=0, sticky="w", padx=(20, 8), pady=(10, 0))
    e = ttk.Entry(parent, textvariable=var, font=FONT_BODY, width=28)
    e.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=20, pady=(2, 0))
    return e


class LoanManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Tracker")
        self.root.geometry("820x620")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.loan_manager = LoanManager()
        self._setup_initial_data()
        self._build_ui()

    # ── initial data ──────────────────────────────────────────────────────────
    def _setup_initial_data(self):
        for args in [("001", "The Great Gatsby", "Book"),
                     ("002", "Inception", "DVD"),
                     ("003", "1984", "Book")]:
            self.loan_manager.add_item(Item(*args))
        for args in [("B001", "Alice"), ("B002", "Bob")]:
            self.loan_manager.add_borrower(Borrower(*args))

    # ── top-level layout ──────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=ACCENT, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📚  Library Tracker", font=FONT_H1,
                 bg=ACCENT, fg="white").pack(side="left", padx=24)
        self.overdue_lbl = tk.Label(hdr, text="", font=FONT_SMALL,
                                    bg="#EF4444", fg="white", padx=10, pady=4)
        self.overdue_lbl.pack(side="right", padx=16)

        # Notebook
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",        background=BG,      borderwidth=0)
        style.configure("TNotebook.Tab",    font=FONT_BODY,     padding=[18, 8],
                        background=BORDER,  foreground=TEXT_SUB)
        style.map("TNotebook.Tab",
                  background=[("selected", CARD_BG)],
                  foreground=[("selected", ACCENT)])
        style.configure("TFrame", background=CARD_BG)

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=16, pady=12)

        self.tab_borrow    = ttk.Frame(nb)
        self.tab_return    = ttk.Frame(nb)
        self.tab_items     = ttk.Frame(nb)
        self.tab_borrowers = ttk.Frame(nb)

        nb.add(self.tab_borrow,    text="📤  Borrow")
        nb.add(self.tab_return,    text="📥  Return")
        nb.add(self.tab_items,     text="📚  Items")
        nb.add(self.tab_borrowers, text="👤  Borrowers")

        self._build_borrow_tab()
        self._build_return_tab()
        self._build_items_tab()
        self._build_borrowers_tab()

        self._refresh_overdue_badge()

    # ── Borrow tab ────────────────────────────────────────────────────────────
    def _build_borrow_tab(self):
        f = self.tab_borrow
        f.configure(style="TFrame")
        f.columnconfigure(0, weight=1)

        tk.Label(f, text="Borrow an Item", font=FONT_H2,
                 bg=CARD_BG, fg=TEXT_MAIN).grid(row=0, column=0, columnspan=2,
                                                 sticky="w", padx=20, pady=(18, 4))

        # Quick-reference box
        ref = tk.Frame(f, bg="#F1F5F9", bd=1, relief="solid")
        ref.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 8))
        tk.Label(ref, text="Quick Reference", font=("Segoe UI", 9, "bold"),
                 bg="#F1F5F9", fg=TEXT_SUB).pack(anchor="w", padx=10, pady=(6, 2))
        self.borrow_ref_lbl = tk.Label(ref, text="", font=FONT_MONO,
                                        bg="#F1F5F9", fg=TEXT_SUB, justify="left")
        self.borrow_ref_lbl.pack(anchor="w", padx=10, pady=(0, 6))
        self._refresh_borrow_ref()

        self.borrow_item_var     = tk.StringVar()
        self.borrow_borrower_var = tk.StringVar()
        self.borrow_date_var     = tk.StringVar()

        label_entry(f, "ITEM ID", 2, self.borrow_item_var)
        label_entry(f, "BORROWER ID", 4, self.borrow_borrower_var)
        label_entry(f, "DUE DATE  (YYYY-MM-DD)", 6, self.borrow_date_var)

        btn = styled_button(f, "Borrow Item →", self._borrow_item)
        btn.grid(row=8, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

    def _refresh_borrow_ref(self):
        lines = []
        for i in self.loan_manager.get_all_items():
            tag = "✓" if i.status == "available" else "✗"
            lines.append(f"  {tag}  {i.item_id}  {i.title}")
        lines.append("")
        for b in self.loan_manager.get_all_borrowers():
            lines.append(f"     {b.borrower_id}  {b.name}")
        self.borrow_ref_lbl.config(text="\n".join(lines))

    def _borrow_item(self):
        item_id     = self.borrow_item_var.get().strip()
        borrower_id = self.borrow_borrower_var.get().strip()
        due_date    = self.borrow_date_var.get().strip()

        if not all([item_id, borrower_id, due_date]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            y, m, d = map(int, due_date.split("-"))
            date(y, m, d)
        except ValueError:
            messagebox.showerror("Error", "Invalid date — use YYYY-MM-DD.")
            return

        if self.loan_manager.borrow_item(item_id, borrower_id, due_date):
            messagebox.showinfo("Success", "Item borrowed successfully!")
            self.borrow_item_var.set("")
            self.borrow_borrower_var.set("")
            self.borrow_date_var.set("")
            self._refresh_all()
        else:
            messagebox.showerror("Error",
                "Could not borrow item.\nCheck IDs are correct and item is available.")

    # ── Return tab ────────────────────────────────────────────────────────────
    def _build_return_tab(self):
        f = self.tab_return
        f.configure(style="TFrame")
        f.columnconfigure(0, weight=1)

        tk.Label(f, text="Return an Item", font=FONT_H2,
                 bg=CARD_BG, fg=TEXT_MAIN).grid(row=0, column=0, columnspan=2,
                                                 sticky="w", padx=20, pady=(18, 4))

        # Currently borrowed box
        box = tk.Frame(f, bg="#F1F5F9", bd=1, relief="solid")
        box.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 8))
        tk.Label(box, text="Currently Borrowed", font=("Segoe UI", 9, "bold"),
                 bg="#F1F5F9", fg=TEXT_SUB).pack(anchor="w", padx=10, pady=(6, 2))
        self.return_ref_lbl = tk.Label(box, text="", font=FONT_MONO,
                                        bg="#F1F5F9", fg=TEXT_SUB, justify="left")
        self.return_ref_lbl.pack(anchor="w", padx=10, pady=(0, 6))
        self._refresh_return_ref()

        self.return_item_var = tk.StringVar()
        label_entry(f, "ITEM ID TO RETURN", 2, self.return_item_var)

        btn = styled_button(f, "Return Item ↩", self._return_item, color=TEAL, hover=TEAL_DK)
        btn.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

    def _refresh_return_ref(self):
        borrowed = [i for i in self.loan_manager.get_all_items() if i.status == "borrowed"]
        if borrowed:
            today = date.today()
            lines = []
            for i in borrowed:
                overdue = i.due_date and i.due_date < today
                flag = "  ⚠ OVERDUE" if overdue else ""
                lines.append(f"  {i.item_id}  {i.title}  — due {i.due_date}{flag}")
            self.return_ref_lbl.config(text="\n".join(lines))
        else:
            self.return_ref_lbl.config(text="  No items currently borrowed.")

    def _return_item(self):
        item_id = self.return_item_var.get().strip()
        if not item_id:
            messagebox.showerror("Error", "Item ID is required.")
            return
        if self.loan_manager.return_item(item_id):
            messagebox.showinfo("Success", "Item returned successfully!")
            self.return_item_var.set("")
            self._refresh_all()
        else:
            messagebox.showerror("Error",
                "Could not return item.\nCheck the ID is correct and the item is borrowed.")

    # ── Items tab ─────────────────────────────────────────────────────────────
    def _build_items_tab(self):
        f = self.tab_items
        f.configure(style="TFrame")
        f.columnconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)

        hdr_row = tk.Frame(f, bg=CARD_BG)
        hdr_row.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 6))
        tk.Label(hdr_row, text="All Items", font=FONT_H2,
                 bg=CARD_BG, fg=TEXT_MAIN).pack(side="left")
        styled_button(hdr_row, "↺ Refresh", self._refresh_items_tab,
                      color=BORDER, hover="#CBD5E1", fg=TEXT_MAIN).pack(side="right")

        cols = ("id", "title", "type", "status", "due_date")
        self.items_tree = ttk.Treeview(f, columns=cols, show="headings", height=14)
        for col, w, label in [
            ("id",       70,  "ID"),
            ("title",   200,  "Title"),
            ("type",     80,  "Type"),
            ("status",   90,  "Status"),
            ("due_date", 110, "Due Date"),
        ]:
            self.items_tree.heading(col, text=label)
            self.items_tree.column(col, width=w, anchor="w")

        sb = ttk.Scrollbar(f, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=sb.set)
        self.items_tree.grid(row=1, column=0, sticky="nsew", padx=(20, 0), pady=(0, 14))
        sb.grid(row=1, column=1, sticky="ns", padx=(0, 20), pady=(0, 14))

        # Row tags for colour coding
        self.items_tree.tag_configure("available", background=TAG_GREEN,  foreground=TAG_GREEN_FG)
        self.items_tree.tag_configure("borrowed",  background=TAG_AMBER,  foreground=TAG_AMBER_FG)
        self.items_tree.tag_configure("overdue",   background=TAG_RED,    foreground=TAG_RED_FG)

        self._refresh_items_tab()

    def _refresh_items_tab(self):
        for row in self.items_tree.get_children():
            self.items_tree.delete(row)
        today = date.today()
        for item in self.loan_manager.get_all_items():
            if item.status == "borrowed" and item.due_date and item.due_date < today:
                tag = "overdue"
            elif item.status == "borrowed":
                tag = "borrowed"
            else:
                tag = "available"
            self.items_tree.insert("", "end", values=(
                item.item_id, item.title, item.item_type,
                item.status, item.due_date or "—"
            ), tags=(tag,))

    # ── Borrowers tab ─────────────────────────────────────────────────────────
    def _build_borrowers_tab(self):
        f = self.tab_borrowers
        f.configure(style="TFrame")
        f.columnconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)

        hdr_row = tk.Frame(f, bg=CARD_BG)
        hdr_row.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 6))
        tk.Label(hdr_row, text="Borrowers", font=FONT_H2,
                 bg=CARD_BG, fg=TEXT_MAIN).pack(side="left")
        styled_button(hdr_row, "↺ Refresh", self._refresh_borrowers_tab,
                      color=BORDER, hover="#CBD5E1", fg=TEXT_MAIN).pack(side="right")

        cols = ("id", "name", "count", "items")
        self.borrowers_tree = ttk.Treeview(f, columns=cols, show="headings", height=14)
        for col, w, label in [
            ("id",    80,  "ID"),
            ("name", 160,  "Name"),
            ("count", 70,  "# Items"),
            ("items", 380, "Borrowed Items"),
        ]:
            self.borrowers_tree.heading(col, text=label)
            self.borrowers_tree.column(col, width=w, anchor="w")

        sb = ttk.Scrollbar(f, orient="vertical", command=self.borrowers_tree.yview)
        self.borrowers_tree.configure(yscrollcommand=sb.set)
        self.borrowers_tree.grid(row=1, column=0, sticky="nsew", padx=(20, 0), pady=(0, 14))
        sb.grid(row=1, column=1, sticky="ns", padx=(0, 20), pady=(0, 14))

        self._refresh_borrowers_tab()

    def _refresh_borrowers_tab(self):
        for row in self.borrowers_tree.get_children():
            self.borrowers_tree.delete(row)
        for b in self.loan_manager.get_all_borrowers():
            items_str = ",  ".join(
                f"{i.item_id} ({i.title})" for i in b.get_borrowed_items()
            ) or "—"
            self.borrowers_tree.insert("", "end", values=(
                b.borrower_id, b.name, len(b.get_borrowed_items()), items_str
            ))

    # ── helpers ───────────────────────────────────────────────────────────────
    def _refresh_overdue_badge(self):
        overdue = self.loan_manager.get_overdue_items()
        if overdue:
            self.overdue_lbl.config(text=f"⚠  {len(overdue)} overdue")
            self.overdue_lbl.pack(side="right", padx=16)
        else:
            self.overdue_lbl.pack_forget()

    def _refresh_all(self):
        self._refresh_borrow_ref()
        self._refresh_return_ref()
        self._refresh_items_tab()
        self._refresh_borrowers_tab()
        self._refresh_overdue_badge()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = LoanManagerGUI(root)
    root.mainloop()
