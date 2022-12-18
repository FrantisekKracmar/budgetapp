import tkinter as tk

from pages.login_page import LoginPage
from pages.main_page import MainPage


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("My awesome budget app")
        img = tk.PhotoImage(file="wallet.png")
        self.tk.call("wm", "iconphoto", self._w, img)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frame in (LoginPage, MainPage):
            frame = Frame(container, self)
            self.frames[Frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

        self.mainloop()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    App()
