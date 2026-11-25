import hashlib
import tkinter as tk
from tkinter import messagebox

MAX_ATTEMPTS = 3

PAPER = "#f6f2e9"
FIELD = "#fffdf8"
INK = "#1c1e1b"
MUTED = "#6d675b"
BRASS = "#c9a75d"
GREEN = "#1f4d3f"
GREEN_DARK = "#163a2f"
LINE = "#d6cdb8"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


STAFF = {
    "admin":     {"hash": hash_password("lib2026"),   "role": "Администратор"},
    "librarian": {"hash": hash_password("books123"),  "role": "Библиотекарь"},
}


class LoginWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.attempts_left = MAX_ATTEMPTS
        self.show_password = tk.BooleanVar(value=False)

        root.title("Библиотека — вход")
        root.geometry("400x420")
        root.resizable(False, False)
        root.configure(bg=PAPER)

        tk.Frame(root, bg=INK, height=6).pack(fill="x")
        tk.Frame(root, bg=BRASS, height=2).pack(fill="x")

        head = tk.Frame(root, bg=PAPER)
        head.pack(pady=(26, 18))
        tk.Label(head, text="Б", font=("Georgia", 16, "bold"), fg=BRASS, bg=PAPER,
                 width=2, highlightthickness=1, highlightbackground=BRASS).pack(side="left", padx=(0, 12))
        titles = tk.Frame(head, bg=PAPER)
        titles.pack(side="left")
        tk.Label(titles, text="Библиотека", font=("Georgia", 20), fg=INK, bg=PAPER).pack(anchor="w")
        tk.Label(titles, text="система учёта книг", font=("Segoe UI", 9), fg=MUTED, bg=PAPER).pack(anchor="w")

        form = tk.Frame(root, bg=PAPER)
        form.pack(fill="x", padx=48)

        tk.Label(form, text="ЛОГИН", font=("Segoe UI", 8, "bold"), fg=MUTED, bg=PAPER).pack(anchor="w")
        self.entry_login = self.make_entry(form)
        self.entry_login.focus()

        tk.Label(form, text="ПАРОЛЬ", font=("Segoe UI", 8, "bold"), fg=MUTED, bg=PAPER).pack(anchor="w", pady=(12, 0))
        self.entry_password = self.make_entry(form, show="*")

        tk.Checkbutton(
            form, text="Показать пароль", variable=self.show_password, command=self.toggle_password,
            bg=PAPER, fg=INK, activebackground=PAPER, selectcolor=FIELD, font=("Segoe UI", 9),
            highlightthickness=0, bd=0,
        ).pack(anchor="w", pady=(8, 0))

        tk.Button(
            form, text="Войти", command=self.check_login, font=("Segoe UI", 10, "bold"),
            bg=GREEN, fg=PAPER, activebackground=GREEN_DARK, activeforeground=PAPER,
            relief="flat", bd=0, cursor="hand2", pady=8,
        ).pack(fill="x", pady=(18, 0))

        self.status = tk.Label(root, text=f"Осталось попыток: {self.attempts_left}",
                               font=("Segoe UI", 9), fg=MUTED, bg=PAPER)
        self.status.pack(pady=(14, 0))

        root.bind("<Return>", self.check_login)

    def make_entry(self, parent, show=""):
        entry = tk.Entry(
            parent, show=show, font=("Segoe UI", 11), bg=FIELD, fg=INK, relief="flat",
            insertbackground=INK, highlightthickness=1, highlightbackground=LINE, highlightcolor=GREEN,
        )
        entry.pack(fill="x", ipady=6, pady=(4, 0))
        return entry

    def toggle_password(self):
        self.entry_password.config(show="" if self.show_password.get() else "*")

    def check_login(self, event=None):
        login = self.entry_login.get().strip()
        password = self.entry_password.get()

        if not login or not password:
            messagebox.showwarning("Внимание", "Введите логин и пароль.")
            return

        user = STAFF.get(login)
        if user and user["hash"] == hash_password(password):
            messagebox.showinfo("Вход выполнен", f"Здравствуйте, {login}!\nРоль: {user['role']}")
            return

        self.attempts_left -= 1
        if self.attempts_left == 0:
            messagebox.showerror("Доступ закрыт", "Три неудачные попытки. Программа закрывается.")
            self.root.destroy()
            return

        messagebox.showerror("Ошибка", "Неверный логин или пароль.")
        self.status.config(text=f"Осталось попыток: {self.attempts_left}", fg="#9b2c22")
        self.entry_password.delete(0, tk.END)
        self.entry_password.focus()


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
