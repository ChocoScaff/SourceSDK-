import tkinter as tk

class Terminal(tk.Text):
    """
    Terminal on the GUI
    """


    def __init__(self, master, **kwargs):
        """
        """
        super().__init__(master, **kwargs)
        self.tag_configure("stdout", foreground="black")
        self.tag_configure("stderr", foreground="red")

    def write(self, message):
        """
        """
        self.insert(tk.END, message)
        self.see(tk.END)

    def flush(self):
        """
        TODO delette
        """
        pass