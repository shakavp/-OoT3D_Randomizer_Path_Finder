"""
created on 22/01/2022
@author: Geraldo C. Zampoli
"""
import tkinter as tk
from tkinter import ttk

class MyApp():
    """
    Path calculator GUI
    """
    def __init__(self):
        self.root = tk.Tk()

        choices = [
            "House",
            "Market",
            "Kokori Florest",
            "Lost Woods"
            ]

        self.root.title('Path Calculator')

        label1 = tk.Label(self.root, text = "Origin")
        label1.grid(column=0, row=0, padx=(10, 10))

        self.combo1 = ttk.Combobox(self.root, values=choices)
        self.combo1.grid(column=0, row=1, padx=(10, 10))
        self.combo1.current(0)

        label2 = tk.Label(self.root, text = "Destination")
        label2.grid(column=2, row=0, padx=(10, 10))

        self.combo2 = ttk.Combobox(self.root, values=choices)
        self.combo2.grid(column=2, row=1, padx=(10, 10))
        self.combo2.current(0)

        button1 = ttk.Button(self.root, text="Add path", command=self.add)
        button1.grid(column=1, row=3, pady=(10, 10))

        button2 = ttk.Button(self.root, text="Calculate shortest path", command=self.calculate_path)
        button2.grid(column=1, row=4, pady=(0, 30))

        self.text_box = tk.Text(self.root, font= ('Arial', 8), height=22, width=70)
        self.text_box.grid(column=0, row=5, columnspan=3, pady=(0, 10))
        self.text_box.config(state='disabled')

    def _update_text(self, msg):
        """
        Update message on texbox
        """
        self.text_box.config(state='normal')
        self.text_box.delete(1.0, 'end')
        self.text_box.insert('end', msg)
        self.text_box.config(state='disabled')

    def _clear_text(self):
        """
        Clear textbox
        """
        self.text_box.delete(1.0, 'end')

    def add(self):
        """
        Add new conection to the digraph and prints a message on textbox
        """
        origin_add = self.combo1.get()
        destination_add = self.combo2.get()
        msg_aux = f"Adding {origin_add} -> {destination_add} to the digraph\n"
        self._update_text(msg_aux)

    def calculate_path(self):
        """
        Calculate the shortest path and print the steps on textbox
        """
        origin_add = self.combo1.get()
        destination_add = self.combo2.get()
        msg_aux = f"Searching shortest path from {origin_add} to {destination_add}\n"
        self._update_text(msg_aux)

app = MyApp()
app.root.mainloop()
