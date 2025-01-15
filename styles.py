import tkinter as tk

BOARD = "#011627"
BLACK = "#01101c"
WHITE = "#E4DFDA"

class MyButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=tk.GROOVE,
            bd=1, 
            highlightthickness=0,  
            padx=10,  
            pady=5,  
            font=("Arial Narrow", 10),  
            foreground=WHITE, 
            background= BOARD, 
        )

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(background=BLACK)  

    def on_leave(self, event):
        self.config(background=BOARD)

class MyMenuButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=tk.FLAT,
            bd=0, 
            highlightthickness=0,  
            padx=10,  
            pady=5,  
            font=("Arial Narrow", 16),  
            foreground=WHITE, 
            background= BOARD, 
        )

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(background=BLACK)  

    def on_leave(self, event):
        self.config(background=BOARD)
        
class MyLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            bd=0, 
            font=("Arial", 12),  
            fg=WHITE, 
            bg= BOARD, 
        )
