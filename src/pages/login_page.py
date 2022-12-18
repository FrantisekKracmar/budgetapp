import tkinter as tk
import tkinter.messagebox as messagebox
from hashlib import sha256

from database import Database
from pages.main_page import MainPage


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._controller = controller
        self._db = Database()

        self._render_content()

    def _render_content(self):
        label_name = tk.Label(self, text="Username")
        label_name.grid(row=0, column=0, padx=10, pady=10)
        self._entry_name = tk.Entry(self)
        self._entry_name.grid(row=0, column=1, padx=10, pady=10)
        label_pwd = tk.Label(self, text="Password")
        label_pwd.grid(row=1, column=0, padx=10, pady=10)
        self._entry_password = tk.Entry(self, show="*")
        self._entry_password.grid(row=1, column=1, padx=10, pady=10)
        button1 = tk.Button(
            self, text="Sign in", width=25, command=self.__verify_login
        )
        button1.grid(row=2, column=1, padx=10, pady=10)
        self._entry_name.focus_set()

    def __verify_login(self):
        entry_pwd = sha256(
            f"{self._entry_password.get()}".encode("ascii")
        ).hexdigest()
        expected_pwd = self._db.get_user_password(self._entry_name.get())
        if entry_pwd == expected_pwd:
            self._controller.show_frame(MainPage)
        else:
            messagebox.showerror("Error", "Username or password is invalid")
