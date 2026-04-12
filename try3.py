import tkinter as tk

root = tk.Tk()

label = tk.Label(root, text="Hello")
label.grid(row=0, column=0)

def hide():
    label.grid_remove()

def show():
    label.grid()

tk.Button(root, text="Hide", command=hide).grid(row=1, column=0)
tk.Button(root, text="Show", command=show).grid(row=2, column=0)

root.mainloop()
